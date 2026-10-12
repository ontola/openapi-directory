#!/usr/bin/env python3
"""Plan one API update; explicitly publish a new draft without changing the checkout."""
import argparse
import copy
import json
import os
import re
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

import health
import update

REPOSITORY = "ontola/openapi-directory"
MANIFEST = "maintenance/sources.json"
BRANCH_PREFIX = "codex/official-update-"
# Generation 1 keeps the historical branch name; later generations of the same
# publication group use "--g<N>" (N >= 2, no leading zeros, bounded).
GENERATED_BRANCH = re.compile(r"(?P<group>[a-z0-9][a-z0-9-]{0,63}?)(?:--g(?P<n>[2-9]|[1-9][0-9]{1,2}))?")
RESERVED_SUFFIX = re.compile(r".*--g[0-9]*")
REQUIRED_INPUTS = {"maintenance/" + name for name in (
    "draft_pr.py", "update.py", "validation.py", "bundle.py", "samples.py", "releases.py",
    "report.py", "health.py", "conversion.py", "embedded.py", "response_keys.py", "requirements.txt",
    "package.json", "package-lock.json", "convert-swagger.cjs", "pending_pr.py", "refresh_pr.py",
    "eligibility.py")}


class PublicationFailure(ValueError):
    def __init__(self, receipt):
        super().__init__("Publication failed; review retained guard before retrying")
        self.receipt = receipt


def command(args, data=None, env=None):
    return subprocess.run(args, cwd=update.ROOT, input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True, env=env, timeout=120).stdout


def git(*args, data=None, env=None):
    return command(["git", *args], data, env)


def guard_inputs(base):
    # The existing importer uses local recipes/toolchain modules. They must be
    # exactly those in the comparison commit, including outside sparse checkout.
    paths = git("ls-tree", "-r", "--name-only", base, "maintenance").decode().splitlines()
    if not REQUIRED_INPUTS <= set(paths):
        raise ValueError("Comparison tree is missing required maintenance inputs; use the delivered tool revision")
    for path in paths:
        if Path(path).suffix in {".py", ".json", ".txt", ".yaml", ".yml", ".cjs"}:
            local = update.ROOT / path
            if local.is_symlink() or not local.is_file() or local.read_bytes() != git("show", base + ":" + path):
                raise ValueError("Local maintenance input differs from comparison tree: " + path)


def branch_name(group, generation=1):
    if type(generation) is not int or not 1 <= generation <= 999:
        raise ValueError("Invalid generated branch generation")
    return BRANCH_PREFIX + group + ("" if generation == 1 else "--g" + str(generation))


def branch_group(branch):
    """Return (group, generation) for a generated branch name, or (None, None)."""
    if not isinstance(branch, str) or not branch.startswith(BRANCH_PREFIX):
        return None, None
    match = GENERATED_BRANCH.fullmatch(branch[len(BRANCH_PREFIX):])
    if not match or RESERVED_SUFFIX.fullmatch(match["group"]):
        return None, None
    return match["group"], int(match["n"] or 1)


def with_branch(plan, branch):
    """A resealed copy of a plan for another generation of the same group."""
    group, _ = branch_group(branch)
    if group != plan["group"]:
        return plan
    result = copy.deepcopy(plan)
    result["branch"] = branch
    result["seal"] = seal(result)
    return result


