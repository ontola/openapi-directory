"""Run with: python -m unittest discover -s APIs/moneybird.com/v2-readonly."""
import unittest
from openapi_schema_validator import OAS30Validator
from generate import nullable_to_30, path_kind

class ConversionTests(unittest.TestCase):
    def test_nullable_union_preserves_values_without_accepting_unrelated_objects(self):
        schema = nullable_to_30({'type': ['string', 'integer', 'null']})
        validator = OAS30Validator(schema)
        for value in [None, '123', 123]:
            self.assertTrue(validator.is_valid(value), repr(value))
        for value in [{}, [], True, 1.5]:
            self.assertFalse(validator.is_valid(value), repr(value))

    def test_overlapping_numeric_types_and_null_only_schema(self):
        numeric = OAS30Validator(nullable_to_30({'type': ['integer', 'number', 'null']}))
        for value in [None, 1, 1.5]:
            self.assertTrue(numeric.is_valid(value))
        self.assertFalse(numeric.is_valid({}))
        null_only = OAS30Validator(nullable_to_30({'type': ['null']}))
        self.assertTrue(null_only.is_valid(None))
        for value in [{}, '', 0]:
            self.assertFalse(null_only.is_valid(value))

    def test_closed_allof_preserves_fields_and_validation(self):
        schema = nullable_to_30({"unevaluatedProperties": False, "allOf": [
            {"type": "object", "properties": {"id": {"type": "integer"}}},
            {"type": "object", "properties": {"name": {"type": "string"}}, "required": []},
        ]})
        validator = OAS30Validator(schema)
        self.assertTrue(validator.is_valid({"id": 1, "name": "Ada"}))
        self.assertFalse(validator.is_valid({"id": 1, "name": 42}))
        self.assertFalse(validator.is_valid({"id": 1, "extra": True}))
        self.assertEqual(schema["properties"]["id"]["type"], "integer")

    def test_download_records_are_not_binary_attachment_downloads(self):
        self.assertEqual(path_kind('/{administration_id}/downloads{format}', '')[0], 'primary_list')
        self.assertEqual(path_kind('/{administration_id}/sales_invoices/{id}/download_pdf{format}', '')[0], 'binary_or_helper')

    def test_duplicate_lookup_does_not_create_a_second_collection(self):
        self.assertEqual(path_kind('/{administration_id}/contacts/doubles{format}', '')[0], 'lookup_helper')
        self.assertEqual(path_kind('/{administration_id}/contacts{format}', '')[0], 'primary_list')

if __name__ == '__main__':
    unittest.main()
