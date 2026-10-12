import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update


def zendesk_conversations_fixture():
    recipe_path = "maintenance/patches/zendesk-conversations.json"
    recipe = json.loads((update.ROOT / recipe_path).read_text())
    asserted = {entry["pointer"]: copy.deepcopy(entry["value"])
                for entry in recipe["assertions"]}
    return {"openapi": "3.0.2", "info": {"title": "Conversations guard", "version": "17.13.2"},
            "paths": {"/v2/apps/{appId}/users": {"get": {
                "description": asserted["#/paths/~1v2~1apps~1{appId}~1users/get/description"],
                "parameters": [{"name": "appId", "in": "path", "required": True,
                                "schema": {"type": "string"}},
                               {"$ref": "#/components/parameters/userFilterQuery"}],
                "responses": {"200": {"description": "OK"}}}}},
            "components": {"schemas": {
                "reference": asserted["#/components/schemas/reference"],
                "displayName": copy.deepcopy(recipe["operations"][0]["context"]["displayName"])},
                "parameters": {"userFilterQuery": asserted["#/components/parameters/userFilterQuery"]}}}


def document(version="1.0"):
    return {"openapi": "3.1.0", "info": {"title": "Test API", "version": version},
            "paths": {"/items/{id}": {"parameters": [{"$ref": "#/components/parameters/Id"}],
                                      "get": {"responses": {"200": {"description": "OK"}}}}},
            "components": {"parameters": {"Id": {"name": "id", "in": "path", "required": True,
                                                    "schema": {"type": "string"}}},
                           "schemas": {"Choice": {"oneOf": [{"type": "string"}, {"type": "null"}]}}}}