def select_sources(manifest, source_id):
    sources = manifest["sources"]
    if manifest.get("schema_version") != 1 or len({s["id"] for s in sources}) != len(sources):
        raise ValueError("Invalid source manifest")
    if any(not isinstance(s["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", s["id"])
           or RESERVED_SUFFIX.fullmatch(s["id"]) for s in sources):
        raise ValueError("Unsafe source ID")
    selected = next((s for s in sources if s["id"] == source_id), None)
    if selected is None:
        raise ValueError("Unknown source ID: " + source_id)
    group = selected.get("publication_group", selected["id"])
    if (not isinstance(group, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", group)
            or RESERVED_SUFFIX.fullmatch(group)):
        raise ValueError("Unsafe publication group")
    members = [s for s in sources if s.get("publication_group", s["id"]) == group]
    if len({s["provider"] for s in members}) != 1:
        raise ValueError("A publication group must describe one provider's API")
    for source in members:
        if source.get("import_blocker"):
            raise ValueError(source["id"] + ": " + source["import_blocker"])
        target = Path(source["target"])
        if str(target) != source["target"]:
            raise ValueError("Source target must be canonical")
        update.destination(source, {"info": {"version": target.parent.name}})
    if len({s["target"] for s in members}) != len(members):
        raise ValueError("Group artifacts target the same file")
    return group, members


def seal(plan):
    return update.sha256(update.canonical({k: v for k, v in plan.items() if k != "seal"}).encode())


def build_plan(source_id, base, cache):
    revision = git("rev-parse", "--verify", base + "^{commit}").decode().strip()
    guard_inputs(revision)
    manifest_raw = git("show", revision + ":" + MANIFEST)
    group, sources = select_sources(json.loads(manifest_raw), source_id)
    checker = health.Checker(update.request, update.now, cache)
    shared_revisions = {}
    plan = {"schema_version": 1, "publication_protocol": 2, "group": group, "base_revision": revision,
            "branch": branch_name(group), "sources": [], "files": {},
            "service_prefixes": sorted({str(Path(s["target"]).parent.parent) + "/" for s in sources})}
    with tempfile.TemporaryDirectory() as directory:
        manifest = Path(directory) / "sources.json"
        manifest.write_bytes(manifest_raw)
        for source in sources:
            observation = checker.check(source)
            if observation.get("source_health_issue"):
                raise ValueError(observation["source_health_issue"])
            fetch_source = copy.deepcopy(source)
            config = fetch_source.get("github")
            repository_ref = (config["repository"].lower(), config["ref"]) if config else None
            if repository_ref in shared_revisions:
                config["ref"] = shared_revisions[repository_ref]
            raw, metadata = update.fetch(fetch_source)
            if config:
                if not re.fullmatch(r"[0-9a-f]{40}", metadata.get("revision") or ""):
                    raise ValueError("GitHub group artifact lacks a pinned source revision")
                if repository_ref in shared_revisions and metadata["revision"] != shared_revisions[repository_ref]:
                    raise ValueError("Companion source revision differs from pinned group snapshot")
                shared_revisions[repository_ref] = metadata["revision"]
            update.cache_snapshot(cache, source["id"], raw, metadata)
            spec, steps = update.prepare_document(source, raw, metadata, cache)
            metadata["transformations"] = steps
            update.cache_snapshot(cache, source["id"], raw, metadata)
            errors = update.validate_document(spec)
            if errors:
                raise ValueError("Native/prepared validation failed: " + "\n".join(errors))
            destination = str(update.destination(source, spec))
            baseline_path, old = update.baseline(source, spec, revision)
            previous = update.stored(destination, revision)
            comparison = update.compare(old, spec, source)
            if old is None:
                comparison.update(added_paths=sorted(spec["paths"]), removed_paths=[],
                                  added_operations=sorted(update.operation_set(spec)), removed_operations=[])
            if previous is None or update.compare(previous, spec, source)["status"] != "matches_source":
                result = update.import_document(source, spec, metadata, old, baseline_path)
                content = update.serialize_document(result)
                # Verify the whole curated vendor view, not just versions/counts.
                if update.compare(update.parse(content.encode()), spec)["status"] != "matches_source":
                    raise ValueError("Serialized import differs from curated vendor content")
                if destination in plan["files"]:
                    raise ValueError("Group artifacts target the same file")
                plan["files"][destination] = content
            advance = update.advance_target(manifest, source, Path(destination))
            if advance:
                manifest.write_bytes(advance[1])
            plan["sources"].append({"id": source["id"], "configuration": source,
                                    "fetch": metadata, "health": observation,
                                    "comparison": comparison, "destination": destination})
        if manifest.read_bytes() != manifest_raw:
            plan["files"][MANIFEST] = manifest.read_text()
    plan["status"] = "candidate" if plan["files"] else "matches_source"
    plan["seal"] = seal(plan)
    return plan


def guard_tree_paths(revision, paths):
    for path in paths:
        for part in [path, *[str(p) for p in Path(path).parents if str(p) != "."]]:
            entry = git("ls-tree", revision, "--", part).decode().strip()
            if entry and entry.split()[0] != ("100644" if part == path else "040000"):
                raise ValueError("Candidate path is not a regular Git file/directory: " + part)


def verify_plan(plan):
    if plan.get("seal") != seal(plan) or plan.get("schema_version") != 1:
        raise ValueError("Candidate integrity changed; rebuild from official sources")
    if not re.fullmatch(r"[0-9a-f]{40}", plan["base_revision"]):
        raise ValueError("Invalid comparison revision")
    guard_inputs(plan["base_revision"])
    original = git("show", plan["base_revision"] + ":" + MANIFEST)
    group, sources = select_sources(json.loads(original), plan["sources"][0]["id"])
    if (plan["group"] != group or branch_group(plan["branch"])[0] != group
            or [s["configuration"] for s in plan["sources"]] != sources
            or [s["id"] for s in plan["sources"]] != [s["id"] for s in sources]
            or plan["service_prefixes"] != sorted({str(Path(s["target"]).parent.parent) + "/" for s in sources})):
        raise ValueError("Candidate source group/configuration differs from comparison tree")
    allowed = {s["destination"] for s in plan["sources"]} | {MANIFEST}
    if not plan["files"] or not set(plan["files"]) <= allowed:
        raise ValueError("Candidate has no changes or unexpected files")
    # Git must see ordinary directories and files, never a symlink or submodule
    # ancestor that could redirect a sparse path or erase unrelated tree content.
    guard_tree_paths(plan["base_revision"], allowed)
    for path, content in plan["files"].items():
        if path != MANIFEST:
            spec = update.parse(content.encode())
            if update.validate_document(spec) or update.serialize_document(spec) != content:
                raise ValueError("Candidate YAML failed validation/roundtrip")
    with tempfile.TemporaryDirectory() as directory:
        manifest = Path(directory) / "sources.json"
        manifest.write_bytes(original)
        for source, row in zip(sources, plan["sources"]):
            content = plan["files"].get(row["destination"])
            spec = update.parse(content.encode()) if content is not None else update.stored(row["destination"], plan["base_revision"])
            if spec is None or str(update.destination(source, spec)) != row["destination"]:
                raise ValueError("Candidate destination differs from declared vendor version")
            advance = update.advance_target(manifest, source, Path(row["destination"]))
            if advance:
                manifest.write_bytes(advance[1])
        expected = manifest.read_bytes()
    actual = plan["files"].get(MANIFEST, original.decode()).encode()
    if actual != expected:
        raise ValueError("Candidate manifest includes unrelated configuration changes")


def commit_plan(plan):
    verify_plan(plan)
    # A private temporary index keeps the full Git tree, without materializing
    # sparse API paths or altering the user's index, branch or working files.
    with tempfile.TemporaryDirectory() as directory:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(directory) / "index")}
        git("read-tree", plan["base_revision"], env=env)
        for path, content in plan["files"].items():
            blob = git("hash-object", "-w", "--stdin", data=content.encode()).decode().strip()
            git("update-index", "--add", "--cacheinfo", "100644," + blob + "," + path, env=env)
        tree = git("write-tree", env=env).decode().strip()
        changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", plan["base_revision"], tree).decode().splitlines()
        if set(changed) != set(plan["files"]):
            raise ValueError("Generated Git tree contains unexpected changes")
        message = "Update official " + plan["group"] + " API description\n\nCandidate SHA-256: " + plan["seal"] + "\n"
        return git("commit-tree", tree, "-p", plan["base_revision"], data=message.encode()).decode().strip()


