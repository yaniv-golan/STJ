import os
import json
import pytest
from jsonschema import validate, ValidationError, SchemaError
from stj_validator import validate_segments, validate_words

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

@pytest.fixture
def schema():
    schema_path = os.path.join(PROJECT_ROOT, 'spec', 'schema', 'stj-schema.json')
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_valid_stj_file(schema):
    # Update the file path to use PROJECT_ROOT
    stj_file_path = os.path.join(PROJECT_ROOT, 'examples', 'simple.stj.json')
    with open(stj_file_path, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    validate(instance=stj_data, schema=schema)

def test_invalid_missing_mandatory_field(schema):
    stj_data = {
        # 'metadata' is missing
        "transcript": {
            "segments": []
        }
    }
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_invalid_wrong_data_type(schema):
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
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_invalid_additional_properties(schema):
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
    with pytest.raises(ValidationError):
        validate(instance=stj_data, schema=schema)

def test_schema_error():
    invalid_schema = {
        "type": "invalid_type"  # Invalid schema
    }
    stj_data = {}
    with pytest.raises(SchemaError):
        validate(instance=stj_data, schema=invalid_schema)

def test_overlapping_segments(schema):
    stj_data = {
        "metadata": {
            "transcriber": {"name": "Test", "version": "1.0"},
            "created_at": "2023-10-21T12:00:00Z"
        },
        "transcript": {
            "segments": [
                {"start": 0.0, "end": 5.0, "text": "First segment"},
                {"start": 4.5, "end": 10.0, "text": "Second segment overlaps"}
            ]
        }
    }
    with pytest.raises(ValueError, match="Segments overlap or are out of order"):
        validate(stj_data, schema)
        validate_segments(stj_data['transcript']['segments'])

def test_invalid_word_timing_mode(schema):
    stj_data = {
        "metadata": {
            "transcriber": {"name": "Test", "version": "1.0"},
            "created_at": "2023-10-21T12:00:00Z"
        },
        "transcript": {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Hello world",
                    "word_timing_mode": "complete",
                    "words": [
                        {"start": 0.0, "end": 1.0, "text": "Hello"}
                        # Missing "world" in words array
                    ]
                }
            ]
        }
    }
    with pytest.raises(ValueError, match="Concatenated words do not match segment text"):
        validate(stj_data, schema)
        validate_words(stj_data['transcript']['segments'][0])

def test_zero_duration_word_without_flag(schema):
    stj_data = {
        "metadata": {
            "transcriber": {"name": "Test", "version": "1.0"},
            "created_at": "2023-10-21T12:00:00Z"
        },
        "transcript": {
            "segments": [
                {
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Zero duration word",
                    "words": [
                        {"start": 1.0, "end": 1.0, "text": "Zero"}
                    ]
                }
            ]
        }
    }
    with pytest.raises(ValueError, match="Zero-duration word at 1.0 without 'word_duration' set to 'zero'"):
        validate(stj_data, schema)
        validate_words(stj_data['transcript']['segments'][0])
