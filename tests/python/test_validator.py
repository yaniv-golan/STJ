import json
import os
import pytest
from stjlib import StandardTranscriptionJSON
from jsonschema import validate  # Add this import

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

@pytest.fixture
def schema():
    # Load the schema
    schema_path = os.path.join(PROJECT_ROOT, 'spec', 'schema', 'stj-schema.json')
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_valid_stj_file():
    stj_file_path = os.path.join(PROJECT_ROOT, 'examples', 'latest', 'simple.stj.json')
    stj = StandardTranscriptionJSON.from_file(stj_file_path)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_invalid_missing_mandatory_field():
    stj_data = {
        "metadata": {
            "created_at": "2024-10-19T15:30:00Z",
            "version": "0.5.0"
            # 'transcriber' is still missing, which should cause validation to fail
        },
        "transcript": {
            "segments": []
        }
    }
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert validation_issues  # Should have validation issues

def test_invalid_wrong_data_type():
    stj_data = {
        "metadata": {
            "transcriber": {
                "name": "test_validator",
                "version": "0.1.0"
            },
            "created_at": "2024-10-19T15:30:00Z",
            "version": "0.5.0"
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
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    with pytest.raises(AttributeError):  
        stj.validate(raise_exception=True)

def test_invalid_additional_properties():
    stj_data = {
        "metadata": {
            "transcriber": {
                "name": "test_validator",
                "version": "0.1.0"
            },
            "created_at": "2024-10-19T15:30:00Z",
            "version": "0.5.0",
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
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert validation_issues  # Should have validation issues

def test_schema_error():
    # Test with an invalid schema
    invalid_schema = {
        "type": "invalid_type"  # Invalid schema
    }
    stj_data = {}
    with pytest.raises(jsonschema.SchemaError):
        validate(instance=stj_data, schema=invalid_schema)
