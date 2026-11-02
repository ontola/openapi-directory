#!/usr/bin/env python3
"""Read-only validation and comparison of native GraphQL artifacts.

No endpoint introspection, credentials, imports, or publication are performed.
SDL ASTs retain applied directives, which standard introspection cannot preserve.
"""
import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from graphql import (GraphQLError, build_client_schema, build_schema, introspection_from_schema,
                     lexicographic_sort_schema, parse, validate_schema)
from graphql.utilities import ast_to_dict

PROFILE = "graphql-core 3.3.1 (native SDL/introspection; no assumed-valid schemas)"


def inspect(raw, format):
    if version("graphql-core") != "3.3.1":
        raise ValueError("Install the pinned graphql-core 3.3.1 validator")
    ast = None
    if format == "sdl":
        text = raw.decode("utf-8-sig")
        document = parse(text)
        if any(node.kind in {"operation_definition", "fragment_definition"} for node in document.definitions):
            raise ValueError("Expected a native schema, not an executable saved query")
        ast = ast_to_dict(document, locations=False)
        schema = build_schema(text)
    elif format == "introspection":
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError("Introspection must be an object")
        if value.get("errors"):
            raise ValueError("Introspection response contains errors")
        data = value.get("data", value)
        if not isinstance(data, dict) or not isinstance(data.get("__schema"), dict):
            raise ValueError("Expected complete __schema introspection, not a query projection")
        schema = build_client_schema(data)
    else:
        raise ValueError("Format must be sdl or introspection")
    errors = [error.message for error in validate_schema(schema)]
    # Invalid upstream schemas are reported, never repaired or called current.
    semantic = None if errors else introspection_from_schema(lexicographic_sort_schema(schema))
    types = {name: value for name, value in schema.type_map.items() if not name.startswith("__")}
    fields = sum(len(getattr(value, "fields", {})) for value in types.values())
    return {"sha256": hashlib.sha256(raw).hexdigest(), "format": format,
            "validation_profile": PROFILE, "validation_errors": errors,
            "counts": {"types": len(types), "fields": fields, "directives": len(schema.directives)},
            "roots": {name: getattr(getattr(schema, name + "_type"), "name", None)
                      for name in ("query", "mutation", "subscription")},
            "semantic": semantic, "sdl_ast": ast}


def semantic_changes(old, new, path="#"):
    """Report changed schema locations without dumping source descriptions/data."""
    def named(value):
        if isinstance(value, list) and value and all(isinstance(x, dict) and isinstance(x.get("name"), str) for x in value):
            return {x["name"]: x for x in value}
        return value
    old, new = named(old), named(new)
    if old == new:
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        changes = []
        for key in sorted(set(old) | set(new)):
            child = path + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in old:
                changes.append({"kind": "added", "path": child})
            elif key not in new:
                changes.append({"kind": "removed", "path": child})
            else:
                changes.extend(semantic_changes(old[key], new[key], child))
        return changes
    return [{"kind": "changed", "path": path}]


def compare(old, new):
    if old["validation_errors"] or new["validation_errors"]:
        return {"status": "validation_blocked", "complete": False}
    same = old["semantic"] == new["semantic"]
    # SDL-only information (applied directives, extension structure) must not
    # disappear behind equivalent introspection. Ordering changes are conservative
    # review findings; no claim of a breaking change is inferred from them.
    ast_equal = old["sdl_ast"] == new["sdl_ast"] if old["sdl_ast"] is not None and new["sdl_ast"] is not None else None
    return {"status": "matches_source" if same and ast_equal is not False else "changed",
            "complete": ast_equal is not None, "introspection_equal": same,
            "sdl_ast_equal": ast_equal,
            "semantic_changes": semantic_changes(old["semantic"], new["semantic"]),
            "limitation": None if ast_equal is not None else
            "Introspection cannot establish applied directives or full SDL equality"}


def summary(result):
    return {key: value for key, value in result.items() if key not in {"semantic", "sdl_ast"}}


def verify_index(root, index):
    errors, artifacts = [], []
    root = root.resolve()
    for item in index["artifacts"]:
        paths = [(root / item[key]).resolve() for key in ("path", "provenance")]
        if any(root not in path.parents for path in paths):
            raise ValueError("Artifact path escapes repository")
        artifact, provenance_path = paths
        provenance = json.loads(provenance_path.read_text())
        result = summary(inspect(artifact.read_bytes(), provenance["format"]))
        if result["sha256"] != item["sha256"] or result["sha256"] != provenance["sha256"]:
            errors.append(item["path"] + ": source hash mismatch")
        if result != provenance["validation"]:
            errors.append(item["path"] + ": validation profile, counts, roots or errors differ from provenance")
        if result["validation_errors"] and (item["status"] != "validation_blocked" or provenance["status"] != "validation_blocked"):
            errors.append(item["path"] + ": invalid source must be explicitly blocked")
        artifacts.append({"path": item["path"], "status": item["status"],
                          "native_validation_errors": result["validation_errors"]})
    return {"snapshot_integrity_errors": errors, "artifacts": artifacts,
            "scope": "Retained snapshot integrity and recorded validation, not live freshness or endpoint health"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, nargs="?")
    parser.add_argument("--verify-index", type=Path)
    parser.add_argument("--format", choices=("sdl", "introspection"), default="sdl")
    parser.add_argument("--upstream", type=Path)
    parser.add_argument("--upstream-format", choices=("sdl", "introspection"), default="sdl")
    args = parser.parse_args(argv)
    try:
        if args.verify_index:
            if args.artifact or args.upstream:
                parser.error("--verify-index cannot be combined with artifact comparison")
            result = verify_index(Path(__file__).resolve().parents[1], json.loads(args.verify_index.read_text()))
            print(json.dumps(result, indent=2))
            return 1 if result["snapshot_integrity_errors"] else 0
        if not args.artifact:
            parser.error("artifact or --verify-index is required")
        local = inspect(args.artifact.read_bytes(), args.format)
        result = {"local": summary(local)}
        invalid = bool(local["validation_errors"])
        if args.upstream:
            upstream = inspect(args.upstream.read_bytes(), args.upstream_format)
            result.update(upstream=summary(upstream), comparison=compare(local, upstream))
            invalid |= bool(upstream["validation_errors"])
        print(json.dumps(result, indent=2))
        return 1 if invalid else 0
    except (OSError, ValueError, TypeError, GraphQLError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
