import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from graphql_inventory import inventory


class GraphQLInventoryTests(unittest.TestCase):
    def test_committed_tree_not_working_copy_and_wrappers_are_not_schemas(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            api = root / "APIs/example.com/1/openapi.yaml"
            api.parent.mkdir(parents=True)
            api.write_text('openapi: 3.0.0\ninfo: {title: GraphQL wrapper, version: "1"}\npaths: {/graphql: {post: {responses: {"200": {description: OK}}}}}\n')
            native = root / "GraphQL/example.com/schema.graphql"
            native.parent.mkdir(parents=True)
            native.write_text('type Query { field: String }')
            (native.parent / "schema.json").write_text(json.dumps({"data": {"__schema": {}}}))
            git("add", ".")
            git("commit", "-qm", "fixture")
            native.unlink()
            result = inventory("HEAD", root)
            self.assertEqual(result["native_sdl_artifacts"], ["GraphQL/example.com/schema.graphql"])
            self.assertEqual(result["introspection_candidates"], ["GraphQL/example.com/schema.json"])
            self.assertEqual(result["openapi_mentions"][0]["classification"], "endpoint_wrapper")
            self.assertFalse(result["openapi_mentions"][0]["native_schema"])
            self.assertEqual(result["parse_failures"], [])
