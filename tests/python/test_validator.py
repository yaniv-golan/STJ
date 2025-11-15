import json
import os
import pytest
from stjlib import StandardTranscriptionJSON
from stjlib.stj import ValidationError

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_valid_stj_file():
    # Test with the example file
    stj_file_path = os.path.join(PROJECT_ROOT, 'examples', 'v0.6.0', 'simple.stj.json')
    stj = StandardTranscriptionJSON.from_file(stj_file_path)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_invalid_missing_mandatory_field():
    stj_data = {
        "stj": {
            "transcript": {
                "segments": [
                    {
                        "text": "Hello, world!"
                    }
                ]
            }
        }
    }
    with pytest.raises(ValidationError, match="STJ version is required"):
        StandardTranscriptionJSON.from_dict(stj_data)

def test_invalid_wrong_data_type():
    stj_data = {
        "stj": {
            "version": "0.6.0",
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
    }
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert validation_issues  # Should have validation issues

def test_invalid_additional_properties():
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "unexpected_field": "unexpected",  # Invalid additional property
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
    }
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert validation_issues  # Should have validation issues

def test_schema_error():
    # Test with an invalid schema
    invalid_schema = {
        "type": "invalid_type"  # Invalid schema
    }
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": []  # Empty segments array should cause validation error
            }
        }
    }
    validation_issues = StandardTranscriptionJSON.from_dict(stj_data).validate(raise_exception=False)
    assert validation_issues  # Should have validation issues
