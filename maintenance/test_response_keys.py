import copy
import unittest

import response_keys
import update


SOURCE = {"yaml_response_keys": {"expected_conversions": 2}}
RAW = b'''openapi: 3.0.0
info: {title: Test, version: '1.0'}
paths:
  /items:
    get:
      responses:
        200:
          description: OK
          content:
            application/json:
              schema: {type: integer, default: 200}
              example: {200: 300}
        404: {description: Missing}
'''


class ResponseKeyTests(unittest.TestCase):
    def test_command_preparation_changes_only_code_keys_and_retains_provenance(self):
        spec, steps = update.prepare_document(SOURCE, RAW)
        responses = spec['paths']['/items']['get']['responses']
        self.assertEqual(set(responses), {'200', '404'})
        content = responses['200']['content']['application/json']
        self.assertEqual(content['schema']['default'], 200)
        self.assertEqual(content['example'], {200: 300})
        self.assertEqual(update.validate_document(spec), [])
        result = update.import_document({'target': 'APIs/example.com/1.0/openapi.yaml'}, spec,
                                        {'url': 'https://vendor.example/spec.yaml',
                                         'sha256': update.sha256(RAW), 'fetched_at': 'today',
                                         'transformations': steps}, None)
        self.assertIn(steps[0], result['info']['x-conversion'])
        self.assertEqual(update.parse(update.serialize_document(result).encode()), result)
        self.assertEqual(set(update.parse(RAW)['paths']['/items']['get']['responses']), {200, 404})

    def test_count_change_and_fixed_vendor_keys_require_recipe_review_without_mutation(self):
        for count in (1, 3):
            spec = update.parse(RAW); original = copy.deepcopy(spec)
            with self.assertRaisesRegex(ValueError, 'count changed'):
                update.response_keys.prepare({'yaml_response_keys': {'expected_conversions': count}}, spec)
            self.assertEqual(spec, original)
        with self.assertRaisesRegex(ValueError, 'count changed'):
            update.prepare_document(SOURCE, RAW.replace(b'        200:', b"        '200':"))

    def test_collision_and_invalid_codes_are_rejected_before_any_mutation(self):
        for bad in ({200: {}, '200': {}, 404: {}}, {200: {}, 99: {}},
                    {200: {}, 600: {}}, {200: {}, True: {}}, {200: {}, 201.5: {}}):
            spec = update.parse(RAW)
            spec['paths']['/items']['get']['responses'] = bad
            original = copy.deepcopy(spec)
            with self.assertRaises(ValueError):
                update.response_keys.prepare(SOURCE, spec)
            self.assertEqual(spec, original)

    def test_opt_in_and_exact_recipe_are_required(self):
        untouched, steps = update.prepare_document({}, RAW)
        self.assertEqual(steps, [])
        self.assertIn(200, untouched['paths']['/items']['get']['responses'])
        for recipe in ({}, {'expected_conversions': True}, {'expected_conversions': 0},
                       {'expected_conversions': 2, 'ignore_errors': True}):
            with self.assertRaisesRegex(ValueError, 'positive exact'):
                update.prepare_document({'yaml_response_keys': recipe}, RAW)

    def test_shared_yaml_response_mapping_is_checked_and_repaired_once(self):
        raw = RAW.replace(b'      responses:\n', b'      responses: &responses\n') + b'    post:\n      responses: *responses\n'
        spec, _ = update.prepare_document(SOURCE, raw)
        self.assertEqual(set(spec['paths']['/items']['post']['responses']), {'200', '404'})
        self.assertEqual(update.validate_document(spec), [])


class RangeCaseTests(unittest.TestCase):
    def spec(self):
        return {"openapi": "3.1.0", "info": {"title": "t", "version": "1"}, "paths": {
            "/a": {"get": {"responses": {"200": {"description": "ok"}, "4xx": {"description": "client"},
                                         "5xx": {"description": "server"}}}}}}

    def test_uppercases_ranges_in_order_and_validates(self):
        spec = self.spec()
        note = response_keys.prepare_range_case({"response_range_case": {"expected_conversions": 2}}, spec)
        self.assertEqual(list(spec["paths"]["/a"]["get"]["responses"]), ["200", "4XX", "5XX"])
        self.assertEqual(spec["paths"]["/a"]["get"]["responses"]["4XX"], {"description": "client"})
        self.assertIn("Uppercased 2", note)
        self.assertEqual(update.validate_document(spec), [])

    def test_count_change_collision_and_bad_recipe_fail_closed(self):
        for recipe in ({"expected_conversions": 3}, {"expected_conversions": 0}, {"other": 1}):
            with self.subTest(recipe=recipe), self.assertRaises(ValueError):
                response_keys.prepare_range_case({"response_range_case": recipe}, self.spec())
        spec = self.spec()
        spec["paths"]["/a"]["get"]["responses"]["4XX"] = {"description": "dup"}
        with self.assertRaisesRegex(ValueError, "collision"):
            response_keys.prepare_range_case({"response_range_case": {"expected_conversions": 2}}, spec)
        fixed = self.spec()  # a vendor fix (already uppercase) stops replay via the count
        responses = fixed["paths"]["/a"]["get"]["responses"]
        responses["4XX"] = responses.pop("4xx")
        responses["5XX"] = responses.pop("5xx")
        with self.assertRaisesRegex(ValueError, "count changed"):
            response_keys.prepare_range_case({"response_range_case": {"expected_conversions": 2}}, fixed)
