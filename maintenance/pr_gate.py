#!/usr/bin/env python3
"""Path-aware PR gate: one always-present check that can be made required.

The real validations only run for the paths they cover, so they cannot be
required directly without blocking docs-only PRs. This gate runs on every PR,
derives which validations the changed paths need, waits for those workflow runs
on the exact head SHA, and passes only if each needed job actually succeeded
(skipped does not count). Docs-only PRs pass immediately.

Required validations:
- maintenance/** or .github/workflows/** -> "Official-source maintenance" job "tests";
- generated branch (codex/official-update-*) touching APIs/** or
  maintenance/sources.json -> "Generated API draft validation" job "validate".

A hand-made API PR (not a generated branch) has no automated validation; the gate
reports that explicitly and leaves review to humans rather than pretending a check ran.
Read-only: it only lists workflow runs and jobs.
"""
import json
import os
import subprocess
import sys
import time

MAINTENANCE = ("Official-source maintenance", "tests")
DRAFT = ("Generated API draft validation", "validate")


def required(paths, head_ref):
    needs, notes = [], []
    if any(p.startswith("maintenance/") or p.startswith(".github/workflows/") for p in paths):
        needs.append(MAINTENANCE)
    api = any(p.startswith("APIs/") or p == "maintenance/sources.json" for p in paths)
    if api and (head_ref or "").startswith("codex/official-update-"):
        needs.append(DRAFT)
    elif api and any(p.startswith("APIs/") for p in paths):
        notes.append("API files changed outside a generated draft: no automated API validation exists; human review required")
    return needs, notes


def evaluate(needs, runs, jobs_by_run):
    """Return ("pass"|"pending"|"fail", details) for the latest run of each needed workflow."""
    details, state = [], "pass"
    for workflow, job in needs:
        candidates = sorted((r for r in runs if r["name"] == workflow), key=lambda r: r["id"], reverse=True)
        if not candidates:
            details.append({"workflow": workflow, "job": job, "status": "missing"})
            state = "pending" if state == "pass" else state
            continue
        run = candidates[0]
        if run["status"] != "completed":
            details.append({"workflow": workflow, "job": job, "status": "running", "run": run["id"]})
            state = "pending" if state == "pass" else state
            continue
        matching = [j for j in jobs_by_run.get(run["id"], []) if j["name"] == job]
        conclusion = matching[0]["conclusion"] if matching else "absent"
        details.append({"workflow": workflow, "job": job, "status": conclusion, "run": run["id"]})
        if conclusion != "success":
            state = "fail"
    return state, details


def gh(endpoint):
    return json.loads(subprocess.run(["gh", "api", "--method", "GET", endpoint], check=True,
                                     stdout=subprocess.PIPE, text=True).stdout)


def main():
    repo, pr = os.environ["GITHUB_REPOSITORY"], os.environ["PR_NUMBER"]
    head, head_ref = os.environ["HEAD_SHA"], os.environ["HEAD_REF"]
    paths = []
    for page in range(1, 31):
        batch = gh("repos/%s/pulls/%s/files?per_page=100&page=%d" % (repo, pr, page))
        paths += [f["filename"] for f in batch]
        if len(batch) < 100:
            break
    else:
        raise SystemExit("PR file list exceeds review bounds; fail closed")
    needs, notes = required(paths, head_ref)
    print(json.dumps({"needs": needs, "notes": notes, "files": len(paths)}))
    deadline = time.time() + int(os.environ.get("GATE_TIMEOUT", "1500"))
    while True:
        runs = [r for r in gh("repos/%s/actions/runs?head_sha=%s&per_page=50" % (repo, head))["workflow_runs"]
                if r["name"] in {w for w, _ in needs}]
        jobs = {r["id"]: gh("repos/%s/actions/runs/%d/jobs" % (repo, r["id"]))["jobs"]
                for r in runs if r["status"] == "completed"}
        state, details = evaluate(needs, runs, jobs)
        if state != "pending" or time.time() > deadline:
            break
        time.sleep(20)
    print(json.dumps({"state": state, "details": details}, indent=2))
    with open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a") as summary:
        summary.write("## PR gate\n\nState: **%s**\n\n```json\n%s\n```\n" % (state, json.dumps(
            {"needs": needs, "notes": notes, "details": details}, indent=2)))
    return 0 if state == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