def validate_commit(base, head, branch):
    """Offline CI validation of an explicitly generated single-API commit."""
    base = git("rev-parse", "--verify", base + "^{commit}").decode().strip()
    head = git("rev-parse", "--verify", head + "^{commit}").decode().strip()
    guard_inputs(base)
    parents = git("rev-list", "--parents", "-n", "1", head).decode().split()[1:]
    if parents != [base]:
        raise ValueError("Draft comparison base/head changed; rebuild or review the pending PR deliberately")
    original = git("show", base + ":" + MANIFEST)
    manifest = json.loads(original)
    group_name, _ = branch_group(branch)
    members = [s for s in manifest["sources"] if group_name is not None and group_name == s.get("publication_group", s["id"])]
    if not members:
        raise ValueError("Draft branch is not a configured publication group")
    group, sources = select_sources(manifest, members[0]["id"])
    changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", base, head).decode().splitlines()
    files = {path: git("show", head + ":" + path).decode() for path in changed}
    rows = []
    for source in sources:
        # Head may advance only the targets of this selected API; verify_plan
        # below reconstructs the exact allowed manifest edits from the base.
        head_manifest = json.loads(git("show", head + ":" + MANIFEST))
        entry = next(s for s in head_manifest["sources"] if s["id"] == source["id"])
        spec = update.stored(entry["target"], head)
        if spec is None or update.validate_document(spec):
            raise ValueError("Draft artifact is absent or fails complete native validation")
        destination = str(update.destination(source, spec))
        if destination != entry["target"]:
            raise ValueError("Draft target differs from vendor version")
        rows.append({"id": source["id"], "configuration": source, "destination": destination})
    plan = {"schema_version": 1, "group": group, "branch": branch, "base_revision": base,
            "sources": rows, "files": files,
            "service_prefixes": sorted({str(Path(s["target"]).parent.parent) + "/" for s in sources})}
    plan["seal"] = seal(plan)
    verify_plan(plan)
    guard_tree_paths(head, {s["destination"] for s in rows} | {MANIFEST})
    comparisons = []
    for source, row in zip(sources, rows):
        current = update.stored(row["destination"], head)
        _, previous = update.baseline(source, current, base)
        comparison = update.compare(previous, current)
        if previous is None:
            comparison.update(added_paths=sorted(current["paths"]), removed_paths=[],
                              added_operations=sorted(update.operation_set(current)), removed_operations=[])
        comparisons.append({"id": source["id"], "destination": row["destination"],
                            "origin": current["info"].get("x-origin"),
                            "conversion": current["info"].get("x-conversion"),
                            **comparison})
    return {"status": "draft_commit_validated", "base_revision": base, "head": head,
            "group": group, "files": sorted(files),
            "comparisons_from_main": comparisons,
            "note": "Offline native validation, typed YAML and exact tree/configuration scope; no fresh vendor comparison."}


