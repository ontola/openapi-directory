import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import conversion
import update


def swagger():
    return {"swagger": "2.0", "info": {"title": "Legacy API", "version": "1.0"},
            "host": "api.example.com", "schemes": ["https"], "basePath": "/v1",
            "consumes": ["application/json"], "produces": ["application/json"],
            "securityDefinitions": {"Key": {"type": "apiKey", "in": "header", "name": "X-Key"}},
            "security": [{"Key": []}],
            "paths": {"/items/{id}": {"parameters": [{"$ref": "#/parameters/Id"}],
                       "put": {"parameters": [{"in": "body", "name": "body", "required": True,
                                                "schema": {"$ref": "#/definitions/Record"}}],
                               "responses": {"200": {"description": "OK", "schema": {"$ref": "#/definitions/Record"}}}}}},
            "parameters": {"Id": {"in": "path", "name": "id", "required": True, "type": "string"}},
            "definitions": {"Record": {"type": "object", "properties": {"name": {"type": "string", "minLength": 1}}}}}


SOURCE = {"id": "legacy", "target": "APIs/example.com/1.0/openapi.yaml", "url": "https://vendor.example/api.json",
          "conversion": {"tool": "swagger2openapi", "version": "7.0.8"}}


def metadata(raw):
    return {"url": SOURCE["url"], "sha256": update.sha256(raw), "fetched_at": "today"}


