import json
import os
import subprocess
import filecmp
import tempfile
import pytest
from jsonschema import validate, ValidationError, SchemaError
from stj_validator import validate_segments, validate_words

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

@pytest.fixture
def schema():
    # Load the schema
    schema_path = os.path.join(PROJECT_ROOT, 'spec', 'schema', 'stj-schema.json')
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_valid_stj_file(schema):
    # Test with a valid STJ file
    stj_file_path = os.path.join(PROJECT_ROOT, 'examples', 'simple.stj.json')
    with open(stj_file_path, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    validate(instance=stj_data, schema=schema)

def test_invalid_missing_mandatory_field(schema):
    # Test with an STJ file missing a mandatory field
    stj_data = {
        # 'metadata' is missing
        "transcript": {
            "segments": []
        }
    }
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_invalid_wrong_data_type(schema):
    # Test with incorrect data types
    stj_data = {
        "metadata": {
            "transcriber": {
                "name": "test_validator",
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
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_invalid_additional_properties(schema):
    # Test with unexpected additional properties
    stj_data = {
        "metadata": {
            "transcriber": {
                "name": "test_validator",
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
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_schema_error():
    # Test with an invalid schema
    invalid_schema = {
        "type": "invalid_type"  # Invalid schema
    }
    stj_data = {}
    with pytest.raises(SchemaError):
        validate(instance=stj_data, schema=invalid_schema)

@pytest.fixture
def base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_stj_to_srt_conversion(base_dir):
    # Paths
    stj_tool = os.path.abspath(os.path.join(base_dir, '..', '..', 'tools', 'python', 'stj_to_srt.py'))
    stj_input = os.path.abspath(os.path.join(base_dir, '..', '..', 'examples', 'simple.stj.json'))
    expected_srt = os.path.abspath(os.path.join(base_dir, '..', 'expected_outputs', 'expected_simple.srt'))
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_srt = os.path.join(temp_dir, 'output_test.srt')

        # Run the conversion
        subprocess.run(['python', stj_tool, stj_input, output_srt], check=True)

        # Compare output with expected SRT file
        assert filecmp.cmp(output_srt, expected_srt), "SRT files do not match."
