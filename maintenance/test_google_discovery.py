"""Synthetic conversion regressions: no provider calls or real account data."""
import copy
import unittest

from openapi_schema_validator import OAS30Validator
from openapi_spec_validator import validate

import google_discovery as google


def source():
    return {
        "discoveryVersion": "v1", "protocol": "rest", "name": "invented", "version": "v1",
        "rootUrl": "https://invented.example/", "servicePath": "api/", "revision": "20261029",
        "title": "Invented test API", "description": "Synthetic descriptions only.",
        "parameters": {"prettyPrint": {"type": "boolean", "location": "query", "default": "true"}},
        "auth": {"oauth2": {"scopes": {"scope:invented:read": {"description": "Read invented objects"}}}},
        "schemas": {
            "Note": {"id": "Note", "type": "object", "properties": {
                "id": {"type": "string", "description": "Keep this property named id."},
                "name": {"type": "string", "readOnly": True},
                "child": {"$ref": "Note", "description": "Recursive metadata survives.", "readOnly": True},
                "value": {"type": "any"},
            }},
        },
        "resources": {"notes": {"methods": {
            "get": {
                "id": "invented.notes.get", "httpMethod": "GET", "path": "v1/{+name}",
                "flatPath": "v1/notes/{notesId}", "description": "Read an invented note.",
                "parameters": {"name": {"type": "string", "location": "path", "required": True,
                                         "pattern": "^notes/[^/]+$"}},
                "response": {"$ref": "Note"}, "scopes": ["scope:invented:read"],
            },
        }}},
    }