class ConversionTests(unittest.TestCase):
    def test_real_conversion_preserves_body_security_and_refs_and_records_format_chain(self):
        spec = swagger()
        original = copy.deepcopy(spec)
        raw = json.dumps(spec).encode()
        fetched = metadata(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted, steps = update.prepare_document(SOURCE, raw, fetched, Path(directory))
            fetched["transformations"] = steps
            self.assertEqual(update.validate_document(converted), [])
            self.assertEqual(converted["servers"], [{"url": "https://api.example.com/v1"}])
            self.assertEqual(converted["security"], [{"Key": []}])
            self.assertEqual(converted["components"]["securitySchemes"]["Key"]["name"], "X-Key")
            operation = converted["paths"]["/items/{id}"]["put"]
            self.assertTrue(operation["requestBody"]["required"])
            self.assertEqual(operation["requestBody"]["content"]["application/json"]["schema"]["$ref"], "#/components/schemas/Record")
            old = copy.deepcopy(converted)
            old["info"]["x-logo"] = {"url": "https://example.com/logo.svg"}
            imported = update.import_document(SOURCE, converted, fetched, old)
            self.assertEqual([o["format"] for o in imported["info"]["x-origin"]], ["swagger", "openapi"])
            self.assertEqual([o["version"] for o in imported["info"]["x-origin"]], ["2.0", "3.0"])
            self.assertEqual(imported["info"]["x-logo"], old["info"]["x-logo"])
            self.assertNotIn("no OpenAPI version conversion", " ".join(imported["info"]["x-conversion"]))
            self.assertIn("resolve:false", " ".join(steps))
            self.assertEqual(fetched["conversion"]["patches"], 0)
            self.assertEqual(fetched["conversion"]["warnings"], [])
            output = Path(directory) / SOURCE["id"] / fetched["sha256"] / "converted.json"
            self.assertEqual(update.sha256(output.read_bytes()), fetched["conversion"]["converted_sha256"])
            self.assertEqual(update.canonical(update.parse(update.serialize_document(imported).encode())), update.canonical(imported))
        self.assertEqual(spec, original)

    def nullable_fixture(self):
        spec = swagger()
        schema = {"type": "string", "format": "date-time", "x-nullable": True,
                  "description": "Vendor nullable timestamp"}
        spec["definitions"]["Record"]["properties"]["timestamp"] = copy.deepcopy(schema)
        source = copy.deepcopy(SOURCE)
        source["conversion"].update(expected_patches=1, nullable_extensions=[{
            "from": "#/definitions/Record/properties/timestamp",
            "to": "#/components/schemas/Record/properties/timestamp", "schema": schema}])
        return source, spec

    def test_nullable_extension_translation_has_zero_patch_control_and_exact_output(self):
        source, spec = self.nullable_fixture()
        raw = json.dumps(spec).encode(); observed = metadata(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted, steps = update.prepare_document(source, raw, observed, Path(directory))
            prop = converted["components"]["schemas"]["Record"]["properties"]["timestamp"]
            self.assertTrue(prop["nullable"]); self.assertNotIn("x-nullable", prop)
            self.assertEqual(observed["conversion"]["patches"], 1)
            control = observed["conversion"]["nullable_control"]
            self.assertEqual(control["patches"], 0)
            self.assertTrue(control["complete_output_equality_except_nullable"])
            self.assertIn("No null semantics removed", steps[0])
            self.assertEqual(update.validate_document(converted), [])

    def test_nullable_guard_rejects_context_location_or_mapping_changes(self):
        source, spec = self.nullable_fixture()
        cases = []
        changed = copy.deepcopy(spec); changed["definitions"]["Record"]["properties"]["timestamp"]["description"] = "changed"
        cases.append((source, changed))
        changed = copy.deepcopy(spec); changed["definitions"]["Record"]["properties"]["second"] = {"type": "string", "x-nullable": True}
        cases.append((source, changed))
        changed_source = copy.deepcopy(source); changed_source["conversion"]["nullable_extensions"][0]["to"] = "#/components/schemas/Record/properties/name"
        cases.append((changed_source, spec))
        changed_source = copy.deepcopy(source); changed_source["conversion"]["nullable_extensions"] *= 2
        cases.append((changed_source, spec))
        for recipe, native in cases:
            raw = json.dumps(native).encode()
            with self.subTest(recipe=recipe), tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
                update.prepare_document(recipe, raw, metadata(raw), Path(directory))

    def test_unguarded_false_nullable_extension_is_preserved_as_nullable_false(self):
        source, spec = self.nullable_fixture()
        spec["definitions"]["Record"]["properties"]["label"] = {"type": "string", "x-nullable": False}
        raw = json.dumps(spec).encode(); observed = metadata(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted, _ = update.prepare_document(source, raw, observed, Path(directory))
        label = converted["components"]["schemas"]["Record"]["properties"]["label"]
        self.assertEqual(label, {"type": "string", "nullable": False})
        self.assertEqual(observed["conversion"]["patches"], 1)
        # An unguarded *true* extension is still rejected.
        spec["definitions"]["Record"]["properties"]["label"]["x-nullable"] = True
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(ValueError, "locations changed"):
            update.prepare_document(source, raw, metadata(raw), Path(directory))

    def test_nullable_control_rejects_unrelated_repairs_even_with_accepted_total(self):
        source, spec = self.nullable_fixture()
        spec["definitions"]["Record"]["properties"]["variant"] = {"type": ["string", "integer"]}
        source["conversion"]["expected_patches"] = 2
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(ValueError, "unrelated repair"):
            update.prepare_document(source, raw, metadata(raw), Path(directory))

    def test_zero_count_control_still_requires_complete_output_equality(self):
        source, spec = self.nullable_fixture()
        raw = json.dumps(spec).encode()
        original_run = conversion.subprocess.run
        def corrupt_control(args, **kwargs):
            result = original_run(args, **kwargs)
            output = Path(args[3])
            if output.name == "nullable-control-result.json":
                data = json.loads(output.read_text())
                data["openapi"]["info"]["description"] = "Unexpected converter change"
                output.write_text(json.dumps(data))
            return result
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(conversion.subprocess, "run", side_effect=corrupt_control), \
                self.assertRaisesRegex(ValueError, "content beyond guarded"):
            update.prepare_document(source, raw, metadata(raw), Path(directory))

    def test_explicit_allof_mode_retains_schema_ref_annotations_and_control(self):
        source, spec = self.nullable_fixture()
        spec["definitions"]["Record"]["properties"]["child"] = {
            "$ref": "#/definitions/Child", "description": "Specific vendor role", "title": "Child record"}
        spec["definitions"]["Child"] = {"type": "object", "required": ["id"],
                                       "properties": {"id": {"type": "string", "minLength": 1}}}
        source["conversion"]["ref_siblings"] = "allOf"
        raw = json.dumps(spec).encode(); observed = metadata(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted, steps = update.prepare_document(source, raw, observed, Path(directory))
            child = converted["components"]["schemas"]["Record"]["properties"]["child"]
            self.assertEqual(child, {"allOf": [{"$ref": "#/components/schemas/Child"},
                                            {"description": "Specific vendor role", "title": "Child record"}]})
            self.assertEqual(converted["components"]["schemas"]["Child"], spec["definitions"]["Child"])
            self.assertEqual(observed["conversion"]["options"]["refSiblings"], "allOf")
            self.assertEqual(observed["conversion"]["nullable_control"]["patches"], 0)
            self.assertEqual(update.validate_document(converted), [])
            self.assertIn("refSiblings:allOf", steps[0])
        source["conversion"]["ref_siblings"] = "preserve"
        with tempfile.TemporaryDirectory() as directory, patch.object(conversion.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "reference-sibling"):
                update.prepare_document(source, raw, metadata(raw), Path(directory))
            run.assert_not_called()

    def test_unexpected_converter_patches_stop_and_reviewed_patches_still_require_validation(self):
        spec = swagger()
        spec["definitions"]["Record"]["properties"]["value"] = {"type": ["string", "null"]}
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            with self.assertRaisesRegex(ValueError, "warning/patch count changed"):
                update.prepare_document(SOURCE, raw, metadata(raw), cache)
            result = json.loads((cache / SOURCE["id"] / update.sha256(raw) / "conversion-result.json").read_text())
            self.assertEqual(result["patches"], 1)
            source = copy.deepcopy(SOURCE)
            source["conversion"]["expected_patches"] = 1
            converted, _ = update.prepare_document(source, raw, metadata(raw), cache)
            self.assertEqual(update.validate_document(converted), [])

    def test_warn_only_does_not_waive_missing_schema_validation(self):
        spec = swagger()
        spec["definitions"]["Record"]["properties"]["child"] = {"$ref": "#/definitions/Missing"}
        # A real unsupported header collection format emits a converter warning.
        # A missing schema alone is not flagged by this converter; validation
        # must still reject it even after a reviewed warning count is accepted.
        spec["paths"]["/items/{id}"]["put"]["parameters"].append({"in": "header", "name": "X-Ids",
            "type": "array", "items": {"type": "string"}, "collectionFormat": "ssv"})
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            with self.assertRaisesRegex(ValueError, "warning/patch count changed"):
                update.prepare_document(SOURCE, raw, metadata(raw), cache)
            result = json.loads((cache / SOURCE["id"] / update.sha256(raw) / "conversion-result.json").read_text())
            self.assertEqual(len(result["warnings"]), 1)
            source = copy.deepcopy(SOURCE)
            source["conversion"]["expected_warnings"] = 1
            fetched = metadata(raw)
            converted, _ = update.prepare_document(source, raw, fetched, cache)
            self.assertTrue(update.validate_document(converted))
            with self.assertRaisesRegex(ValueError, "Import blocked"):
                update.import_document(source, converted, fetched, None)

    def test_reviewed_empty_descriptions_and_disjoint_types_do_not_hide_invalid_defaults(self):
        spec = swagger()
        spec["paths"]["/items/{id}"]["put"]["responses"]["200"]["description"] = ""
        properties = spec["definitions"]["Record"]["properties"]
        properties["variant_id"] = {"type": ["string", "integer"]}
        properties["notify_on_subscribe"] = {"type": "string", "default": False}
        source = copy.deepcopy(SOURCE)
        source["conversion"]["expected_patches"] = 2
        raw = json.dumps(spec).encode()
        fetched = metadata(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted, _ = update.prepare_document(source, raw, fetched, Path(directory))
            self.assertEqual(converted["paths"]["/items/{id}"]["put"]["responses"]["200"]["description"], "")
            new_properties = converted["components"]["schemas"]["Record"]["properties"]
            self.assertEqual(new_properties["variant_id"], {"oneOf": [{"type": "string"}, {"type": "integer"}]})
            self.assertEqual(new_properties["notify_on_subscribe"], {"type": "string", "default": False})
            errors = update.validate_document(converted)
            self.assertTrue(any("notify_on_subscribe/default" in error for error in errors), errors)
            with self.assertRaisesRegex(ValueError, "Import blocked"):
                update.import_document(source, converted, fetched, None)
        self.assertEqual(spec, update.parse(raw))

    def test_preflight_rejects_unpinned_refs_and_warning_marker_collisions_without_running_tool(self):
        for ref in ("https://vendor.example/schema.json#/Item", "file:///tmp/item.json", "schema.json#/Item"):
            spec = swagger()
            spec["x-documentation"] = {"$ref": ref}
            with tempfile.TemporaryDirectory() as directory, patch.object(conversion.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "External references"):
                    conversion.prepare(SOURCE, spec, metadata(b"raw"), Path(directory))
                run.assert_not_called()
        spec = swagger()
        spec["x-s2o-warning"] = "Already converted warning"
        with tempfile.TemporaryDirectory() as directory, patch.object(conversion.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "warning markers"):
                conversion.prepare(SOURCE, spec, metadata(b"raw"), Path(directory))
            run.assert_not_called()

    def test_changed_format_or_invalid_expectations_require_recipe_review(self):
        cases = [(SOURCE, {"openapi": "3.0.0"}),
                 ({**SOURCE, "conversion": {"tool": "swagger2openapi", "version": "different"}}, swagger()),
                 ({**SOURCE, "conversion": {"tool": "swagger2openapi", "version": "7.0.8", "expected_patches": True}}, swagger())]
        with tempfile.TemporaryDirectory() as directory, patch.object(conversion.subprocess, "run") as run:
            for source, spec in cases:
                with self.assertRaises(ValueError):
                    conversion.prepare(source, spec, metadata(b"raw"), Path(directory))
            run.assert_not_called()

    def test_failed_conversion_audit_retains_original_bytes_and_no_success_comparison(self):
        spec = swagger()
        spec["definitions"]["Record"]["properties"]["value"] = {"type": ["string", "null"]}
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory, patch.object(update, "fetch", return_value=(raw, metadata(raw))):
            result = update.audit(SOURCE, "origin/main", Path(directory))
            self.assertEqual(result["status"], "failed")
            self.assertIn("warning/patch count changed", result["error"])
            self.assertEqual(result["last_successful_fetch"], "today")
            self.assertNotIn("last_successful_comparison", result)
            self.assertNotIn("last_successful_validation", result)
            snapshot = Path(directory) / SOURCE["id"] / update.sha256(raw)
            self.assertEqual((snapshot / "source").read_bytes(), raw)
            self.assertTrue((snapshot / "conversion-result.json").exists())

    def test_exact_vendor_patches_apply_after_conversion(self):
        raw = json.dumps(swagger()).encode()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recipe = {"schema_version": 1, "description": "Reviewed schema correction", "operations": [
                {"pointer": "#/components/schemas/Record/properties/name/minLength", "from": 1, "value": 3, "context": {"type": "string"}}]}
            path = root / "maintenance/patches/test.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(recipe))
            source = {**SOURCE, "patches": ["maintenance/patches/test.json"]}
            with patch.object(update, "ROOT", root):
                converted, steps = update.prepare_document(source, raw, metadata(raw), root / "cache")
            self.assertEqual(converted["components"]["schemas"]["Record"]["properties"]["name"]["minLength"], 3)
            self.assertTrue(steps[0].startswith("Converted Swagger"))
            self.assertTrue(steps[1].startswith("Applied maintenance/patches/test.json"))
            self.assertEqual(update.validate_document(converted), [])

    def test_missing_responses_are_blocked_before_the_converter_can_invent_defaults(self):
        spec = swagger()
        del spec["paths"]["/items/{id}"]["put"]["responses"]
        raw = json.dumps(spec).encode()
        with tempfile.TemporaryDirectory() as directory, patch.object(conversion.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "refusing to let the converter invent"):
                update.prepare_document(SOURCE, raw, metadata(raw), Path(directory))
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
