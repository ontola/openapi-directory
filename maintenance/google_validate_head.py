#!/usr/bin/env python3
"""Read-only validation of actual changed Google artifacts at an exact Git head.

Run this from trusted base tooling. Generated artifacts must exactly match
their pinned official source plus preserved base curation. Legacy artifacts
receive full OAS validation with that narrower result labelled explicitly.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request

from openapi_spec_validator import validate
import yaml

import google_refresh as refresh

SOURCE = re.compile(r"https://raw\.githubusercontent\.com/googleapis/discovery-artifact-manager/([0-9a-f]{40})/(discoveries/[A-Za-z0-9._-]+\.json)")
PROFILE = "Converted the official Google Discovery v1 document to OpenAPI 3.0.3 with maintenance/google_discovery.py (conversion profile 1)."


def source_of(document):
    steps = document.get("info", {}).get("x-conversion", [])
    if not steps or steps[0] != PROFILE:
        return None
    origins = document["info"].get("x-origin", [])
    if not origins or origins[0].get("format") != "google":
        raise ValueError("Missing official Discovery source")
    match = SOURCE.fullmatch(origins[0].get("url", ""))
    if not match:
        raise ValueError("Source must pin the official Google repository by full SHA")
    digest = re.search(r"original source SHA-256 ([0-9a-f]{64})\.", steps[1] if len(steps) > 1 else "")
    if not digest:
        raise ValueError("Missing original source hash")
    return origins[0]["url"], match[1], match[2], digest[1]


def original(repository, revision, path):
    result = subprocess.run(["git", "-C", str(repository), "show", revision + ":" + path], capture_output=True)
    if result.returncode:
        exists = subprocess.run(["git", "-C", str(repository), "cat-file", "-e", revision], capture_output=True)
        if exists.returncode:
            raise ValueError("Git revision is unavailable")
        return None
    return result.stdout


def artifact(task):
    repository, base, head, path, cache = task
    row = {"path": path}
    try:
        raw = original(repository, head, path)
        if raw is None:
            raise ValueError("Removing a Google artifact needs a separate reviewed change")
        document = yaml.load(raw, Loader=refresh.LOADER)
        source = source_of(document)
        if source is None:
            validate(document)
            return {**row, "status": "valid", "mode": "legacy-oas-only"}
        url, revision, source_path, digest = source
        cache = Path(cache)
        source_file = cache / "sources" / (digest + ".json")
        if not source_file.exists():
            with urllib.request.urlopen(url, timeout=60) as response:
                native_raw = response.read(64 * 1024 * 1024 + 1)
            if len(native_raw) > 64 * 1024 * 1024:
                raise ValueError("Discovery source exceeds validation bound")
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_file.write_bytes(native_raw)
        native_raw = source_file.read_bytes()
        if hashlib.sha256(native_raw).hexdigest() != digest:
            raise ValueError("Pinned source hash mismatch")
        native = json.loads(native_raw)
        if path != "APIs/googleapis.com/" + native["name"] + "/" + native["version"] + "/openapi.yaml":
            raise ValueError("Artifact service/version differs from its official source")
        before = original(repository, base, path)
        reviewed = refresh.candidate((str(source_file), revision, source_path, path, before, str(cache / "candidates")))
        if "candidate" not in reviewed:
            raise ValueError("Source projection failed: " + reviewed.get("error", reviewed["status"]))
        expected = yaml.load(Path(reviewed["candidate"]).read_bytes(), Loader=refresh.LOADER)
        if not refresh.typed_equal(expected, document):
            raise ValueError("Artifact does not exactly match its source/conversion/base curation")
        return {**row, "status": "valid", "mode": "native-projection", "source_sha256": digest,
                "source_revision": revision, "artifact_sha256": hashlib.sha256(raw).hexdigest(),
                **{key: reviewed[key] for key in ("operations", "schemas", "references")}}
    except Exception as error:
        return {**row, "status": "invalid", "error": type(error).__name__ + ": " + str(error)[:2000]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--cache", type=Path, default=Path("cache/maintenance/google-head-validation"))
    args = parser.parse_args()
    if any(not re.fullmatch(r"[0-9a-f]{40}", value) for value in (args.base, args.head)):
        parser.error("Require exact full Git SHAs")
    repository = Path.cwd()
    paths = refresh.git(repository, "diff", "--name-only", args.base, args.head, "--", "APIs/googleapis.com").decode().splitlines()
    if any(not path.endswith(("/openapi.yaml", "/swagger.yaml")) for path in paths):
        raise SystemExit("Unexpected file in the Google API diff")
    rows = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        tasks = [(repository, args.base, args.head, path, args.cache) for path in paths]
        for index, future in enumerate(concurrent.futures.as_completed([pool.submit(artifact, task) for task in tasks]), 1):
            row = future.result()
            rows.append(row)
            if row["status"] != "valid" or index % 25 == 0:
                print(json.dumps({"completed": index, "total": len(paths), **row}), flush=True)
    rows.sort(key=lambda row: row["path"])
    result = {"base": args.base, "head": args.head, "files": len(rows),
              "valid": sum(row["status"] == "valid" for row in rows),
              "native_projection": sum(row.get("mode") == "native-projection" for row in rows),
              "legacy_oas_only": sum(row.get("mode") == "legacy-oas-only" for row in rows), "artifacts": rows}
    args.cache.mkdir(parents=True, exist_ok=True)
    (args.cache / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "artifacts"}), flush=True)
    return 0 if result["valid"] == result["files"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