class GoogleDiscoveryTests(unittest.TestCase):
    def test_complete_oas_and_recursive_metadata(self):
        native = source()
        unchanged = copy.deepcopy(native)
        document = google.convert(native)
        validate(document)
        self.assertEqual(google.check(native, document)["operations"], 1)
        self.assertEqual(native, unchanged)
        note = document["components"]["schemas"]["Note"]
        self.assertIn("id", note["properties"])
        self.assertEqual(note["x-google-discovery-id"], "Note")
        self.assertEqual(note["properties"]["child"]["allOf"], [{"$ref": "#/components/schemas/Note"}])
        self.assertTrue(note["properties"]["child"]["readOnly"])
        self.assertEqual(document["servers"], [{"url": "https://invented.example/api"}])

    def test_resource_name_collisions_keep_every_method(self):
        native = source()
        native["resources"]["media"] = {"methods": {"download": {
            "id": "invented.media.download", "httpMethod": "GET", "path": "v1/{+name}",
            "flatPath": "v1/notes/{notesId}/attachments/{attachmentsId}",
            "parameters": {"name": {"type": "string", "location": "path", "required": True,
                                      "pattern": "^notes/[^/]+/attachments/[^/]+$"}},
            "response": {"$ref": "Note"}, "supportsMediaDownload": True,
        }}}
        document = google.convert(native)
        self.assertEqual(google.check(native, document)["operations"], 2)
        validate(document)
        media = document["paths"]["/v1/notes/{notesId}/attachments/{attachmentsId}"]["get"]
        self.assertEqual(media["responses"]["2XX"]["content"]["*/*"]["schema"], {"type": "string", "format": "binary"})
        expansion = media["x-google-discovery"]
        self.assertEqual(expansion["resourceNameBindings"], {"notesId": "name", "attachmentsId": "name"})
        self.assertEqual(expansion["resourceNameParameters"], native["resources"]["media"]["methods"]["download"]["parameters"])

    def test_singleton_resource_is_a_constant(self):
        native = source()
        method = native["resources"]["notes"]["methods"]["get"]
        method["flatPath"] = "v1/singleton"
        document = google.convert(native)
        operation = document["paths"]["/v1/singleton"]["get"]
        self.assertNotIn("parameters", operation)
        self.assertEqual(operation["x-google-discovery"]["resourceNameConstants"], {"name": "singleton"})
        google.check(native, document)

    def test_constraints_and_integer_precision_survive(self):
        native = source()
        method = native["resources"]["notes"]["methods"]["get"]
        method["parameters"]["limit"] = {"type": "integer", "location": "query", "minimum": "0",
                                          "maximum": "9223372036854775807", "default": "0", "format": "int64"}
        method["parameters"]["filter"] = {"type": "string", "location": "query", "pattern": "^invented-.*$"}
        document = google.convert(native)
        parameters = {p["name"]: p for p in document["paths"]["/v1/notes/{notesId}"]["get"]["parameters"]}
        self.assertEqual(parameters["limit"]["schema"], {"type": "integer", "minimum": 0,
                                                       "maximum": 9223372036854775807, "default": 0, "format": "int64"})
        self.assertEqual(parameters["filter"]["schema"]["pattern"], "^invented-.*$")
        self.assertIs(document["components"]["parameters"]["prettyPrint"]["schema"]["default"], True)
        validate(document)

    def test_oauth_flows_and_scopes_are_alternatives(self):
        document = google.convert(source())
        security = document["paths"]["/v1/notes/{notesId}"]["get"]["security"]
        self.assertEqual(security, [{"Oauth2": ["scope:invented:read"]}, {"Oauth2c": ["scope:invented:read"]}])

    def test_method_specific_annotations_and_enum_metadata_remain_explicit(self):
        native = {"type": "string", "enum": ["A", "B"], "enumDescriptions": ["First", "Second"],
                  "enumDeprecated": [False, True], "annotations": {"required": ["invented.notes.create"]}}
        result = google.schema(native)
        self.assertNotIn("required", result)
        self.assertEqual(result["x-google-annotations"], native["annotations"])
        self.assertEqual(result["x-google-enum-descriptions"], ["First", "Second"])
        self.assertEqual(result["x-google-enum-deprecated"], [False, True])

    def test_any_schema_accepts_all_json_types(self):
        converted = google.schema({"type": "any"})
        for value in [None, True, 7, 2.5, "invented", [], {}]:
            OAS30Validator(converted).validate(value)

    def test_duplicate_routes_or_ids_cannot_silently_overwrite(self):
        native = source()
        methods = native["resources"]["notes"]["methods"]
        methods["other"] = {**copy.deepcopy(methods["get"]), "id": "invented.other.get"}
        with self.assertRaisesRegex(ValueError, "collide"):
            google.convert(native)
        methods["other"]["id"] = methods["get"]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate method"):
            google.convert(native)

    def test_missing_or_unused_path_parameters_are_refused(self):
        native = source()
        method = native["resources"]["notes"]["methods"]["get"]
        method["parameters"]["unused"] = {"type": "string", "location": "path"}
        with self.assertRaisesRegex(ValueError, "inventory"):
            google.convert(native)
        del method["parameters"]["unused"]
        del method["parameters"]["name"]
        with self.assertRaisesRegex(ValueError, "inventory"):
            google.convert(native)

    def test_independent_inventory_catches_dropped_operations_and_refs(self):
        native = source()
        document = google.convert(native)
        del document["paths"]["/v1/notes/{notesId}"]["get"]
        with self.assertRaisesRegex(ValueError, "lost or invented methods"):
            google.check(native, document)
        document = google.convert(native)
        del document["components"]["schemas"]["Note"]
        with self.assertRaisesRegex(ValueError, "lost or invented schemas"):
            google.check(native, document)

    def test_request_media_protocols_and_unknown_metadata_are_preserved(self):
        native = source()
        method = native["resources"]["notes"]["methods"]["get"]
        method.update(request={"$ref": "Note", "parameterName": "invented"}, streamingType="SERVER_SIDE",
                      mediaUpload={"accept": ["image/*"], "protocols": {"simple": {"path": "/upload/v1/notes"}}})
        document = google.convert(native)
        operation = document["paths"]["/v1/notes/{notesId}"]["get"]
        self.assertEqual(operation["requestBody"]["content"]["application/json"]["schema"], {"$ref": "#/components/schemas/Note"})
        self.assertEqual(operation["x-google-discovery"]["mediaUpload"], method["mediaUpload"])
        self.assertEqual(operation["x-google-discovery"]["streamingType"], "SERVER_SIDE")
        self.assertEqual(operation["x-google-discovery"]["requestParameterName"], "invented")

    def test_invalid_native_default_is_not_repaired_or_hidden(self):
        native = source()
        native["schemas"]["Note"]["properties"]["choice"] = {"type": "string", "enum": ["A"], "default": "B"}
        document = google.convert(native)
        self.assertEqual(document["components"]["schemas"]["Note"]["properties"]["choice"]["default"], "B")
        with self.assertRaises(Exception):
            validate(document)

    def test_ref_is_also_a_legal_property_name_and_literal_default(self):
        native = source()
        native["schemas"]["Note"]["properties"]["$ref"] = {"type": "string"}
        validate(google.convert(native))
        native["schemas"]["Note"]["properties"]["config"] = {"type": "object", "default": '{"$ref":"literal data"}'}
        document = google.convert(native)
        # The independent inventory treats literal JSON data as data. The
        # third-party OAS validator currently misresolves a $ref in a default.
        self.assertEqual(google.check(native, document)["schemas"], 1)


if __name__ == "__main__":
    unittest.main()