def gh_json(endpoint, method="GET", payload=None):
    args = ["gh", "api", "--method", method, endpoint]
    if payload is not None:
        args += ["--input", "-"]
    return json.loads(command(args, json.dumps(payload).encode() if payload is not None else None))


def pages(endpoint, limit=10):
    separator = "&" if "?" in endpoint else "?"
    result = []
    for page in range(1, limit + 1):
        values = gh_json(endpoint + separator + "per_page=100&page=" + str(page))
        if not isinstance(values, list):
            raise ValueError("Invalid GitHub list response")
        result.extend(values)
        if len(values) < 100:
            return result
    raise ValueError("GitHub pagination exceeds review bounds; no publication")


def existing_pr(plan):
    matches = []
    for pr in pages("repos/" + REPOSITORY + "/pulls?state=open"):
        files = pages("repos/" + REPOSITORY + "/pulls/" + str(pr["number"]) + "/files", limit=30)
        # GitHub truncates PR files at 3000. A full page at the bound fails closed.
        if pr["head"]["ref"] == plan["branch"] or any(
                f["filename"].startswith(prefix) for f in files for prefix in plan["service_prefixes"]):
            matches.append({"number": pr["number"], "url": pr["html_url"], "head": pr["head"]["sha"]})
    return matches


def remote_guard(plan):
    for options in (("--all",), ("--push", "--all")):
        remotes = git("remote", "get-url", *options, "origin").decode().splitlines()
        if len(remotes) != 1 or not re.fullmatch(
                r"(?:https://github.com/|git@github.com:)(?:ontola|localthought)/openapi-directory(?:\.git)?", remotes[0]):
            raise ValueError("Publication is restricted to one unambiguous fetch/push origin for this fork")
    main = git("ls-remote", "--exit-code", "origin", "refs/heads/main").decode().split()
    if not main or main[0] != plan["base_revision"]:
        raise ValueError("Remote main advanced; fetch and rebuild before publication")


def remote_generations(group):
    """All remote generated branches of exactly this group: {generation: (branch, sha)}."""
    output = git("ls-remote", "origin", "refs/heads/" + BRANCH_PREFIX + group + "*").decode()
    found = {}
    for line in output.splitlines():
        sha, ref = line.split()
        name = ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else None
        found_group, generation = branch_group(name)
        if found_group == group:
            found[generation] = (name, sha)
    return found


