#!/usr/bin/env python3
"""Review or locally import all descriptions in a pinned official Discovery checkout.

No network, Git commits, pushes, PRs, schedules, or provider-data requests.
Absent historical versions are retained. Each import must pass complete OAS,
reference/inventory, and typed YAML checks before replacing its own file.
"""
import argparse
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from openapi_spec_validator import validate
import yaml

import google_discovery as google
import google_compatibility

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
OFFICIAL = "https://github.com/googleapis/discovery-artifact-manager"
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def git(directory, *arguments):
    return subprocess.check_output(["git", "-C", str(directory), *arguments])


def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(typed_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def preserve_curation(old, converted):
    result = copy.deepcopy(converted)
    if not old:
        return result
    result["info"] = {**copy.deepcopy(old["info"]), **result["info"]}
    result["info"]["contact"] = {**copy.deepcopy(old["info"].get("contact", {})), **result["info"].get("contact", {})}
    for key in ("externalDocs", "tags", "x-hasEquivalentPaths"):
        if key in old:
            result[key] = copy.deepcopy(old[key])
    return result


def check_curation(old, document):
    """Verify curation separately from the merge that is meant to retain it."""
    if not old:
        return
    for key in ("externalDocs", "tags", "x-hasEquivalentPaths"):
        if key in old and (key not in document or not typed_equal(old[key], document[key])):
            raise ValueError("Existing root curation changed: " + key)
    for key, value in old.get("info", {}).items():
        if key.startswith("x-") and key not in {"x-origin", "x-conversion"}:
            if key not in document["info"] or not typed_equal(value, document["info"][key]):
                raise ValueError("Existing info curation changed: " + key)
    for key, value in old.get("info", {}).get("contact", {}).items():
        if key.startswith("x-") and not typed_equal(value, document["info"].get("contact", {}).get(key)):
            raise ValueError("Existing contact curation changed: " + key)


def revision_of(document):
    revision = document.get("x-google-discovery", {}).get("revision", "")
    if re.fullmatch(r"\d{8}", revision):
        return revision
    for step in document.get("info", {}).get("x-conversion", []):
        match = re.search(r"(?:Discovery document, revision|Discovery revision) (\d{8})", step)
        if match:
            return match[1]
    return None


def inventory(document):
    return {operation["operationId"] for item in document.get("paths", {}).values()
            for method, operation in item.items() if method in google.METHODS and "operationId" in operation}


def candidate(task):
    source_file, source_revision, source_path, target, original, cache = task[:6]
    source_blob = task[6] if len(task) > 6 else None
    row = {"source": source_path, "target": target, "source_repository_revision": source_revision}
    try:
        raw = Path(source_file).read_bytes()
        if source_blob is not None:
            object_bytes = b"blob " + str(len(raw)).encode() + b"\0" + raw
            if hashlib.sha1(object_bytes, usedforsecurity=False).hexdigest() != source_blob:
                raise ValueError("Source bytes do not match the pinned Git blob")
        native = json.loads(raw)
        row.update(service=native["name"], version=native["version"],
                   discovery_revision=native.get("revision"), source_sha256=hashlib.sha256(raw).hexdigest())
        old = yaml.load(original, Loader=LOADER) if original else None
        previous_revision = revision_of(old or {})
        if previous_revision and native.get("revision", "") < previous_revision:
            return {**row, "status": "retained_newer", "existing_discovery_revision": previous_revision}
        reviewed, compatibility = google_compatibility.prepare(native)
        document = google.convert(reviewed)
        stats = google.check(reviewed, document)
        converted = preserve_curation(old, document)
        source_url = OFFICIAL.replace("github.com", "raw.githubusercontent.com") + "/" + source_revision + "/" + source_path
        converted["info"]["x-origin"] = [
            {"format": "google", "url": source_url, "version": "v1"},
            {"format": "openapi", "url": source_url, "version": "3.0"},
        ]
        converted["info"]["x-conversion"] = [
            "Converted the official Google Discovery v1 document to OpenAPI 3.0.3 with maintenance/google_discovery.py (conversion profile 1).",
            "Source repository revision " + source_revision + "; Discovery revision " + native.get("revision", "unspecified") + "; original source SHA-256 " + row["source_sha256"] + ".",
            "Used Google's flatPath to disambiguate methods sharing reserved resource-name paths. Original paths, complete resource-name parameter patterns/bindings and singleton constants remain in x-google-discovery metadata.",
            "Preserved schema and parameter constraints, exact integer bounds, reference siblings via allOf, and all native methods and schemas. Enum descriptions/deprecation and method-specific required annotations remain explicit x-google-* metadata, not global required constraints.",
            "OAuth flows and accepted scopes are alternatives. Authorization endpoints follow Google's OAuth documentation. Discovery supplies no success status code, so responses use the OpenAPI 2XX range.",
            "JSON requests/responses and binary downloads are represented directly. Upload protocols, streaming/subscription details, regional/mTLS metadata and other Discovery-only annotations remain explicit extensions; no upload endpoint or protocol implementation is invented.",
            "Preserved existing APIs.guru info/contact curation, externalDocs and tags when refreshing an existing version. Full OpenAPI validation, native inventories, all local references and typed YAML roundtrip passed. This is a description refresh, not live API/account compatibility verification.",
        ]
        converted["info"]["x-conversion"].extend(compatibility)
        check_curation(old, converted)
        validate(converted)
        text = yaml.dump(converted, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=100000)
        parsed = yaml.load(text, Loader=LOADER)
        if not typed_equal(converted, parsed):
            raise ValueError("Typed YAML roundtrip changed the generated document")
        # Never rewrite an otherwise identical description just for source provenance.
        def content(value):
            result = copy.deepcopy(value)
            for key in ("x-origin", "x-conversion"):
                result.get("info", {}).pop(key, None)
            return result
        status = "added" if old is None else "unchanged" if typed_equal(content(old), content(converted)) else "refreshed"
        rendered = text.encode()
        candidate_path = Path(cache) / row["source_sha256"] / "openapi.yaml"
        candidate_path.parent.mkdir(parents=True, exist_ok=True)
        candidate_path.write_bytes(rendered)
        current_ids = inventory(converted)
        old_ids = inventory(old or {})
        old_schemas = set((old or {}).get("components", {}).get("schemas", {}))
        row.update(status=status, **stats, compatibility=compatibility, candidate=str(candidate_path),
                   candidate_sha256=hashlib.sha256(rendered).hexdigest(),
                   baseline_sha256=hashlib.sha256(original).hexdigest() if original else None,
                   added_operation_ids=sorted(current_ids - old_ids), removed_operation_ids=sorted(old_ids - current_ids),
                   added_schema_names=sorted(set(native["schemas"]) - old_schemas),
                   removed_schema_names=sorted(old_schemas - set(native["schemas"])))
        return row
    except Exception as error:
        return {**row, "status": "blocked", "error": type(error).__name__ + ": " + str(error)[:4000]}


def apply(rows, repository):
    for row in rows:
        if row["status"] not in {"added", "refreshed"}:
            continue
        target = repository / row["target"]
        raw = Path(row["candidate"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["candidate_sha256"]:
            raise ValueError("Candidate changed after validation")
        existing = target.read_bytes() if target.exists() else None
        actual = hashlib.sha256(existing).hexdigest() if existing is not None else None
        if actual != row["baseline_sha256"] and existing != raw:
            raise ValueError("Refusing to overwrite a working-tree edit: " + row["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=".google-discovery-", dir=target.parent)
        try:
            with os.fdopen(descriptor, "wb") as output:
                output.write(raw)
            os.chmod(name, 0o644)
            os.replace(name, target)
        finally:
            if os.path.exists(name):
                os.unlink(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-checkout", required=True, type=Path)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--cache", type=Path, default=REPOSITORY / "cache/maintenance/google-discovery")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--only", action="append", help="Optional service name; repeated for a bounded pilot")
    parser.add_argument("--write", action="store_true", help="Write validated candidates locally; default is review only")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_revision) or not 1 <= args.workers <= 8:
        parser.error("Require a full source SHA and 1–8 workers")
    source_root = args.source_checkout.resolve()
    if git(source_root, "rev-parse", "HEAD").decode().strip() != args.source_revision:
        raise SystemExit("Source checkout is not at the reviewed revision")
    remote = git(source_root, "remote", "get-url", "origin").decode().strip().removesuffix(".git")
    if remote != OFFICIAL or git(source_root, "status", "--porcelain", "--", "discoveries").strip():
        raise SystemExit("Require an unmodified official Google Discovery checkout")
    source_blobs = {}
    for line in git(source_root, "ls-tree", "-r", "HEAD", "--", "discoveries").decode().splitlines():
        header, path = line.split("\t", 1)
        source_blobs[path] = header.split()[2]
    baseline = git(REPOSITORY, "rev-parse", "HEAD").decode().strip()
    original_paths = git(REPOSITORY, "ls-tree", "-r", "--name-only", "HEAD", "--", "APIs/googleapis.com").decode().splitlines()
    originals = {path: git(REPOSITORY, "show", "HEAD:" + path) for path in original_paths if path.endswith(("openapi.yaml", "swagger.yaml"))}
    tasks, seen = [], set()
    selected = set(args.only or [])
    for source in sorted((source_root / "discoveries").glob("*.json")):
        native = json.loads(source.read_bytes())
        if "name" not in native:
            continue  # index.json is a Discovery directory, not an API.
        service, version = native["name"], native["version"]
        if selected and service not in selected:
            continue
        if not LABEL.fullmatch(service) or not LABEL.fullmatch(version):
            raise SystemExit("Unsafe service/version path")
        target = "APIs/googleapis.com/" + service + "/" + version + "/openapi.yaml"
        if target in seen:
            raise SystemExit("Duplicate source service/version")
        seen.add(target)
        tasks.append((str(source), args.source_revision, source.relative_to(source_root).as_posix(), target,
                      originals.get(target), str(args.cache.resolve()), source_blobs[source.relative_to(source_root).as_posix()]))
    rows = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(candidate, task) for task in tasks]
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            row = future.result()
            rows.append(row)
            if row["status"] == "blocked" or index % 25 == 0:
                print(json.dumps({"completed": index, "total": len(tasks), "target": row["target"], "status": row["status"],
                                  **({"error": row["error"][:300]} if "error" in row else {})}), flush=True)
    for path in sorted(originals.keys() - seen):
        if not selected or path.split("/")[2] in selected:
            rows.append({"target": path, "status": "source_unavailable", "action": "retain existing version; absent from this official mirror snapshot"})
    index_file = source_root / "discoveries/index.json"
    indexed_missing = []
    if index_file.exists():
        for item in json.loads(index_file.read_bytes())["items"]:
            if selected and item["name"] not in selected:
                continue
            target = "APIs/googleapis.com/" + item["name"] + "/" + item["version"] + "/openapi.yaml"
            if target not in seen:
                indexed_missing.append({"id": item["id"], "discovery_url": item["discoveryRestUrl"], "existing": target in originals})
    rows.sort(key=lambda row: row["target"])
    counts = {status: sum(row["status"] == status for row in rows) for status in sorted({row["status"] for row in rows})}
    report = {"baseline": baseline, "source_repository": OFFICIAL, "source_revision": args.source_revision,
              "source_index_sha256": hashlib.sha256(index_file.read_bytes()).hexdigest() if index_file.exists() else None,
              "conversion_profile": 1, "live_google_verification": False, "write_requested": args.write,
              "counts": counts, "indexed_without_source": indexed_missing, "artifacts": rows}
    report_path = args.report or args.cache / "report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    if args.write:
        if git(REPOSITORY, "rev-parse", "HEAD").decode().strip() != baseline:
            raise SystemExit("Repository HEAD changed during review; nothing applied")
        apply(rows, REPOSITORY)
    print(json.dumps({"counts": counts, "indexed_without_source": len(indexed_missing), "report": str(report_path)}), flush=True)
    return 1 if counts.get("blocked") else 0


if __name__ == "__main__":
    raise SystemExit(main())