class UpdaterTests(unittest.TestCase):
    def coinbase_delegation_fixture(self):
        recipe = json.loads((update.ROOT / "maintenance/patches/coinbase-cdp.json").read_text())
        spec = {"openapi": "3.1.0", "info": {"title": "CDP guard", "version": "2.0.0"},
                "paths": {}, "components": {"parameters": {"XDeveloperAuth":
                    copy.deepcopy(recipe["assertions"][0]["value"])}}}
        for assertion in recipe["assertions"][1:]:
            path, method, field = assertion["pointer"][8:].split("/")
            path = path.replace("~1", "/").replace("~0", "~")
            operation = spec["paths"].setdefault(path, {}).setdefault(method, {
                "responses": {"200": {"description": "OK"}}})
            operation[field] = copy.deepcopy(assertion["value"])
        for reference in update.reference_objects(spec):
            name = reference.rsplit("/", 1)[1]
            if reference.startswith("#/components/schemas/"):
                spec["components"].setdefault("schemas", {})[name] = {"type": "string"}
            elif name != "XDeveloperAuth":
                # Other vendor parameters are unchanged by this recipe; minimal
                # independent definitions keep the bounded reference fixture valid.
                spec["components"]["parameters"][name] = {
                    "name": name, "in": "header", "required": False,
                    "schema": {"type": "string"}}
        return spec

    def test_coinbase_reference_flags_preserve_optional_header_and_contract(self):
        from jsonschema import Draft202012Validator
        source = {"patches": ["maintenance/patches/coinbase-cdp.json"]}
        spec = self.coinbase_delegation_fixture()
        raw = json.dumps(spec).encode()
        self.assertTrue(update.validate_document(spec))
        result, steps = update.prepare_document(source, raw)
        expected = copy.deepcopy(spec)
        for operation in expected["paths"].values():
            for method in operation.values():
                del method["parameters"][1]["required"]
        self.assertEqual(result, expected)
        self.assertEqual(update.validate_document(result), [])
        header = result["components"]["parameters"]["XDeveloperAuth"]
        self.assertIs(header["required"], False)
        validator = Draft202012Validator(header["schema"])
        for instance, valid in (("", True), ("signed-token", True), (None, False),
                                (False, False), (42, False), ({}, False)):
            self.assertEqual(validator.is_valid(instance), valid)
        for path in result["paths"].values():
            for operation in path.values():
                reference = operation["parameters"][1]
                self.assertEqual(reference, {"$ref": "#/components/parameters/XDeveloperAuth"})
                self.assertEqual(update.pointer(result, reference["$ref"]), header)
        self.assertEqual(update.canonical(update.parse(update.serialize_document(result).encode())),
                         update.canonical(result))
        self.assertEqual(json.loads(raw), spec)
        self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])

    def test_coinbase_recipe_stops_on_vendor_fixes_and_referenced_header_changes(self):
        source = {"patches": ["maintenance/patches/coinbase-cdp.json"]}
        original = self.coinbase_delegation_fixture()
        changes = []
        for key, value in (("required", True), ("required", 0), ("in", "query"),
                           ("schema", {"type": "string", "minLength": 1})):
            spec = copy.deepcopy(original)
            spec["components"]["parameters"]["XDeveloperAuth"][key] = value
            changes.append(spec)
        for path, item in original["paths"].items():
            for method in item:
                for value in (None, True, 0):
                    spec = copy.deepcopy(original)
                    parameter = spec["paths"][path][method]["parameters"][1]
                    if value is None:
                        del parameter["required"]  # Native vendor correction.
                    else:
                        parameter["required"] = value
                    changes.append(spec)
                spec = copy.deepcopy(original)
                spec["paths"][path][method]["parameters"][1]["$ref"] = "#/components/parameters/Other"
                changes.append(spec)
                spec = copy.deepcopy(original)
                spec["paths"][path][method]["operationId"] = "changed-contract"
                changes.append(spec)
        for index, spec in enumerate(changes):
            raw = json.dumps(spec).encode()
            with self.subTest(change=index), self.assertRaisesRegex(ValueError, "review recipe"):
                update.prepare_document(source, raw)
            self.assertEqual(json.loads(raw), spec)


    def test_unreferenced_guard_rejects_direct_descendant_and_enclosing_uses(self):
        spec = document()
        target = "#/components/parameters/Id"
        # The fixture genuinely uses Id; removal must not be licensed.
        with self.assertRaisesRegex(ValueError, "target is used"):
            update.assert_unreferenced(spec, [target])
        spec["paths"] = {}
        update.assert_unreferenced(spec, [target])
        for ref in (target, "#/components/parameters/Id/schema", "#/components/parameters",
                    "#", "https://example.com/spec#/components/parameters/Id",
                    "#%2Fcomponents%2Fparameters%2FId"):
            for location in ("example", "x-vendor", "discriminator"):
                changed = copy.deepcopy(spec)
                changed[location] = {"nested": [{"$ref": ref}]}
                with self.subTest(ref=ref, location=location), self.assertRaisesRegex(ValueError, "target is used"):
                    update.assert_unreferenced(changed, [target])
        spec["x-other"] = {"$ref": "#/components/parameters/IdOther"}
        update.assert_unreferenced(spec, [target])

    def test_unreferenced_guard_handles_pointer_escapes_arrays_and_aliases(self):
        spec = document()
        spec["x-data"] = {"a/b~c": [{"value": 42}]}
        target = "#/x-data/a~1b~0c/0"
        update.assert_unreferenced(spec, [target])
        for ref in (target, "#/x-data/a~1b~0c/%30", "#/x-data/a~1b~0c/0/value",
                    "#/x-data/a~1b~0c"):
            spec["x-use"] = [ref]
            with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, "target is used"):
                update.assert_unreferenced(spec, [target])
        del spec["x-use"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            update.assert_unreferenced(spec, [target, "#/x-data/a~1b~0c/%30"])

    def test_unreferenced_preconditions_fail_before_patch_and_retain_cache(self):
        spec = document()
        raw = json.dumps(spec).encode()
        recipe = {"schema_version": 1, "description": "Reviewed unused removal",
                  "unreferenced": ["#/components/parameters/Id"],
                  "operations": [{"pointer": "#/components/parameters/Id", "from": spec["components"]["parameters"]["Id"],
                                  "remove": True, "context": {"Id": spec["components"]["parameters"]["Id"]}}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/fixture.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(recipe))
            cache = root / "cache"
            metadata = {"sha256": update.sha256(raw), "fetched_at": "today"}
            with patch.object(update, "ROOT", root), patch.object(update, "fetch", return_value=(raw, metadata)):
                result = update.audit({"id": "guard", "target": "APIs/example.com/1/openapi.yaml",
                                       "patches": ["maintenance/patches/fixture.json"]}, "origin/main", cache)
            self.assertEqual(result["status"], "failed")
            self.assertIn("target is used", result["error"])
            self.assertNotIn("last_successful_validation", result)
            self.assertEqual((cache / "guard" / metadata["sha256"] / "source").read_bytes(), raw)
            self.assertEqual(json.loads(raw), spec)

    def test_unreferenced_guard_rejects_malformed_missing_and_duplicate_targets(self):
        spec = document()
        spec["paths"] = {}
        for targets in (None, {}, [], [None], ["https://example.com"], ["#/missing"],
                        ["#/components/parameters/Id", "#/components/parameters/Id"],
                        ["#/components/parameters/Id~2"], ["#/components/parameters/%ZZ"],
                        ["#/components/schemas/Choice/oneOf/01"]):
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                update.assert_unreferenced(spec, targets)

    def test_zendesk_support_null_only_alternative_preserves_original_semantics(self):
        from jsonschema import Draft4Validator
        from openapi_schema_validator import OAS30Validator
        recipe = json.loads((update.ROOT / "maintenance/patches/zendesk-support.json").read_text())
        original = recipe["assertions"][0]["value"]["properties"]["value"]
        compatible = recipe["operations"][0]["value"]
        expected = copy.deepcopy(original)
        expected["oneOf"][4] = {"type": "string", "nullable": True, "enum": [None]}
        self.assertEqual(compatible, expected)
        outcomes = []
        for value in (None, "", "current_user", "null", True, False, 0, 1, -2, 1.5, {}, [], ["current_user"]):
            a = Draft4Validator(original).is_valid(value)
            b = OAS30Validator(compatible).is_valid(value)
            self.assertEqual(a, b, value)
            self.assertEqual(OAS30Validator(compatible["oneOf"][4]).is_valid(value), value is None)
            outcomes.append(a)
        self.assertIn(True, outcomes)
        self.assertIn(False, outcomes)
        # Preserve the vendor's overlapping integer/number oneOf alternatives.
        self.assertFalse(OAS30Validator(compatible).is_valid(1))

    def test_zendesk_support_removes_only_unused_parameter_and_refuses_vendor_fixes(self):
        recipe_path = "maintenance/patches/zendesk-support.json"
        recipe = json.loads((update.ROOT / recipe_path).read_text())
        condition, parameter = [copy.deepcopy(entry["value"]) for entry in recipe["assertions"]]
        spec = {"openapi": "3.0.3", "info": {"title": "Support guard", "version": "2.0.0"}, "paths": {},
                "components": {"schemas": {"AccessRuleCondition": condition}, "parameters": {
                    "UserLogin": parameter, **copy.deepcopy(recipe["operations"][1]["context"])}}}
        source = {"patches": [recipe_path]}
        raw = json.dumps(spec).encode()
        result, steps = update.prepare_document(source, raw)
        self.assertEqual(update.validate_document(result), [])
        expected = copy.deepcopy(spec)
        expected["components"]["schemas"]["AccessRuleCondition"]["properties"]["value"] = recipe["operations"][0]["value"]
        del expected["components"]["parameters"]["UserLogin"]
        self.assertEqual(result, expected)
        self.assertIn(update.sha256((update.ROOT / recipe_path).read_bytes()), steps[0])
        for change in ("new use", "style fixed", "removed", "null fixed", "operator changed"):
            changed = copy.deepcopy(spec)
            if change == "new use":
                changed["x-use"] = {"$ref": "#/components/parameters/UserLogin"}
            elif change == "style fixed":
                changed["components"]["parameters"]["UserLogin"]["style"] = "simple"
            elif change == "removed":
                del changed["components"]["parameters"]["UserLogin"]
            elif change == "null fixed":
                changed["components"]["schemas"]["AccessRuleCondition"]["properties"]["value"] = recipe["operations"][0]["value"]
            else:
                changed["components"]["schemas"]["AccessRuleCondition"]["properties"]["operator"]["enum"].append("not_present")
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "review recipe"):
                update.prepare_document(source, json.dumps(changed).encode())
        self.assertEqual(json.loads(raw), spec)

    def confluence_v1_fixture(self):
        recipe = json.loads((update.ROOT / "maintenance/patches/confluence-v1.json").read_text())
        spec = {"openapi": "3.0.1", "info": {"title": "Confluence v1 guard", "version": "1.0.0"},
                "paths": {}}
        for assertion in recipe["assertions"]:
            parts = assertion["pointer"].split("/")
            path = parts[2].replace("~1", "/").replace("~0", "~")
            operation = spec["paths"].setdefault(path, {}).setdefault("get", {
                "parameters": [], "responses": {"200": {"description": "OK"}}})
            if parts[-1] == "operationId":
                operation["operationId"] = assertion["value"]
            else:
                index = int(parts[-1])
                while len(operation["parameters"]) <= index:
                    i = len(operation["parameters"])
                    operation["parameters"].append({"name": "other" + str(i), "in": "query",
                                                     "schema": {"type": "integer"}})
                operation["parameters"][index] = copy.deepcopy(assertion["value"])
        return spec

    def test_confluence_v1_null_defaults_preserve_string_constraints_and_required_name(self):
        from openapi_schema_validator import OAS30Validator
        source = {"patches": ["maintenance/patches/confluence-v1.json"]}
        original = self.confluence_v1_fixture()
        raw = json.dumps(original).encode()
        self.assertTrue(update.validate_document(original))
        result, steps = update.prepare_document(source, raw)
        expected = copy.deepcopy(original)
        cases = (("/wiki/rest/api/label", 0, ("label", ""), (None, 0, ["label"])),
                 ("/wiki/rest/api/label", 1, ("page", "blogpost", "attachment", "page_template"),
                  (None, "user", "", ["page"], 0)),
                 ("/wiki/rest/api/group", 2, ("user", "admin", "site-admin"),
                  (None, "page", "", ["admin"], 0)))
        for path, index, accepted, rejected in cases:
            del expected["paths"][path]["get"]["parameters"][index]["schema"]["default"]
            old = original["paths"][path]["get"]["parameters"][index]["schema"]
            new = result["paths"][path]["get"]["parameters"][index]["schema"]
            for instance in accepted + rejected:
                valid = instance in accepted
                self.assertEqual(OAS30Validator(old).is_valid(instance), valid)
                self.assertEqual(OAS30Validator(new).is_valid(instance), valid)
        self.assertEqual(result, expected)
        self.assertEqual(update.validate_document(result), [])
        self.assertIs(result["paths"]["/wiki/rest/api/label"]["get"]["parameters"][0]["required"], True)
        self.assertNotIn("required", result["paths"]["/wiki/rest/api/label"]["get"]["parameters"][1])
        self.assertIs(result["paths"]["/wiki/rest/api/group"]["get"]["parameters"][2]["required"], False)
        self.assertEqual(json.loads(raw), original)
        self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])

    def test_confluence_v1_recipe_stops_on_nullable_and_other_vendor_corrections(self):
        source = {"patches": ["maintenance/patches/confluence-v1.json"]}
        for path, index in (("/wiki/rest/api/label", 0), ("/wiki/rest/api/label", 1),
                            ("/wiki/rest/api/group", 2)):
            for change in ("removed", "valid-default", "nullable", "required", "type", "name", "identity"):
                spec = self.confluence_v1_fixture()
                op = spec["paths"][path]["get"]
                param = op["parameters"][index]
                if change == "removed":
                    del param["schema"]["default"]
                elif change == "valid-default":
                    param["schema"]["default"] = param["schema"].get("enum", ["label"])[0]
                elif change == "nullable":
                    param["schema"]["nullable"] = True
                elif change == "required":
                    param["required"] = not param.get("required", False)
                elif change == "type":
                    param["schema"]["type"] = "array"
                elif change == "name":
                    param["name"] = "changed"
                else:
                    op["operationId"] = "changed"
                raw = json.dumps(spec).encode()
                with self.subTest(path=path, index=index, change=change), self.assertRaisesRegex(ValueError, "review recipe"):
                    update.prepare_document(source, raw)
                self.assertEqual(json.loads(raw), spec)

    def confluence_label_fixture(self):
        recipe = json.loads((update.ROOT / "maintenance/patches/confluence-v2.json").read_text())
        spec = {"openapi": "3.0.3", "info": {"title": "Confluence label guard", "version": "2.0.0"},
                "paths": {}}
        for assertion in recipe["assertions"]:
            path = assertion["pointer"].split("/")[2].replace("~1", "/").replace("~0", "~")
            operation = spec["paths"].setdefault(path, {}).setdefault("get", {
                "parameters": [{"name": "id", "in": "path", "required": True,
                                "schema": {"type": "integer"}}, None],
                "responses": {"200": {"description": "OK"}}})
            if assertion["pointer"].endswith("/operationId"):
                operation["operationId"] = assertion["value"]
            else:
                operation["parameters"][1] = copy.deepcopy(assertion["value"])
        return spec

    def test_confluence_default_removals_preserve_label_filter_values(self):
        from openapi_schema_validator import OAS30Validator
        source = {"patches": ["maintenance/patches/confluence-v2.json"]}
        original = self.confluence_label_fixture()
        raw = json.dumps(original).encode()
        self.assertTrue(update.validate_document(original))
        result, steps = update.prepare_document(source, raw)
        expected = copy.deepcopy(original)
        for path in expected["paths"].values():
            del path["get"]["parameters"][1]["schema"]["default"]
        self.assertEqual(result, expected)
        self.assertEqual(update.validate_document(result), [])
        for path, item in result["paths"].items():
            old_parameter = original["paths"][path]["get"]["parameters"][1]
            parameter = item["get"]["parameters"][1]
            self.assertIs(parameter["required"], False)
            self.assertEqual((parameter["name"], parameter["in"]), ("prefix", "query"))
            a, b = OAS30Validator(old_parameter["schema"]), OAS30Validator(parameter["schema"])
            for instance, valid in (("my", True), ("team", True), ("my, team", False),
                                    ("", False), ("global", False), (None, False),
                                    (["my", "team"], False), (0, False)):
                self.assertEqual(a.is_valid(instance), valid)
                self.assertEqual(b.is_valid(instance), valid)
        self.assertEqual(json.loads(raw), original)
        self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])

    def test_confluence_recipe_rejects_vendor_default_and_contract_corrections(self):
        source = {"patches": ["maintenance/patches/confluence-v2.json"]}
        original = self.confluence_label_fixture()
        for path in original["paths"]:
            for change in ("removed", "valid-default", "expanded-enum", "array", "required", "identity"):
                spec = copy.deepcopy(original)
                operation = spec["paths"][path]["get"]
                parameter = operation["parameters"][1]
                if change == "removed":
                    del parameter["schema"]["default"]
                elif change == "valid-default":
                    parameter["schema"]["default"] = "my"
                elif change == "expanded-enum":
                    parameter["schema"]["enum"].append("my, team")
                elif change == "array":
                    parameter["schema"] = {"type": "array", "items": {"type": "string"},
                                           "default": ["my", "team"]}
                elif change == "required":
                    parameter["required"] = True
                else:
                    operation["operationId"] = "changed-contract"
                raw = json.dumps(spec).encode()
                with self.subTest(path=path, change=change), self.assertRaisesRegex(ValueError, "review recipe"):
                    update.prepare_document(source, raw)
                self.assertEqual(json.loads(raw), spec)

    def test_zendesk_reference_dependency_retains_positive_and_negative_constraints(self):
        import itertools
        from jsonschema import Draft4Validator
        source = {"patches": ["maintenance/patches/zendesk-conversations.json"]}
        spec = zendesk_conversations_fixture()
        raw = json.dumps(spec).encode()
        self.assertTrue(update.validate_document(spec))
        result, steps = update.prepare_document(source, raw)
        self.assertEqual(update.validate_document(result), [])
        original = spec["components"]["schemas"]["reference"]
        compatible = result["components"]["schemas"]["reference"]
        expected = copy.deepcopy(original)
        del expected["dependencies"]
        expected["anyOf"] = [{"not": {"required": ["sourceType"]}}, {"required": ["source"]}]
        self.assertEqual(compatible, expected)
        outcomes = []
        absent = object()
        for source_type, source_value in itertools.product([absent, "Page", None, 42],
                                                          [absent, "1234", None, 42]):
            instance = {"uri": "https://example.com/article"}
            if source_type is not absent:
                instance["sourceType"] = source_type
            if source_value is not absent:
                instance["source"] = source_value
            a = Draft4Validator(original).is_valid(instance)
            b = Draft4Validator(compatible).is_valid(instance)
            self.assertEqual(a, b, instance)
            outcomes.append(a)
        self.assertEqual(sum(outcomes), 3)
        self.assertEqual(len(outcomes) - sum(outcomes), 13)
        validator = Draft4Validator(compatible)
        self.assertFalse(validator.is_valid({"uri": "https://example.com", "sourceType": "Page"}))
        self.assertFalse(validator.is_valid({"sourceType": "Page", "source": "1234"}))
        self.assertFalse(validator.is_valid({"uri": "https://example.com", "title": "x" * 129}))
        self.assertEqual(json.loads(raw), spec)
        self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])

    def test_zendesk_filter_requirement_matches_documented_email_lookup(self):
        from jsonschema import Draft4Validator
        spec = zendesk_conversations_fixture()
        result, _ = update.prepare_document({"patches": ["maintenance/patches/zendesk-conversations.json"]},
                                             json.dumps(spec).encode())
        old = spec["components"]["parameters"]["userFilterQuery"]
        new = result["components"]["parameters"]["userFilterQuery"]
        expected = copy.deepcopy(old)
        del expected["schema"]["properties"]["identities.email"]["required"]
        expected["schema"]["required"] = ["identities.email"]
        self.assertEqual(new, expected)
        self.assertIs(new["required"], True)
        self.assertEqual((new["style"], new["explode"]), ("deepObject", True))
        validator = Draft4Validator(new["schema"])
        for instance in ({}, {"profile.email": "sue@example.org"}, {"identities.email": None},
                         {"identities.email": 42}):
            self.assertFalse(validator.is_valid(instance), instance)
        self.assertTrue(validator.is_valid({"identities.email": "sue@example.org"}))
        # The vendor declares string, not an email format, pattern or minimum length.
        self.assertTrue(validator.is_valid({"identities.email": ""}))

    def test_zendesk_recipe_refuses_vendor_fixes_and_changed_contracts(self):
        source = {"patches": ["maintenance/patches/zendesk-conversations.json"]}
        original = zendesk_conversations_fixture()
        complete_fix, _ = update.prepare_document(source, json.dumps(original).encode())
        changed_dependency = copy.deepcopy(original)
        changed_dependency["components"]["schemas"]["reference"]["dependencies"] = {"source": ["sourceType"]}
        changed_uri = copy.deepcopy(original)
        changed_uri["components"]["schemas"]["reference"]["required"] = []
        fixed_filter = copy.deepcopy(original)
        fixed_filter["components"]["parameters"]["userFilterQuery"] = copy.deepcopy(
            complete_fix["components"]["parameters"]["userFilterQuery"])
        optional_filter = copy.deepcopy(original)
        optional_filter["components"]["parameters"]["userFilterQuery"]["required"] = False
        changed_contract = copy.deepcopy(original)
        changed_contract["paths"]["/v2/apps/{appId}/users"]["get"]["description"] = "Lists all users."
        for changed in (complete_fix, changed_dependency, changed_uri, fixed_filter,
                        optional_filter, changed_contract):
            before = copy.deepcopy(changed)
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "assertion changed; review recipe"):
                update.prepare_document(source, json.dumps(changed).encode())
            self.assertEqual(changed, before)

    def test_yaml_equals_keys_and_values_match_json_and_roundtrip(self):
        raw = b"""openapi: 3.1.0
info: {title: Equals, version: '1'}
paths: {}
components:
  schemas:
    Query:
      type: object
      properties:
        =: {type: string, default: =}
      required: [=]
      example: {=: =}
"""
        expected = {"openapi": "3.1.0", "info": {"title": "Equals", "version": "1"},
                    "paths": {}, "components": {"schemas": {"Query": {
                        "type": "object", "properties": {"=": {"type": "string", "default": "="}},
                        "required": ["="], "example": {"=": "="}}}}}
        parsed = update.parse(raw)
        self.assertEqual(parsed, update.parse(json.dumps(expected).encode()))
        self.assertEqual(update.validate_document(parsed), [])
        self.assertEqual(update.parse(update.serialize_document(parsed).encode()), expected)
        invalid = copy.deepcopy(parsed)
        invalid["components"]["schemas"]["Query"]["properties"]["="]["default"] = False
        self.assertTrue(update.validate_document(invalid))
        with self.assertRaisesRegex(ValueError, "Import blocked"):
            update.import_document({"target": "APIs/example.com/1/openapi.yaml"}, invalid,
                                   {"url": "https://example.com/spec.yaml"}, None)

    def test_yaml12_integer_and_sexagesimal_resolution_preserves_vendor_strings(self):
        raw = b"""openapi: 3.1.0
info: {title: Scalars, version: '1'}
paths: {}
x-values: [1:10, 012, -012, +012, 0o12, 0x12, +0o12, 1:10.5, -.5, .5e2, 3.e2]
"""
        spec = update.parse(raw)
        self.assertEqual(spec["x-values"], ["1:10", 12, -12, 12, 10, 18, "+0o12", "1:10.5", -.5, 50., 300.])
        self.assertEqual([type(v) for v in spec["x-values"]],
                         [str, int, int, int, int, int, str, str, float, float, float])
        spec["x-strings"] = ["012", "0o12", "0x12", "+012", "1:10", "=", "-.5", ".5e2", "3.e2"]
        self.assertEqual(update.parse(update.serialize_document(spec).encode()), spec)
        # Parser configuration must not mutate PyYAML's global safe loader.
        import yaml
        self.assertEqual(yaml.safe_load("1:10"), 70)
        self.assertEqual(yaml.safe_load("012"), 10)

    def test_equals_implicit_resolution_does_not_accept_explicit_unknown_tags(self):
        import yaml
        raw = b"openapi: 3.1.0\ninfo: {title: Tagged, version: '1'}\npaths: {}\nx-value: !!value '='\n"
        with self.assertRaises(yaml.constructor.ConstructorError):
            update.parse(raw)

    def test_curated_import_is_reproducible_across_process_hash_seeds(self):
        script = '''import hashlib, update
from test_update import document
old = document()
old["info"].update({k: "curated" for k in sorted(update.CURATION)})
metadata = {"url": "https://vendor.example/spec.json", "revision": "abc", "sha256": "def", "fetched_at": "today"}
result = update.import_document({"target": "APIs/example.com/1.0/openapi.yaml"}, document(), metadata, old)
print(hashlib.sha256(update.serialize_document(result).encode()).hexdigest())
'''
        outputs = [subprocess.check_output([os.sys.executable, "-c", script],
                                           cwd=Path(update.__file__).parent,
                                           env={**os.environ, "PYTHONHASHSEED": seed})
                   for seed in ("1", "42", "123")]
        self.assertEqual(len(set(outputs)), 1)

    def test_fixed_version_schema_and_security_changes_are_detected(self):
        old = document()
        new = copy.deepcopy(old)
        new["components"]["parameters"]["Id"]["schema"]["minLength"] = 2
        self.assertEqual(update.compare(old, new)["status"], "changed")
        new = copy.deepcopy(old)
        new["security"] = []
        self.assertEqual(update.compare(old, new)["status"], "changed")

    def test_key_order_is_not_a_change(self):
        old = document()
        new = dict(reversed(list(old.items())))
        self.assertEqual(update.compare(old, new)["status"], "matches_source")

    def test_undefined_security_scheme_blocks_validation_and_import(self):
        spec = document()
        spec["paths"]["/items/{id}"]["get"]["security"] = [{"oauth2": ["items:read"]}]
        # The library's structural validation alone does not reject this name.
        update.validate(spec)
        self.assertTrue(any("Undefined security scheme oauth2" in error
                            for error in update.validate_document(spec)))
        with self.assertRaisesRegex(ValueError, "Undefined security scheme oauth2"):
            update.import_document({"target": "APIs/example.com/1.0/openapi.yaml"}, spec,
                                   {"url": "https://example.com/spec.json", "sha256": "test"}, None)

    def test_security_names_at_global_referenced_path_callback_and_webhook_locations(self):
        spec = document()
        spec["security"] = [{"GlobalMissing": []}]
        spec["components"]["pathItems"] = {"x-Named": {"get": {
            "responses": {"200": {"description": "OK"}}, "security": [{"PathMissing": []}]}}}
        spec["paths"]["/alias"] = {"$ref": "#/components/pathItems/x-Named"}
        spec["webhooks"] = {"change": {"post": {
            "responses": {"200": {"description": "OK"}}, "security": [{"WebhookMissing": []}]}}}
        spec["components"]["callbacks"] = {"Notify": {"{$request.query.url}": {"post": {
            "responses": {"200": {"description": "OK"}}, "security": [{"CallbackMissing": []}]}}}}
        spec["paths"]["/items/{id}"]["get"]["callbacks"] = {
            "notify": {"$ref": "#/components/callbacks/Notify"}}
        errors = update.security_requirement_errors(spec)
        for name in ("GlobalMissing", "PathMissing", "WebhookMissing", "CallbackMissing"):
            self.assertTrue(any("Undefined security scheme " + name in error for error in errors))
        self.assertEqual(len(errors), 4)

    def test_defined_security_alternatives_anonymous_and_payload_names_are_accepted(self):
        spec = document()
        spec["components"]["securitySchemes"] = {
            "Key": {"type": "apiKey", "in": "header", "name": "X-Key"},
            "Alias": {"$ref": "#/components/securitySchemes/Key"}}
        spec["security"] = [{"Key": []}, {}]
        spec["paths"]["/items/{id}"]["get"]["security"] = [{"Alias": []}]
        spec["components"]["schemas"]["Payload"] = {"type": "object", "properties": {
            "security": {"type": "array"}}, "example": {"security": [{"PayloadName": []}]}}
        spec["x-config"] = {"security": [{"ExtensionName": []}]}
        self.assertEqual(update.validate_document(spec), [])
        spec["paths"]["/items/{id}"]["get"]["security"] = []
        self.assertEqual(update.validate_document(spec), [])

    def test_recursive_callback_security_traversal_terminates_and_aggregates(self):
        spec = document()
        spec["components"]["pathItems"] = {"Recursive": {"post": {
            "responses": {"200": {"description": "OK"}}, "security": [{"Missing": []}],
            "callbacks": {"again": {"{$request.query.url}": {
                "$ref": "#/components/pathItems/Recursive"}}}}}}
        spec["paths"]["/other"] = {"get": {
            "responses": {"200": {"description": "OK"}}, "security": [{"Missing": []}]}}
        errors = update.security_requirement_errors(spec)
        self.assertEqual(len(errors), 1)
        self.assertIn("2 requirement(s)", errors[0])

    def test_security_traversal_failure_is_an_import_blocker(self):
        spec = document()
        spec["paths"]["/bad"] = {"$ref": "#/components/pathItems/Missing"}
        self.assertTrue(any("Security requirement traversal" in error
                            for error in update.validate_document(spec)))

    def test_curation_survives_without_perpetual_drift(self):
        old = document()
        old["info"].update({key: "curated" for key in update.CURATION})
        old["info"]["contact"] = {"x-twitter": "test"}
        old["info"]["x-conversion"] = ["Previous snapshot"]
        old["externalDocs"] = {"url": "https://example.com"}
        old["tags"] = [{"name": "curated"}, {"name": "vendor", "description": "curated description"}]
        new = document()
        new["tags"] = [{"name": "vendor"}, {"name": "new"}]
        result = update.preserve_curation(old, new)
        for key in update.CURATION:
            self.assertEqual(result["info"][key], old["info"][key])
        self.assertEqual(result["info"]["contact"]["x-twitter"], "test")
        self.assertEqual(result["externalDocs"], old["externalDocs"])
        self.assertEqual(len(result["tags"]), 3)
        self.assertEqual(update.compare(result, new)["status"], "matches_source")
        new["tags"][0]["description"] = "Changed by vendor"
        self.assertEqual(update.compare(result, new)["status"], "changed")

    def test_new_version_directory_and_unsafe_versions(self):
        source = {"target": "APIs/example.com/service/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor"}
        self.assertEqual(str(update.destination(source, document("2.0"))),
                         "APIs/example.com/service/2.0/openapi.yaml")
        for version in ("", "..", "../escape", "2026/10"):
            with self.assertRaises(ValueError):
                update.destination(source, document(version))

    def test_stable_directory_policy_refreshes_in_place_and_keeps_guards(self):
        source = {"target": "APIs/example.com/v2/openapi.yaml", "provider": "example.com",
                  "version_policy": "stable_directory"}
        for version in ("v2-20261008-2ab2a03735", "v2-20261009-0000000000"):
            self.assertEqual(str(update.destination(source, document(version))), source["target"])
        for version in ("", "..", "2026/10"):
            with self.assertRaises(ValueError):
                update.destination(source, document(version))
        with self.assertRaises(ValueError):
            update.destination(dict(source, target="APIs/other.com/v2/openapi.yaml"), document("v2"))
        with self.assertRaises(ValueError):
            update.destination(dict(source, version_policy="guess"), document("v2"))

    def test_moneybird_recipe_removes_only_invalid_boolean_default_and_stops_on_vendor_fix(self):
        source = {"patches": ["maintenance/patches/moneybird.json"]}
        spec = {"openapi": "3.1.0", "info": {"title": "Moneybird", "version": "v2-x"}, "paths": {},
                "components": {"schemas": {"base_contact_response": {"type": "object", "properties": {
                    "is_trusted": {"type": "boolean", "default": "default"}}}}}}
        self.assertTrue(update.validate_document(spec))
        result, steps = update.prepare_document(source, json.dumps(spec).encode())
        self.assertEqual(result["components"]["schemas"]["base_contact_response"]["properties"]["is_trusted"],
                         {"type": "boolean"})
        self.assertEqual(update.validate_document(result), [])
        for fixed in ({"type": "boolean"}, {"type": "boolean", "default": False}, {"type": "string", "default": "default"}):
            changed = copy.deepcopy(spec)
            changed["components"]["schemas"]["base_contact_response"]["properties"]["is_trusted"] = fixed
            with self.subTest(fixed=fixed), self.assertRaises((ValueError, KeyError)):
                update.prepare_document(source, json.dumps(changed).encode())

    def test_default_removal_recipes_replay_exactly_and_stop_on_vendor_fix(self):
        for name in ("openai", "klaviyo", "jira-platform"):
            source = {"patches": ["maintenance/patches/" + name + ".json"]}
            recipe = json.loads((update.ROOT / source["patches"][0]).read_text())
            spec = {"openapi": "3.0.3", "info": {"title": name, "version": "1"}, "paths": {}}
            for operation in recipe["operations"]:
                parts = [p.replace("~1", "/").replace("~0", "~") for p in operation["pointer"][2:].split("/")]
                node = spec
                for part in parts[:-2]:
                    node = node.setdefault(part, {})  # minimal skeleton; dict keys stand in for indices
                node[parts[-2]] = dict(operation["context"], **{parts[-1]: operation["from"]})
            result, steps = update.prepare_document(source, json.dumps(spec).encode())
            for operation in recipe["operations"]:
                with self.assertRaises(KeyError):
                    update.pointer(result, operation["pointer"])
            self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])
            fixed = json.loads(json.dumps(spec))
            first = recipe["operations"][0]["pointer"]
            parent = update.pointer(fixed, first.rsplit("/", 1)[0])
            del parent[first.rsplit("/", 1)[1]]
            with self.subTest(recipe=name), self.assertRaisesRegex(ValueError, "source value changed"):
                update.prepare_document(source, json.dumps(fixed).encode())

    def test_volatile_examples_opt_in_ignores_only_example_churn(self):
        source = {"volatile_examples": True, "version_policy": "stable_directory"}
        old = document("v2-a")
        old["components"]["schemas"]["Thing"] = {"type": "object", "example": {"id": "1"},
                                                 "properties": {"example": {"type": "string"}}}
        old["paths"]["/items/{id}"]["get"]["responses"]["200"]["content"] = {
            "application/json": {"examples": {"one": {"value": {"id": "1", "created_at": "2026-01-01"}}}}}
        churn = copy.deepcopy(old)
        churn["info"]["version"] = "v2-b"
        churn["components"]["schemas"]["Thing"]["example"] = {"id": "2"}
        churn["paths"]["/items/{id}"]["get"]["responses"]["200"]["content"]["application/json"]["examples"]["one"]["value"]["id"] = "2"
        result = update.compare(old, churn, source)
        self.assertEqual(result["status"], "matches_source")
        self.assertTrue(result["volatile_example_changes_only"])
        self.assertEqual(update.compare(old, churn)["status"], "changed")  # strict without opt-in
        self.assertEqual(update.compare(old, churn, dict(source, version_policy="vendor"))["status"], "changed")
        real = copy.deepcopy(churn)
        real["components"]["schemas"]["Thing"]["properties"]["example"]["type"] = "integer"  # a property named example
        self.assertEqual(update.compare(old, real, source)["status"], "changed")
        real = copy.deepcopy(churn)
        real["paths"]["/items/{id}"]["get"]["responses"]["200"]["description"] = "Changed"
        self.assertEqual(update.compare(old, real, source)["status"], "changed")

    def test_mollie_recipe_drops_only_reference_object_schema_siblings(self):
        source = {"patches": ["maintenance/patches/mollie.json"]}
        recipe = json.loads((update.ROOT / source["patches"][0]).read_text())
        operation = recipe["operations"][0]
        self.assertEqual(len(recipe["operations"]), 35)
        self.assertTrue(all(o["pointer"].endswith("/schema") and set(o["context"]) == {"$ref"} for o in recipe["operations"]))
        ref = operation["context"]["$ref"]
        target = ref.rsplit("/", 1)[1]
        parts = [p.replace("~1", "/").replace("~0", "~") for p in operation["pointer"][2:].split("/")]
        spec = {"openapi": "3.1.0", "info": {"title": "Mollie", "version": "1.0.0"}, "paths": {},
                "components": {"parameters": {target: {"name": "from", "in": "query", "schema": {"type": "string"}}}}}
        node = spec
        for part in parts[:-3]:
            node = node.setdefault(part, {})
        node[parts[-3]] = [{}] * int(parts[-2]) + [{"$ref": ref, "schema": operation["from"]}] if parts[-3] == "parameters" else node
        single = dict(recipe, operations=[operation])
        path = update.ROOT / "maintenance/patches/mollie.json"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "maintenance/patches").mkdir(parents=True)
            (root / "maintenance/patches/mollie.json").write_text(json.dumps(single))
            with patch.object(update, "ROOT", root):
                result, _ = update.prepare_document(source, json.dumps(spec).encode())
                self.assertEqual(update.pointer(result, operation["pointer"].rsplit("/", 1)[0]), {"$ref": ref})
                fixed = json.loads(json.dumps(spec))
                del update.pointer(fixed, operation["pointer"].rsplit("/", 1)[0])["schema"]
                with self.assertRaisesRegex(ValueError, "source value changed"):
                    update.prepare_document(source, json.dumps(fixed).encode())

    def test_paypal_representation_recipes_replay_exactly_and_stop_on_vendor_fix(self):
        names = ("catalogs-products", "notifications-webhooks", "payment-experience-web-profiles",
                 "customer-partner-referrals", "invoicing", "payments")
        for name in names:
            source = {"patches": ["maintenance/patches/paypal-" + name + ".json"]}
            recipe = json.loads((update.ROOT / source["patches"][0]).read_text())
            spec = {"openapi": "3.0.3", "info": {"title": name, "version": "1"}, "paths": {}}
            for operation in recipe["operations"]:
                parts = [p.replace("~1", "/").replace("~0", "~") for p in operation["pointer"][2:].split("/")]
                node = spec
                for part in parts[:-2]:
                    node = node.setdefault(part, {})
                node.setdefault(parts[-2], {}).update(dict(operation["context"], **{parts[-1]: operation["from"]}))
            result, _ = update.prepare_document(source, json.dumps(spec).encode())
            for operation in recipe["operations"]:
                if operation.get("remove"):
                    with self.assertRaises(KeyError):
                        update.pointer(result, operation["pointer"])
                else:
                    self.assertEqual(update.pointer(result, operation["pointer"]), operation["value"])
            fixed = json.loads(json.dumps(result))  # an already-corrected vendor source stops replay
            with self.subTest(recipe=name), self.assertRaises((ValueError, KeyError)):
                update.prepare_document(source, json.dumps(fixed).encode())

    def test_array_pointer_escaped_tokens_and_referenced_parameters(self):
        spec = document()
        self.assertEqual(update.pointer(spec, "#/components/schemas/Choice/oneOf/1"), {"type": "null"})
        self.assertEqual(update.pointer({"a/b": {"~": ["yes"]}}, "#/a~1b/~0/0"), "yes")
        with self.assertRaises(ValueError):
            update.pointer(spec, "#/components/schemas/Choice/oneOf/-1")
        self.assertEqual(update.validate_document(spec), [])
        spec["components"]["parameters"]["Id"]["name"] = "wrong"
        self.assertTrue(any("mismatched" in e for e in update.validate_document(spec)))

    def test_missing_responses_and_broken_references_fail(self):
        spec = document()
        spec["paths"]["/items/{id}"]["get"]["responses"] = {}
        self.assertTrue(update.validate_document(spec))
        spec = document()
        del spec["components"]["parameters"]["Id"]
        self.assertTrue(update.validate_document(spec))

    def test_external_schema_refs_block_but_snippets_and_example_data_do_not(self):
        spec = document()
        spec["x-fern-examples"] = [{"code": {"$ref": "snippet.ts"}}]
        spec["components"]["schemas"]["Choice"]["example"] = {"$ref": "literal payload"}
        self.assertEqual(update.validate_document(spec), [])
        spec["components"]["schemas"]["x-real-schema"] = {"$ref": "common.yaml#/Thing"}
        self.assertTrue(any("bundling" in e for e in update.validate_document(spec)))

    def test_timestamp_versions_remain_strings_and_html_is_rejected(self):
        raw = b'openapi: 3.1.0\ninfo:\n  title: Test\n  version: 2026-10-02\npaths: {}\n'
        self.assertEqual(update.parse(raw)["info"]["version"], "2026-10-02")
        with self.assertRaises(ValueError):
            update.parse(b"<html>Not Found</html>")

    def test_json_and_yaml_preserve_boolean_like_property_names(self):
        spec = document()
        spec["components"]["schemas"]["Workflow"] = {"type": "object", "properties": {
            "on": {"type": "string"}, "off": {"type": "string"}, "yes": {"type": "string"}}}
        for raw in (json.dumps(spec).encode(),
                    b'openapi: 3.1.0\ninfo: {title: Test, version: "1"}\npaths: {}\n'
                    b'components:\n  schemas:\n    Workflow:\n      properties:\n'
                    b'        on: {type: string}\n        off: {type: string}\n        yes: {type: string}\n'):
            parsed = update.parse(raw)
            self.assertEqual(set(parsed["components"]["schemas"]["Workflow"]["properties"]), {"on", "off", "yes"})
            update.canonical(parsed)

    def test_import_records_provenance_without_mutating_source(self):
        new = document()
        before = copy.deepcopy(new)
        metadata = {"url": "https://vendor.example/openapi.json", "revision": "abc",
                    "sha256": "def", "fetched_at": "today"}
        source = {"target": "APIs/example.com/1.0/openapi.yaml"}
        result = update.import_document(source, new, metadata, None)
        self.assertEqual(new, before)
        self.assertIn("abc", result["info"]["x-conversion"][0])
        self.assertEqual(result["info"]["x-origin"][0]["version"], "3.1")
        with self.assertRaises(ValueError):
            update.import_document({**source, "import_blocker": "Not bundled"}, new, metadata, None)

    def test_repeat_refresh_records_actual_curation_baseline_instead_of_manifest_fallback(self):
        source = {"id": "test", "target": "APIs/example.com/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        old = document("2.0")
        old["info"]["x-logo"] = {"url": "https://example.com/current-logo.svg"}
        new = document("2.0")
        new["info"]["description"] = "Vendor clarification"
        raw = json.dumps(new).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            manifest.write_text(json.dumps({"schema_version": 1, "sources": [source]}))
            with patch.object(update, "ROOT", root), patch.object(update, "load_sources", return_value=[source]), \
                 patch.object(update, "fetch", return_value=(raw, metadata)), \
                 patch.object(update, "stored", return_value=old):
                self.assertEqual(update.main(["import", "--source", "test", "--manifest", str(manifest),
                                              "--cache", str(root / "cache")]), 0)
            result = update.parse((root / "APIs/example.com/2.0/openapi.yaml").read_bytes())
        self.assertEqual(result["info"]["x-logo"], old["info"]["x-logo"])
        self.assertIn("Preserved existing APIs.guru curation metadata from APIs/example.com/2.0/openapi.yaml.",
                      result["info"]["x-conversion"])

    def test_new_release_advances_reviewed_baseline_for_the_next_release(self):
        source = {"id": "test", "target": "APIs/example.com/1.740/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        old = document("1.740")
        old["info"]["x-logo"] = {"url": "https://example.com/current.svg"}
        new = document("1.762")
        new["paths"] = {"/new": {"post": {"responses": {"200": {"description": "OK"}}}}}
        raw = json.dumps(new).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            original = json.dumps({"schema_version": 1, "sources": [source]}, indent=4) + "\n"
            manifest.write_text(original)
            def stored(path, base):
                if path == source["target"]:
                    return old
                output = root / path
                return update.parse(output.read_bytes()) if output.exists() else None
            with patch.object(update, "ROOT", root), patch.object(update, "stored", side_effect=stored), \
                 patch.object(update, "fetch", return_value=(raw, metadata)):
                update.main(["import", "--source", "test", "--manifest", str(manifest),
                             "--cache", str(root / "cache")])
                current = update.load_sources(manifest)[0]
                self.assertEqual(current["target"], "APIs/example.com/1.762/openapi.yaml")
                self.assertEqual(manifest.read_text(), original.replace("1.740", "1.762"))
                imported = stored(current["target"], "base")
                self.assertEqual(imported["info"]["x-logo"], old["info"]["x-logo"])
                self.assertIn(source["target"], imported["info"]["x-conversion"][-2])
                upcoming = document("1.800")
                upcoming["paths"] = {"/next": new["paths"]["/new"]}
                with patch.object(update, "fetch", return_value=(json.dumps(upcoming).encode(), metadata)):
                    result = update.audit(current, "base", root / "cache")
                self.assertEqual(result["baseline"], current["target"])
                self.assertEqual(result["removed_paths"], ["/new"])
                self.assertEqual(result["added_paths"], ["/next"])

    def test_initial_swagger_baseline_preserves_curation_then_yields_to_current_release(self):
        source = {"id": "test", "target": "APIs/example.com/2.0/openapi.yaml",
                  "initial_baseline": "APIs/example.com/1.0/swagger.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        legacy = {"swagger": "2.0", "info": {"title": "Community description", "version": "1.0",
                   "x-logo": {"url": "https://example.com/logo.svg"}, "x-unofficialSpec": True},
                  "paths": {"/legacy": {"get": {"responses": {"200": {"description": "OK"}}}}},
                  "externalDocs": {"url": "https://example.com/docs"}}
        new = document("2.0")
        raw = json.dumps(new).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            manifest.write_text(json.dumps({"schema_version": 1, "sources": [source]}))
            legacy_file = root / source["initial_baseline"]
            legacy_file.parent.mkdir(parents=True)
            legacy_file.write_text(json.dumps(legacy))
            original = legacy_file.read_bytes()
            def stored(path, base):
                output = root / path
                return update.parse(output.read_bytes()) if output.exists() else None
            with patch.object(update, "ROOT", root), patch.object(update, "stored", side_effect=stored), \
                    patch.object(update, "fetch", return_value=(raw, metadata)):
                self.assertEqual(update.main(["import", "--source", "test", "--manifest", str(manifest),
                                              "--cache", str(root / "cache")]), 0)
                imported = stored(source["target"], "base")
                self.assertEqual(imported["info"]["x-logo"], legacy["info"]["x-logo"])
                self.assertEqual(imported["externalDocs"], legacy["externalDocs"])
                self.assertNotIn("x-unofficialSpec", imported["info"])
                self.assertTrue(any(source["initial_baseline"] in s for s in imported["info"]["x-conversion"]))
                self.assertEqual(legacy_file.read_bytes(), original)
                self.assertEqual(update.baseline(source, new, "base"), (source["target"], imported))
                self.assertEqual(update.baseline(source, document("3.0"), "base"),
                                 (source["target"], imported))

    def test_initial_baseline_rejects_unsafe_paths_and_missing_history(self):
        source = {"id": "test", "target": "APIs/example.com/2.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor"}
        for path in ("APIs/other.com/1.0/swagger.yaml", "APIs/example.com/../1.0/swagger.yaml",
                     "/APIs/example.com/1.0/swagger.yaml", "APIs/example.com/1.0/spec.json",
                     "APIs//example.com/1.0/swagger.yaml", 42):
            with self.subTest(path=path), patch.object(update, "stored") as stored:
                with self.assertRaisesRegex(ValueError, "canonical spec path"):
                    update.baseline({**source, "initial_baseline": path}, document("2.0"), "base")
                stored.assert_not_called()
        with patch.object(update, "stored", return_value=None):
            with self.assertRaisesRegex(ValueError, "absent from the comparison tree"):
                update.baseline({**source, "initial_baseline": "APIs/example.com/1.0/swagger.yaml"},
                                document("2.0"), "base")

    def test_invalid_release_leaves_manifest_and_destination_untouched(self):
        source = {"id": "test", "target": "APIs/example.com/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        invalid = document("2.0")
        invalid["paths"]["/items/{id}"]["get"]["responses"] = {}
        raw = json.dumps(invalid).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            manifest.write_text(json.dumps({"schema_version": 1, "sources": [source]}))
            original = manifest.read_bytes()
            with patch.object(update, "ROOT", root), patch.object(update, "stored", return_value=None), \
                 patch.object(update, "fetch", return_value=(raw, metadata)):
                with self.assertRaisesRegex(ValueError, "Import blocked"):
                    update.main(["import", "--source", "test", "--manifest", str(manifest),
                                 "--cache", str(root / "cache")])
            self.assertEqual(manifest.read_bytes(), original)
            self.assertFalse((root / "APIs/example.com/2.0/openapi.yaml").exists())

    def test_manifest_change_guard_and_matching_release_target_repair(self):
        source = {"id": "test", "target": "APIs/example.com/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        raw = json.dumps(document("2.0")).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            manifest.write_text(json.dumps({"schema_version": 1, "sources": [{**source, "priority": "new"}]}))
            with self.assertRaisesRegex(ValueError, "configuration changed"):
                update.advance_target(manifest, source, Path("APIs/example.com/2.0/openapi.yaml"))
            manifest.write_text(json.dumps({"schema_version": 1, "sources": [source]}))
            with patch.object(update, "ROOT", root), patch.object(update, "stored", return_value=document("2.0")), \
                 patch.object(update, "fetch", return_value=(raw, metadata)):
                update.main(["import", "--source", "test", "--manifest", str(manifest),
                             "--cache", str(root / "cache")])
            self.assertEqual(update.load_sources(manifest)[0]["target"], "APIs/example.com/2.0/openapi.yaml")
            self.assertFalse((root / "APIs").exists())

    def test_concurrent_manifest_edit_during_validation_is_preserved(self):
        source = {"id": "test", "target": "APIs/example.com/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor",
                  "url": "https://vendor.example/api.json"}
        raw = json.dumps(document("2.0")).encode()
        metadata = {"url": source["url"], "sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "sources.json"
            original = json.dumps({"schema_version": 1, "sources": [source]})
            manifest.write_text(original)
            def validate(spec):
                manifest.write_text(original + "\n")
                return []
            with patch.object(update, "ROOT", root), patch.object(update, "stored", return_value=None), \
                 patch.object(update, "fetch", return_value=(raw, metadata)), \
                 patch.object(update, "validate_document", side_effect=validate):
                with self.assertRaisesRegex(ValueError, "Manifest changed during validation"):
                    update.main(["import", "--source", "test", "--manifest", str(manifest),
                                 "--cache", str(root / "cache")])
            self.assertEqual(manifest.read_text(), original + "\n")
            self.assertFalse((root / "APIs").exists())

    def test_failed_fetch_does_not_advance_success_and_subset_report_keeps_other_apis(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            report.write_text(json.dumps({"sources": [
                {"id": "one", "last_successful_fetch": "yesterday", "last_successful_validation": "yesterday"},
                {"id": "two", "status": "matches_source"}]}))
            results = [{"id": "one", "status": "failed", "checked_at": "today"}]
            with patch.object(update, "git", return_value=b"commit\n"):
                update.write_report(report, results, "origin/main")
            rows = {row["id"]: row for row in json.loads(report.read_text())["sources"]}
            self.assertEqual(rows["one"]["last_successful_fetch"], "yesterday")
            self.assertEqual(rows["one"]["last_successful_validation"], "yesterday")
            self.assertIn("two", rows)
            with patch.object(update, "fetch", side_effect=OSError("Network unavailable")):
                result = update.audit({"id": "one", "target": "APIs/example.com/1.0/openapi.yaml"},
                                      "origin/main", Path(directory))
            self.assertEqual(result["status"], "failed")
            self.assertNotIn("last_successful_fetch", result)

    def test_changed_referenced_content_is_detected_after_bundling(self):
        # Bundlers supply resolved documents to the same comparison function.
        old = document()
        new = document()
        new["components"]["schemas"]["Choice"]["oneOf"].append({"type": "integer"})
        self.assertEqual(update.compare(old, new)["status"], "changed")

    def test_existing_destination_is_preferred_after_version_bump(self):
        source = {"id": "test", "target": "APIs/example.com/1.0/openapi.yaml",
                  "provider": "example.com", "version_policy": "vendor"}
        raw = json.dumps(document("2.0")).encode()
        metadata = {"sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(update, "fetch", return_value=(raw, metadata)), \
                 patch.object(update, "stored", return_value=document("2.0")) as stored:
                result = update.audit(source, "origin/main", Path(directory))
            self.assertEqual(result["status"], "matches_source")
            stored.assert_called_once_with("APIs/example.com/2.0/openapi.yaml", "origin/main")

    def test_exact_patch_replay_provenance_and_source_preconditions(self):
        spec = document()
        spec["components"]["schemas"]["Flag"] = {"type": "boolean", "default": "false"}
        raw = json.dumps(spec).encode()
        recipe = {"schema_version": 1, "description": "Fixed a string boolean default.",
                  "operations": [{"pointer": "#/components/schemas/Flag/default", "from": "false",
                                  "value": False, "context": {"type": "boolean"}}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/flag.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(recipe))
            source = {"patches": ["maintenance/patches/flag.json"]}
            with patch.object(update, "ROOT", root):
                result, steps = update.prepare_document(source, raw)
                self.assertIs(result["components"]["schemas"]["Flag"]["default"], False)
                self.assertEqual(update.validate_document(result), [])
                self.assertEqual(json.loads(raw), spec)
                self.assertIn(update.sha256(path.read_bytes()), steps[0])
                imported = update.import_document(source, result, {
                    "url": "https://example.com/openapi.json", "sha256": update.sha256(raw),
                    "fetched_at": "today", "transformations": steps}, None)
                self.assertIn(steps[0], imported["info"]["x-conversion"])
                self.assertFalse(any("no API content patches" in s for s in imported["info"]["x-conversion"]))
                # A vendor fix or unrelated type change must require recipe review.
                for key, value in (("default", False), ("default", "true"), ("type", "string")):
                    changed = copy.deepcopy(spec)
                    changed["components"]["schemas"]["Flag"][key] = value
                    with self.assertRaisesRegex(ValueError, "review recipe"):
                        update.prepare_document(source, json.dumps(changed).encode())
                del spec["components"]["schemas"]["Flag"]["default"]
                with self.assertRaisesRegex(ValueError, "review recipe"):
                    update.prepare_document(source, json.dumps(spec).encode())

    def test_patch_types_duplicates_and_paths_fail_closed(self):
        spec = document()
        spec["components"]["schemas"]["Flag"] = {"type": "boolean", "default": False}
        recipe = {"schema_version": 1, "description": "Test",
                  "operations": [{"pointer": "#/components/schemas/Flag/default", "from": 0,
                                  "value": True, "context": {"type": "boolean"}}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/flag.json"
            path.parent.mkdir(parents=True)
            source = {"patches": ["maintenance/patches/flag.json"]}
            with patch.object(update, "ROOT", root):
                path.write_text(json.dumps(recipe))
                with self.assertRaisesRegex(ValueError, "source value changed"):
                    update.prepare_document(source, json.dumps(spec).encode())
                recipe["operations"][0]["from"] = False
                recipe["operations"][0]["value"] = False
                recipe["operations"].append(copy.deepcopy(recipe["operations"][0]))
                path.write_text(json.dumps(recipe))
                with self.assertRaisesRegex(ValueError, "duplicate patch pointer"):
                    update.prepare_document(source, json.dumps(spec).encode())
                with self.assertRaisesRegex(ValueError, "under maintenance/patches"):
                    update.prepare_document({"patches": ["../escape.json"]}, json.dumps(spec).encode())

    def test_patch_failure_retains_raw_snapshot_and_does_not_report_success(self):
        raw = json.dumps(document()).encode()
        metadata = {"sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            with patch.object(update, "fetch", return_value=(raw, metadata)), \
                 patch.object(update, "prepare_document", side_effect=ValueError("Review patch")):
                result = update.audit({"id": "test", "target": "APIs/example.com/1.0/openapi.yaml"},
                                      "origin/main", cache)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["last_successful_fetch"], "today")
            self.assertNotIn("last_successful_comparison", result)
            self.assertNotIn("last_successful_validation", result)
            self.assertEqual((cache / "test" / metadata["sha256"] / "source").read_bytes(), raw)

    def test_clickup_reference_assertions_preserve_constraints_and_reject_vendor_fix(self):
        source = {"patches": ["maintenance/patches/clickup-v3.json"]}
        recipe = json.loads((update.ROOT / source["patches"][0]).read_text())
        schemas = {entry["pointer"].rsplit("/", 1)[1]: copy.deepcopy(entry["value"])
                   for entry in recipe["assertions"]}
        spec = {"openapi": "3.0.0", "info": {"title": "Reference guard", "version": "1"},
                "paths": {}, "components": {"schemas": schemas}}
        raw = json.dumps(spec).encode()
        self.assertTrue(update.validate_document(spec))
        result, steps = update.prepare_document(source, raw)
        expected = copy.deepcopy(spec)
        del expected["components"]["schemas"]["PublicDocsCreateDocOptionsDto"]["properties"]["parent"]["default"]
        self.assertEqual(result, expected)
        self.assertEqual(update.validate_document(result), [])
        self.assertEqual(json.loads(raw), spec)
        self.assertIn(update.sha256((update.ROOT / source["patches"][0]).read_bytes()), steps[0])
        # The default's immediate siblings are unchanged by this valid vendor fix.
        fixed = copy.deepcopy(spec)
        fixed["components"]["schemas"]["PublicDocsParentDto"]["nullable"] = True
        self.assertEqual(update.validate_document(fixed), [])
        self.assertEqual(fixed["components"]["schemas"]["PublicDocsCreateDocOptionsDto"],
                         spec["components"]["schemas"]["PublicDocsCreateDocOptionsDto"])
        changed_required = copy.deepcopy(spec)
        changed_required["components"]["schemas"]["PublicDocsCreateDocOptionsDto"]["required"] = ["parent"]
        corrected_default = copy.deepcopy(spec)
        del corrected_default["components"]["schemas"]["PublicDocsCreateDocOptionsDto"]["properties"]["parent"]["default"]
        for changed in (fixed, changed_required, corrected_default):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "assertion changed; review recipe"):
                update.prepare_document(source, json.dumps(changed).encode())

    def test_patch_assertions_handle_escaped_array_pointers_and_json_types(self):
        spec = document()
        spec["x-context"] = {"a/b~c": [False]}
        recipe = {"schema_version": 1, "description": "Reviewed fixture",
                  "assertions": [{"pointer": "#/x-context/a~1b~0c/0", "value": False}],
                  "operations": [{"pointer": "#/info/title", "from": "Test API", "value": "Reviewed",
                                  "context": {"version": "1.0"}}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/fixture.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(recipe))
            with patch.object(update, "ROOT", root):
                result, _ = update.prepare_document({"patches": ["maintenance/patches/fixture.json"]}, json.dumps(spec).encode())
                self.assertEqual(result["info"]["title"], "Reviewed")
                for changed in (0, "false", None):
                    with self.subTest(value=changed):
                        spec["x-context"]["a/b~c"][0] = changed
                        with self.assertRaisesRegex(ValueError, "assertion changed; review recipe"):
                            update.prepare_document({"patches": ["maintenance/patches/fixture.json"]}, json.dumps(spec).encode())

    def test_patch_assertions_reject_malformed_missing_and_unknown_fields(self):
        spec = document()
        operation = {"pointer": "#/info/title", "from": "Test API", "value": "Reviewed",
                     "context": {"version": "1.0"}}
        assertion = {"pointer": "#/info/version", "value": "1.0"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/fixture.json"
            path.parent.mkdir(parents=True)
            with patch.object(update, "ROOT", root):
                for assertions in (None, {}, [], [None], [{"pointer": "#/info/version"}],
                                   [{**assertion, "extra": True}], [assertion, assertion],
                                   [{"pointer": "https://example.com/spec", "value": 1}],
                                   [{"pointer": "#/missing", "value": None}],
                                   [{"pointer": "#/components/schemas/Choice/oneOf/99", "value": {}}]):
                    recipe = {"schema_version": 1, "description": "Test", "operations": [operation],
                              "assertions": assertions}
                    path.write_text(json.dumps(recipe))
                    with self.subTest(assertions=assertions), self.assertRaises(ValueError):
                        update.prepare_document({"patches": ["maintenance/patches/fixture.json"]}, json.dumps(spec).encode())
                recipe = {"schema_version": 1, "description": "Test", "operations": [operation],
                          "assertoin": [assertion]}
                path.write_text(json.dumps(recipe))
                with self.assertRaisesRegex(ValueError, "Invalid patch recipe"):
                    update.prepare_document({"patches": ["maintenance/patches/fixture.json"]}, json.dumps(spec).encode())

    def test_reference_assertion_failure_retains_valid_vendor_source_in_audit(self):
        recipe_path = "maintenance/patches/clickup-v3.json"
        recipe = json.loads((update.ROOT / recipe_path).read_text())
        schemas = {entry["pointer"].rsplit("/", 1)[1]: copy.deepcopy(entry["value"])
                   for entry in recipe["assertions"]}
        schemas["PublicDocsParentDto"]["nullable"] = True
        spec = {"openapi": "3.0.0", "info": {"title": "Vendor corrected", "version": "1"},
                "paths": {}, "components": {"schemas": schemas}}
        self.assertEqual(update.validate_document(spec), [])
        raw = json.dumps(spec).encode()
        metadata = {"sha256": update.sha256(raw), "fetched_at": "today"}
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            with patch.object(update, "fetch", return_value=(raw, metadata)):
                result = update.audit({"id": "test", "target": "APIs/example.com/1/openapi.yaml",
                                       "patches": [recipe_path]}, "origin/main", cache)
            self.assertEqual(result["status"], "failed")
            self.assertIn("assertion changed; review recipe", result["error"])
            self.assertNotIn("last_successful_validation", result)
            self.assertNotIn("last_successful_comparison", result)
            self.assertEqual((cache / "test" / metadata["sha256"] / "source").read_bytes(), raw)

    def test_checked_removal_of_an_invalid_default_and_transformation_order(self):
        spec = document()
        spec["components"]["schemas"]["InvalidDefault"] = {
            "type": "string", "default": None, "description": "Vendor description"}
        recipe = {"schema_version": 1, "description": "Removed only an invalid null default.",
                  "operations": [{"pointer": "#/components/schemas/InvalidDefault/default", "from": None,
                                  "remove": True, "context": {"type": "string"}}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "maintenance/patches/default.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(recipe))
            source = {"patches": ["maintenance/patches/default.json"]}
            with patch.object(update, "ROOT", root):
                patched, steps = update.prepare_document(source, json.dumps(spec).encode())
                self.assertEqual(patched["components"]["schemas"]["InvalidDefault"], {
                    "type": "string", "description": "Vendor description"})
                self.assertEqual(update.validate_document(patched), [])
                metadata = {"url": "https://example.com/spec", "sha256": "hash", "fetched_at": "today",
                            "transformations": steps}
                result = update.import_document(source, patched, metadata, None)
                log = result["info"]["x-conversion"]
                self.assertLess(log.index(steps[0]), len(log) - 1)
                self.assertIn("Serialized", log[-1])


if __name__ == "__main__":
    unittest.main()