def merged_outcome(plan, branch, sha):
    """Read-only checks that a generation is a verified merged generated outcome.

    Returns (verified, observation). Missing objects, foreign commits, squash or
    rebase merges, unmerged/closed PRs and moved tips are all unverified (held).
    """
    checks = {"branch": branch, "tip": sha}
    try:
        prs = [pr for pr in pages("repos/" + REPOSITORY + "/pulls?state=all&head="
                                  + urllib.parse.quote(REPOSITORY.split("/")[0] + ":" + branch, safe=""))
               if pr.get("head", {}).get("ref") == branch
               and pr.get("head", {}).get("repo", {}).get("full_name") == REPOSITORY]
        checks["pull_requests"] = [pr.get("number") for pr in prs]
        if len(prs) != 1:
            return False, {**checks, "reason": "Exactly one PR must exist for the branch"}
        pr = prs[0]
        checks.update(number=pr.get("number"), merge_commit=pr.get("merge_commit_sha"), merged_at=pr.get("merged_at"))
        if pr.get("state") != "closed" or not pr.get("merged_at"):
            return False, {**checks, "reason": "PR is open or closed without merging"}
        if pr.get("head", {}).get("sha") != sha:
            return False, {**checks, "reason": "Branch tip moved after the PR"}
        git("cat-file", "-e", sha + "^{commit}")
        try:
            git("merge-base", "--is-ancestor", sha, plan["base_revision"])
        except subprocess.CalledProcessError:
            return False, {**checks, "reason": "Head is not in main history (squash/rebase merge or unmerged)"}
        parents = git("rev-list", "--parents", "-n", "1", sha).decode().split()[1:]
        if len(parents) != 1:
            return False, {**checks, "reason": "Generated commit must have exactly one parent"}
        message = git("show", "-s", "--format=%B", sha).decode()
        if not re.fullmatch(r"Update official " + re.escape(plan["group"])
                            + r" API description\n\nCandidate SHA-256: [0-9a-f]{64}\n*", message):
            return False, {**checks, "reason": "Commit message is not a generated candidate"}
        changed = git("diff-tree", "--no-commit-id", "--name-only", "-r", parents[0], sha).decode().splitlines()
        if not changed or any(path != MANIFEST and not any(path.startswith(prefix) for prefix in plan["service_prefixes"])
                              for path in changed):
            return False, {**checks, "reason": "Generated commit touches files outside this API"}
    except subprocess.CalledProcessError:
        return False, {**checks, "reason": "Required Git objects or ancestry are unavailable"}
    return True, {**checks, "verified": True}


def next_generation(plan, cache):
    """Choose the branch for a new draft without deleting or reusing any branch.

    Returns the plan unchanged when generation 1 is absent or when any existing
    generation is not a verified merged outcome (publish() then holds as before).
    Otherwise returns a resealed plan for the lowest unused generation and records
    an immutable retirement observation for each verified merged generation.
    """
    group = plan["group"]
    existing = remote_generations(group)
    if 1 not in existing:
        return plan
    observations = []
    for generation, (branch, sha) in sorted(existing.items()):
        verified, observation = merged_outcome(plan, branch, sha)
        if not verified:
            return plan
        observations.append((generation, observation))
    generation = next(n for n in range(2, 1000) if n not in existing)
    directory = cache / "publication" / group / "retired"
    if directory.is_symlink() or directory.parent.is_symlink():
        raise ValueError("Redirected publication guard directory")
    directory.mkdir(parents=True, exist_ok=True)
    for number, observation in observations:
        path = directory / ("g" + str(number) + ".json")
        record = {"kind": "merged_generation_observation", "not_a_creation_receipt": True,
                  "group": group, "generation": number, **observation}
        if path.exists() or path.is_symlink():
            old = json.loads(path.read_text())
            if {k: old.get(k) for k in ("branch", "tip", "number")} != {k: record.get(k) for k in ("branch", "tip", "number")}:
                raise ValueError("Retained retirement observation differs; deliberate review required")
            continue
        path.write_text(json.dumps({**record, "observed_at": update.now()}, indent=2) + "\n")
    return with_branch(plan, branch_name(group, generation))


