"""Exact source guards and independent native RE2/ECMA-262 witnesses."""
import copy
import re
import sys
import unittest

import re2
import regress
from openapi_schema_validator import OAS30Validator

import google_compatibility as compatibility


def fixture(service, version, operations):
    return {"name": service, "version": version, "resources": {"invented": {"methods": {
        str(index): {"id": name, "parameters": copy.deepcopy(parameters)}
        for index, (name, parameters) in enumerate(operations.items())
    }}}}


class GoogleCompatibilityTests(unittest.TestCase):
    def test_org_unit_default_correction_preserves_all_value_constraints(self):
        native = fixture("admin", "reports_v1", {name: {"orgUnitID": value} for name, value in compatibility.ORG_UNIT_PARAMETERS.items()})
        before = copy.deepcopy(native)
        result, notes = compatibility.prepare(native)
        self.assertEqual(native, before)
        self.assertEqual(len(notes), 1)
        for operation in result["resources"]["invented"]["methods"].values():
            parameter = operation["parameters"]["orgUnitID"]
            self.assertNotIn("default", parameter)
            self.assertEqual(parameter["x-google-discovery-default"], "")
            original = compatibility.ORG_UNIT_PARAMETERS[operation["id"]]
            self.assertEqual({k: v for k, v in parameter.items() if k != "x-google-discovery-default"},
                             {k: v for k, v in original.items() if k != "default"})
            validator = OAS30Validator({"type": "string", "pattern": parameter["pattern"]})
            for value in ["id:abc", "id:12", "", "invalid", "id:UPPER"]:
                self.assertEqual(validator.is_valid(value), bool(re2.search(original["pattern"], value)))

    def test_vendor_fixes_or_other_node_changes_require_review(self):
        for field, value in [("default", "id:fixed"), ("pattern", ".*"), ("description", "Changed by vendor")]:
            native = fixture("admin", "reports_v1", {name: {"orgUnitID": original} for name, original in compatibility.ORG_UNIT_PARAMETERS.items()})
            native["resources"]["invented"]["methods"]["0"]["parameters"]["orgUnitID"][field] = value
            with self.assertRaisesRegex(ValueError, "Review changed"):
                compatibility.prepare(native)
        native = fixture("pagespeedonline", "v5", {"pagespeedonline.pagespeedapi.runpagespeed": {"url": compatibility.PAGESPEED_PARAMETER}})
        native["resources"]["invented"]["methods"]["0"]["parameters"]["url"]["pattern"] = "https://.*"
        with self.assertRaisesRegex(ValueError, "Review changed"):
            compatibility.prepare(native)

    def test_pagespeed_preserves_native_pattern_and_matches_real_engines(self):
        native = fixture("pagespeedonline", "v5", {"pagespeedonline.pagespeedapi.runpagespeed": {"url": compatibility.PAGESPEED_PARAMETER}})
        result, notes = compatibility.prepare(native)
        parameter = result["resources"]["invented"]["methods"]["0"]["parameters"]["url"]
        self.assertEqual(parameter["x-google-re2-pattern"], compatibility.PAGESPEED_PATTERN)
        self.assertEqual(len(notes), 1)
        original = re2.compile(compatibility.PAGESPEED_PATTERN)
        ecma = regress.Regex(parameter["pattern"])
        portable = re.compile(parameter["pattern"])
        samples = ["", "ftp://invented.example", "https:/invented.example", "http", "http://invented.example",
                   "HTTP://invented.example", "UrL:HtTpS://invented.example", "ORIGIN:HTTPS://invented.example",
                   "httpſ://invented.example", "url:httpſ://invented.example", "HTTPß://invented.example",
                   "https://invented.example\nlast", "https://invented.example\rlast",
                   "https://invented.example\u2028last", "https://invented.example\u2029last",
                   "prefix https://invented.example", "orıgın:https://invented.example"]
        for value in samples:
            with self.subTest(value=value):
                self.assertEqual(bool(original.search(value)), ecma.find(value) is not None)
                self.assertEqual(bool(original.fullmatch(value)), portable.fullmatch(value) is not None)

    def test_all_unicode_case_folds_for_the_pattern_literals(self):
        # Exhaust the Unicode scalar domain once, using RE2's own Unicode
        # folding. ASCII-only replacements would miss U+017F long s.
        alphabet = "".join(chr(code) for code in range(sys.maxunicode + 1) if not 0xD800 <= code <= 0xDFFF)
        actual = set(re2.findall("(?i)[urloriginhtps]", alphabet))
        self.assertEqual(actual, set("uUrRlLoOiIgGnNhHtTpPsSſ"))

    def test_other_apis_are_not_repaired(self):
        native = fixture("invented", "v1", {"invented.get": {"url": compatibility.PAGESPEED_PARAMETER}})
        result, notes = compatibility.prepare(native)
        self.assertEqual(result, native)
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
