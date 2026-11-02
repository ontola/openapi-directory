import json
import tempfile
import unittest
from pathlib import Path

from graphql import build_schema, introspection_from_schema
import graphql_schema as audit


class GraphQLSchemaTests(unittest.TestCase):
    def inspect(self, text):
        return audit.inspect(text.encode(), "sdl")

    def test_full_schema_and_native_roots(self):
        result = self.inspect('"API" type Query { user(id: ID!): User } type User { id: ID!, name: String }')
        self.assertEqual(result["validation_errors"], [])
        self.assertEqual(result["roots"]["query"], "Query")

    def test_saved_query_is_not_a_schema(self):
        with self.assertRaises(ValueError):
            self.inspect('{ user { id } }')
        with self.assertRaises(ValueError):
            audit.inspect(b'{"data":{"user":{"id":"1"}}}', "introspection")

    def test_semantic_changes_include_descriptions_defaults_and_deprecations(self):
        base = self.inspect('type Query { field(a: Int = 1): String }')
        for variant in ['type Query { field(a: Int = 2): String }',
                        'type Query { "new docs" field(a: Int = 1): String }',
                        'type Query { field(a: Int = 1): String @deprecated(reason: "old") }',
                        'type Query { field(a: Int = 1): Int }']:
            self.assertEqual(audit.compare(base, self.inspect(variant))["status"], "changed")

    def test_applied_directives_are_not_lost(self):
        base = 'directive @scope(name: String!) on FIELD_DEFINITION\ntype Query { field: String %s }'
        a = self.inspect(base % '@scope(name: "one")')
        b = self.inspect(base % '@scope(name: "two")')
        result = audit.compare(a, b)
        self.assertTrue(result["introspection_equal"])
        self.assertEqual(result["status"], "changed")

    def test_same_source_matches_and_whitespace_is_ignored(self):
        self.assertEqual(audit.compare(self.inspect('type Query { a: String }'),
                                      self.inspect('type Query{a:String}'))["status"], "matches_source")

    def test_invalid_interface_is_blocked(self):
        invalid = self.inspect('interface Node { id: ID! } type User implements Node { id: String } type Query { user: User }')
        self.assertTrue(invalid["validation_errors"])
        self.assertEqual(audit.compare(invalid, invalid)["status"], "validation_blocked")

    def test_introspection_does_not_claim_complete_sdl_equivalence(self):
        raw = json.dumps(introspection_from_schema(build_schema('type Query { a: String }'))).encode()
        result = audit.compare(self.inspect('type Query { a: String }'), audit.inspect(raw, "introspection"))
        self.assertTrue(result["introspection_equal"])
        self.assertFalse(result["complete"])
        self.assertIsNotNone(result["limitation"])

    def test_error_response_is_not_partial_success(self):
        with self.assertRaises(ValueError):
            audit.inspect(b'{"errors":[{"message":"denied"}],"data":{}}', "introspection")

    def test_changes_identify_types_fields_and_deprecation_locations(self):
        a = self.inspect('type Query { old: String, stable: String }')
        b = self.inspect('type Query { new: String, stable: String @deprecated(reason: "retired") }')
        changes = audit.compare(a, b)["semantic_changes"]
        self.assertIn({"kind": "removed", "path": "#/__schema/types/Query/fields/old"}, changes)
        self.assertIn({"kind": "added", "path": "#/__schema/types/Query/fields/new"}, changes)
        self.assertIn({"kind": "changed", "path": "#/__schema/types/Query/fields/stable/isDeprecated"}, changes)

    def test_snapshot_integrity_detects_tampering_and_false_validity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = b'interface Node { id: ID! } type User implements Node { id: String } type Query { user: User }'
            result = audit.summary(audit.inspect(raw, "sdl"))
            (root / "schema.graphql").write_bytes(raw)
            provenance = {"format": "sdl", "sha256": result["sha256"], "validation": result,
                          "status": "validation_blocked"}
            (root / "provenance.json").write_text(json.dumps(provenance))
            item = {"path": "schema.graphql", "provenance": "provenance.json",
                    "sha256": result["sha256"], "status": "validation_blocked"}
            self.assertEqual(audit.verify_index(root, {"artifacts": [item]})["snapshot_integrity_errors"], [])
            item["status"] = "verified_current"
            self.assertTrue(audit.verify_index(root, {"artifacts": [item]})["snapshot_integrity_errors"])
            item["status"] = "validation_blocked"
            (root / "schema.graphql").write_bytes(raw + b'\n')
            self.assertTrue(audit.verify_index(root, {"artifacts": [item]})["snapshot_integrity_errors"])

    def test_artifacts_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit.verify_index(Path(directory), {"artifacts": [{"path": "../secret", "provenance": "../meta"}]})