def pr_body(plan):
    lines = ["Validated official-source update for " + plan["group"] + ".", "",
             "Draft for deliberate per-API review; no automatic merge. Comparison base: " + plan["base_revision"] + "."]
    if plan.get("publication_protocol") == 2:
        lines += ["", "Initial submission snapshot. This text is retained if the generated draft is refreshed. "
                  "Review the latest head/diff and its Generated API draft validation summary for current versions, "
                  "changes and provenance; the snapshot below describes the original submission."]
    for source in plan["sources"]:
        metadata, comparison = source["fetch"], source["comparison"]
        lines += ["", "Source " + source["id"] + ": [official artifact](" + metadata["url"] + ").",
                  "Entry SHA-256: " + metadata["sha256"] + ". Revision: " + str(metadata.get("revision") or "hosted source; see fetch date") + ".",
                  "Stored/source statistics: " + json.dumps({k: v for k, v in comparison.items() if k in {"stored", "source", "status"}}, sort_keys=True) + ".",
                  "Scope: " + source["configuration"].get("coverage", source["configuration"].get("discovery", "See reviewed source manifest."))]
        for field in ("added_paths", "removed_paths", "added_operations", "removed_operations"):
            values = comparison.get(field, [])
            lines += [field.replace("_", " ") + ": " + str(len(values)) + "."]
            lines += ["- " + item for item in values[:50]]
            if len(values) > 50:
                lines += ["Remaining entries are in the candidate report and full PR diff."]
        lines += metadata.get("transformations", []) or ["No bundling, conversion, or API content patches."]
        lines += ["Validation: " + update.VALIDATION_DESCRIPTION + "; serialized typed roundtrip and complete curated vendor comparison passed."]
        if source["health"]["source_health"] == "not_assessed":
            lines += ["Hosted repository health is not assessed; no repository identity/freshness claim."]
    lines += ["", "Changed files:"] + ["- " + path for path in sorted(plan["files"])]
    body = "\n".join(lines) + "\n"
    if len(body.encode()) > 60000:
        raise ValueError("Review body is too large; prepare a manual PR")
    return body


def publish(plan, cache):
    verify_plan(plan)
    directory = cache / "publication" / plan["group"]
    directory.mkdir(parents=True, exist_ok=True)
    blocked = directory / "blocked.json"
    lock = directory / "publishing.lock"
    try:
        with lock.open("x") as handle:
            handle.write(plan["seal"] + "\n")
    except FileExistsError:
        raise ValueError("Publication already running or interrupted; review retained lock before retrying") from None
    try:
        if blocked.exists() or blocked.is_symlink():
            raise ValueError("A previous publication failed; retain evidence and require deliberate review before retrying")
        return publish_locked(plan, blocked)
    finally:
        lock.unlink()


def verify_pr_identity(pr, plan, commit):
    number = pr.get("number")
    if (not isinstance(number, int) or isinstance(number, bool) or number < 1
            or pr.get("html_url") != "https://github.com/" + REPOSITORY + "/pull/" + str(number)
            or pr.get("draft") is not True or pr.get("state") != "open"
            or pr.get("head", {}).get("sha") != commit
            or pr.get("head", {}).get("ref") != plan["branch"]
            or pr.get("base", {}).get("ref") != "main"
            or pr.get("base", {}).get("sha") != plan["base_revision"]
            or any(pr.get(side, {}).get("repo", {}).get("full_name") != REPOSITORY for side in ("head", "base"))):
        raise ValueError("Unexpected created PR identity/state; inspect before further actions")


def verify_created_pr(pr, plan, commit):
    verify_pr_identity(pr, plan, commit)
    number = pr["number"]
    files = pages("repos/" + REPOSITORY + "/pulls/" + str(number) + "/files", limit=30)
    if len(files) != len(plan["files"]) or {f["filename"] for f in files} != set(plan["files"]):
        raise ValueError("Created PR file list differs from validated candidate")
    # The branch/base may have changed while paginating. Only the exact head/base
    # and still-draft PR count as a verified publication result.
    current = gh_json("repos/" + REPOSITORY + "/pulls/" + str(number))
    verify_pr_identity(current, plan, commit)


