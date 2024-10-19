import unittest
import json
import os
from jsonschema import validate, ValidationError, SchemaError

class TestSTJValidator(unittest.TestCase):

    def setUp(self):
        # Load the schema
        schema_path = os.path.join('spec', 'schema', 'stj-schema.json')
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)

    def test_valid_stj_file(self):
        # Test with a valid STJ file
        stj_file_path = os.path.join('examples', 'complex.stj.json')
        with open(stj_file_path, 'r', encoding='utf-8') as f:
            stj_data = json.load(f)
        try:
            validate(instance=stj_data, schema=self.schema)
        except ValidationError as e:
            self.fail(f"ValidationError raised unexpectedly: {e}")

    def test_invalid_missing_mandatory_field(self):
        # Test with an STJ file missing a mandatory field
        stj_data = {
            # 'metadata' is missing
            "transcript": {
                "segments": []
            }
        }
        with self.assertRaises(ValidationError):
            validate(instance=stj_data, schema=self.schema)

    def test_invalid_wrong_data_type(self):
        # Test with incorrect data types
        stj_data = {
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.1.0"
                },
                "created_at": "2023-10-19T15:30:00Z"
            },
            "transcript": {
                "segments": [
                    {
                        "start": "not a number",  # Incorrect data type
                        "end": 5.0,
                        "text": "Sample text"
                    }
                ]
            }
        }
        with self.assertRaises(ValidationError):
            validate(instance=stj_data, schema=self.schema)

    def test_invalid_additional_properties(self):
        # Test with unexpected additional properties
        stj_data = {
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.1.0"
                },
                "created_at": "2023-10-19T15:30:00Z",
                "unexpected_field": "unexpected"
            },
            "transcript": {
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.0,
                        "text": "Sample text"
                    }
                ]
            }
        }
        # Assuming the schema does not allow additional properties in metadata
        with self.assertRaises(ValidationError):
            validate(instance=stj_data, schema=self.schema)

    def test_schema_error(self):
        # Test with an invalid schema
        invalid_schema = {
            "type": "invalid_type"  # Invalid schema
        }
        stj_data = {}
        with self.assertRaises(SchemaError):
            validate(instance=stj_data, schema=invalid_schema)

if __name__ == '__main__':
    unittest.main()
