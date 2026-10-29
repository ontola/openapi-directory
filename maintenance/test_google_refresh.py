"""Import safeguards independent of any real source checkout or API."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import google_discovery as google
import google_refresh as refresh
from test_google_discovery import source


class GoogleRefreshTests(unittest.TestCase):
    def test_preserves_existing_curation_and_does_not_invent_new_curation(self):
        converted = google.convert(source())
        old = {"info": {"title": "Old title", "x-logo": {"url": "https://invented.example/logo.svg"},
                        "x-preferred": True, "contact": {"x-twitter": "invented"}},
               "externalDocs": {"url": "https://invented.example/docs"}, "tags": [{"name": "curated"}],
               "x-hasEquivalentPaths": True}
        before = copy.deepcopy(old)
        result = refresh.preserve_curation(old, converted)
        self.assertEqual(result["info"]["title"], converted["info"]["title"])
        self.assertEqual(result["info"]["x-logo"], old["info"]["x-logo"])
        self.assertIs(result["info"]["x-preferred"], True)
        self.assertEqual(result["info"]["contact"]["x-twitter"], "invented")
        self.assertEqual(result["tags"], old["tags"])
        self.assertEqual(result["externalDocs"], old["externalDocs"])
        self.assertIs(result["x-hasEquivalentPaths"], True)
        refresh.check_curation(old, result)
        self.assertEqual(old, before)
        self.assertNotIn("x-logo", refresh.preserve_curation(None, converted)["info"])

    def test_independent_curation_check_catches_missing_or_changed_root_flags(self):
        old = {"info": {"x-logo": {"url": "https://invented.example/logo.svg"}}, "x-hasEquivalentPaths": True}
        document = refresh.preserve_curation(old, google.convert(source()))
        del document["x-hasEquivalentPaths"]
        with self.assertRaisesRegex(ValueError, "root curation changed"):
            refresh.check_curation(old, document)
        document["x-hasEquivalentPaths"] = False
        with self.assertRaisesRegex(ValueError, "root curation changed"):
            refresh.check_curation(old, document)
        document["x-hasEquivalentPaths"] = True
        del document["info"]["x-logo"]
        with self.assertRaisesRegex(ValueError, "info curation changed"):
            refresh.check_curation(old, document)

    def test_typed_roundtrip_check_distinguishes_bool_int_and_float(self):
        self.assertFalse(refresh.typed_equal({"v": True}, {"v": 1}))
        self.assertFalse(refresh.typed_equal({"v": 1}, {"v": 1.0}))
        self.assertTrue(refresh.typed_equal({"v": [9223372036854775807]}, {"v": [9223372036854775807]}))

    def test_independent_schema_check_detects_lost_constraints(self):
        native = source()
        native["schemas"]["Note"]["properties"]["id"]["pattern"] = "^invented-.*$"
        document = google.convert(native)
        del document["components"]["schemas"]["Note"]["properties"]["id"]["pattern"]
        with self.assertRaisesRegex(ValueError, "Schema field changed"):
            google.check(native, document)

    def test_invalid_candidate_never_creates_a_target_or_success_stamp(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            native = source()
            native["schemas"]["Note"]["properties"]["id"]["default"] = False
            path = root / "native.json"
            path.write_text(json.dumps(native))
            row = refresh.candidate((str(path), "a" * 40, "discoveries/invented.v1.json",
                                     "APIs/googleapis.com/invented/v1/openapi.yaml", None, str(root / "cache")))
            self.assertEqual(row["status"], "blocked")
            self.assertNotIn("candidate", row)
            self.assertFalse((root / "cache").exists())

    def test_newer_live_discovery_is_not_downgraded_to_an_older_mirror(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            native = source()
            native["revision"] = "20261028"
            path = root / "native.json"
            path.write_text(json.dumps(native))
            old = b'info:\n  x-conversion:\n    - "Official Google Discovery document, revision 20261029"\n'
            row = refresh.candidate((str(path), "a" * 40, "discoveries/invented.v1.json",
                                     "APIs/googleapis.com/invented/v1/openapi.yaml", old, str(root / "cache")))
            self.assertEqual(row["status"], "retained_newer")
            self.assertFalse((root / "cache").exists())

    def test_changed_source_bytes_cannot_claim_the_pinned_revision(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "native.json"
            path.write_text(json.dumps(source()))
            row = refresh.candidate((str(path), "a" * 40, "discoveries/invented.v1.json",
                                     "APIs/googleapis.com/invented/v1/openapi.yaml", None, str(root / "cache"), "b" * 40))
            self.assertEqual(row["status"], "blocked")
            self.assertIn("pinned Git blob", row["error"])
            self.assertNotIn("candidate", row)

    def test_apply_checks_both_candidate_hash_and_working_tree_edits(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            candidate = root / "candidate.yaml"
            candidate.write_bytes(b"new validated bytes\n")
            target = root / "APIs/googleapis.com/invented/v1/openapi.yaml"
            target.parent.mkdir(parents=True)
            original = b"original bytes\n"
            target.write_bytes(original)
            row = {"status": "refreshed", "target": str(target.relative_to(root)), "candidate": str(candidate),
                   "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                   "baseline_sha256": hashlib.sha256(original).hexdigest()}
            target.write_bytes(b"an intentional working-tree edit\n")
            with self.assertRaisesRegex(ValueError, "working-tree edit"):
                refresh.apply([row], root)
            self.assertEqual(target.read_bytes(), b"an intentional working-tree edit\n")
            target.write_bytes(original)
            candidate.write_bytes(b"unexpected changed bytes\n")
            with self.assertRaisesRegex(ValueError, "Candidate changed"):
                refresh.apply([row], root)
            self.assertEqual(target.read_bytes(), original)
            candidate.write_bytes(b"new validated bytes\n")
            refresh.apply([row], root)
            self.assertEqual(target.read_bytes(), candidate.read_bytes())


if __name__ == "__main__":
    unittest.main()
