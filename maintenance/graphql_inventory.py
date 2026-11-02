#!/usr/bin/env python3
"""Inventory committed native GraphQL schemas and OpenAPI mentions at a Git ref."""
import argparse
import json
import subprocess
from pathlib import Path

from update import parse


def inventory(base, root):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root)

    revision = git("rev-parse", "--verify", base + "^{commit}").decode().strip()
    paths = git("ls-tree", "-r", "--name-only", revision).decode().splitlines()
    native = [p for p in paths if p.endswith((".graphql", ".gql"))]
    # Search committed content, including files outside sparse checkouts.
    found = subprocess.run(["git", "grep", "-l", "-i", "-e", "graphql", "-e", '"__schema"',
                            revision, "--", "APIs", "GraphQL"], cwd=root, capture_output=True)
    if found.returncode not in (0, 1):
        raise RuntimeError("Git inventory search failed: " + found.stderr.decode())
    mentions, failures, introspection = [], [], []
    for entry in found.stdout.decode().splitlines():
        path = entry.split(":", 1)[1]
        if path.endswith((".graphql", ".gql")):
            continue
        raw = git("show", revision + ":" + path)
        if path.endswith(".json"):
            try:
                value = json.loads(raw)
                if isinstance(value, dict) and ("__schema" in value or
                        isinstance(value.get("data"), dict) and "__schema" in value["data"]):
                    introspection.append(path)
                    continue
            except ValueError:
                pass
        if not path.startswith("APIs/") or not path.endswith((".yaml", ".json")):
            continue
        try:
            spec = parse(raw)
            routes = [p for p in spec["paths"] if "graphql" in p.lower()]
            mentions.append({"path": path, "graphql_routes": routes,
                             "classification": "endpoint_wrapper" if routes else "text_mention",
                             "native_schema": False})
        except Exception as error:
            failures.append({"path": path, "error": str(error)[:500]})
    return {"base_revision": revision, "native_sdl_artifacts": native,
            "introspection_candidates": introspection, "openapi_mentions": mentions,
            "parse_failures": failures,
            "limitations": ["A GraphQL endpoint wrapper or prose mention is not a native schema.",
                            "Introspection-shaped files are candidates until validated.",
                            "Search is bounded to committed native SDL suffixes and GraphQL/__schema mentions in APIs and GraphQL directories; arbitrary embedded schemas elsewhere are unassessed."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inventory(args.base, Path(__file__).resolve().parents[1])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"base_revision": result["base_revision"],
                      "native_sdl_artifacts": len(result["native_sdl_artifacts"]),
                      "introspection_candidates": len(result["introspection_candidates"]),
                      "openapi_mentions": len(result["openapi_mentions"]),
                      "parse_failures": len(result["parse_failures"])}))
    return 1 if result["parse_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
