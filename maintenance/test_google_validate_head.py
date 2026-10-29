import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import google_refresh as refresh
import google_validate_head as validator
from test_google_discovery import source


class GoogleHeadTests(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL).decode().strip()

    def setup_artifact(self, root):
        self.git(root, "init", "-q", "-b", "main")
        self.git(root, "config", "user.name", "Invented Test")
        self.git(root, "config", "user.email", "invented@example.invalid")
        self.git(root, "commit", "--allow-empty", "-m", "Invented baseline")
        base = self.git(root, "rev-parse", "HEAD")
        cache = root / "cache"
        raw = json.dumps(source()).encode()
        digest = hashlib.sha256(raw).hexdigest()
        native = cache / "sources" / (digest + ".json")
        native.parent.mkdir(parents=True)
        native.write_bytes(raw)
        path = "APIs/googleapis.com/invented/v1/openapi.yaml"
        row = refresh.candidate((str(native), "a" * 40, "discoveries/invented.v1.json", path, None, str(cache / "initial")))
        self.assertEqual(row["status"], "added")
        target = root / path
        target.parent.mkdir(parents=True)
        shutil.copyfile(row["candidate"], target)
        self.git(root, "add", path)
        self.git(root, "commit", "-m", "Invented API addition")
        return base, self.git(root, "rev-parse", "HEAD"), path, cache

    def test_exact_head_is_reconstructed_from_the_pinned_native_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, head, path, cache = self.setup_artifact(root)
            with patch("urllib.request.urlopen", side_effect=AssertionError("No network in this test")):
                result = validator.artifact((root, base, head, path, cache))
            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["mode"], "native-projection")
            self.assertEqual(result["operations"], 1)

    def test_modified_valid_schema_is_rejected_despite_valid_provenance(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, _, path, cache = self.setup_artifact(root)
            target = root / path
            document = refresh.yaml.load(target.read_bytes(), Loader=refresh.LOADER)
            document["components"]["schemas"]["Note"]["properties"]["id"]["type"] = "integer"
            target.write_text(refresh.yaml.safe_dump(document))
            self.git(root, "add", path)
            self.git(root, "commit", "-m", "Invented mismatch")
            result = validator.artifact((root, base, self.git(root, "rev-parse", "HEAD"), path, cache))
            self.assertEqual(result["status"], "invalid")
            self.assertIn("exactly match", result["error"])

    def test_tampered_source_and_artifact_removal_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, head, path, cache = self.setup_artifact(root)
            next((cache / "sources").glob("*.json")).write_text("{}")
            result = validator.artifact((root, base, head, path, cache))
            self.assertEqual(result["status"], "invalid")
            self.assertIn("source hash mismatch", result["error"])
            self.git(root, "rm", path)
            self.git(root, "commit", "-m", "Invented removal")
            result = validator.artifact((root, base, self.git(root, "rev-parse", "HEAD"), path, cache))
            self.assertEqual(result["status"], "invalid")
            self.assertIn("Removing a Google artifact", result["error"])

    def test_source_url_must_be_an_exact_official_repository_pin(self):
        document = {"info": {"x-conversion": [validator.PROFILE, "original source SHA-256 " + "b" * 64 + "."],
                             "x-origin": [{"format": "google", "url": "https://attacker.example/spec.json"}]}}
        with self.assertRaisesRegex(ValueError, "official Google repository"):
            validator.source_of(document)
        document["info"]["x-origin"][0]["url"] = "https://raw.githubusercontent.com/googleapis/discovery-artifact-manager/master/discoveries/invented.v1.json"
        with self.assertRaisesRegex(ValueError, "full SHA"):
            validator.source_of(document)


if __name__ == "__main__":
    unittest.main()
