import unittest
import json
import os
from jsonschema import validate, ValidationError

class TestSTJValidator(unittest.TestCase):
    def setUp(self):
        # Load the schema
        schema_path = os.path.join('..', '..', 'spec', 'schema', 'stj-schema.json')
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)

    def test_valid_stj_file(self):
        stj_file_path = os.path.join('..', '..', 'examples', 'simple.stj.json')
        with open(stj_file_path, 'r', encoding='utf-8') as f:
            stj_data = json.load(f)
        try:
            validate(instance=stj_data, schema=self.schema)
        except ValidationError as e:
            self.fail(f"ValidationError raised unexpectedly: {e}")

    def test_invalid_stj_file(self):
        # Create an invalid STJ data
        stj_data = {"invalid": "data"}
        with self.assertRaises(ValidationError):
            validate(instance=stj_data, schema=self.schema)

if __name__ == '__main__':
    unittest.main()