def publish_locked(plan, blocked):
    remote_guard(plan)
    pending = existing_pr(plan)
    if pending:
        return {"status": "existing_pending", "pull_requests": pending,
                "note": "Review/update existing PRs; no new branch, overwrite, comment or duplicate PR."}
    branch_ref = "refs/heads/" + plan["branch"]
    _, generation = branch_group(plan["branch"])
    if generation is None:
        raise ValueError("Unexpected generated branch name")
    if generation > 1:
        # Re-verify every existing generation under the lock; never trust an
        # earlier observation if a branch or PR changed in between.
        existing = remote_generations(plan["group"])
        if 1 not in existing or any(not merged_outcome(plan, branch, sha)[0]
                                    for number, (branch, sha) in existing.items() if number != generation):
            return {"status": "existing_branch", "branch": plan["branch"],
                    "note": "An earlier generation is not a verified merged outcome; investigate manually."}
    if git("ls-remote", "origin", branch_ref).strip():
        return {"status": "existing_branch", "branch": plan["branch"],
                "note": "Existing branch retained; investigate/recover prior outcome manually."}
    body = pr_body(plan)
    commit = commit_plan(plan)
    remote_guard(plan)
    stage = "push"
    pr = None
    try:
        # Empty expected ref means CREATE ONLY, even if someone creates the
        # branch after our read. No existing remote commit can be replaced.
        git("push", "--porcelain", "--force-with-lease=" + branch_ref + ":", "origin", commit + ":" + branch_ref)
        stage = "post_push_base_check"
        remote_guard(plan)
        stage = "create_pull_request"
        pr = gh_json("repos/" + REPOSITORY + "/pulls", "POST", {
            "title": "Update official " + plan["group"] + " API", "body": body,
            "head": plan["branch"], "base": "main", "draft": True})
        stage = "verify_pull_request"
        verify_created_pr(pr, plan, commit)
        return {"status": "draft_created", "url": pr["html_url"], "number": pr["number"], "head": commit}
    except Exception as error:
        # Preserve unknown outcomes too. Never retry/redact/unblock a rejected
        # push or duplicate a PR after a POST timeout. Do not echo vendor examples.
        receipt = {"stage": stage, "candidate_sha256": plan["seal"],
                   "branch": plan["branch"], "head": commit,
                   "recorded_at": update.now(), "error_type": type(error).__name__,
                   "created_url": pr.get("html_url") if isinstance(pr, dict) else None}
        blocked.write_text(json.dumps(receipt, indent=2) + "\n")
        raise PublicationFailure(receipt) from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--source", help="One reviewed API ID; explicit groups include all companion artifacts")
    selection.add_argument("--validate-head", help="Offline CI validation of a generated draft commit")
    parser.add_argument("--branch", help="Exact generated draft branch, required with --validate-head")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--cache", type=Path, default=update.ROOT / "cache/maintenance/drafts")
    parser.add_argument("--publish", action="store_true", help="Explicitly create a new draft; no merge or existing-branch update")
    args = parser.parse_args(argv)
    if args.validate_head:
        if not args.branch or args.publish:
            parser.error("--validate-head requires --branch and forbids --publish")
        result = validate_commit(args.base, args.validate_head, args.branch)
        print(json.dumps(result, indent=2))
        return 0
    if args.branch:
        parser.error("--branch is only used for offline draft validation")
    args.cache.mkdir(parents=True, exist_ok=True)
    try:
        plan = build_plan(args.source, args.base, args.cache)
        result = run_plan(plan, args)
    except Exception as error:
        # Raw vendor examples/subprocess output never enter terminal diagnostics.
        result = {"status": "failed", "source": args.source, "stage": "plan_or_publish",
                  "error_type": type(error).__name__, "attempted_at": update.now(),
                  "note": "Review cached sources/candidate and publication guard; do not automatically retry."}
        if isinstance(error, PublicationFailure):
            result["stage"] = error.receipt["stage"]
            url = error.receipt.get("created_url")
            if isinstance(url, str) and re.fullmatch(r"https://github.com/ontola/openapi-directory/pull/[1-9][0-9]*", url):
                result["created_url"] = url  # Caller must attach even when verification fails.
        (args.cache / "failure.json").write_text(json.dumps({**result, "diagnostic": str(error)}, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "failed" else 0


def run_plan(plan, args):
    # Candidate directories identify an immutable attempt, so a later no-op does
    # not leave an earlier body alongside a report claiming the current source.
    if args.publish and plan["files"]:
        plan = next_generation(plan, args.cache)
    directory = args.cache / plan["group"] / plan["seal"]
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "candidate.json").write_text(json.dumps(plan, indent=2) + "\n")
    if plan["files"]:
        (directory / "body.md").write_text(pr_body(plan))
    result = {"status": plan["status"], "group": plan["group"], "base_revision": plan["base_revision"],
              "files": sorted(plan["files"]), "candidate_sha256": plan["seal"]}
    if args.publish and plan["files"]:
        result.update(publish(plan, args.cache))
    (directory / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.cache / "latest-result.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
