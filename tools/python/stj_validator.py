#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENDOR_DIR = PROJECT_ROOT / 'vendor' / 'python'


def _ensure_vendor_path():
    if VENDOR_DIR.exists():
        vendor_path = str(VENDOR_DIR)
        if vendor_path not in sys.path:
            sys.path.append(vendor_path)


try:
    import jsonschema  # noqa: E402
except ImportError:
    _ensure_vendor_path()
    try:
        import jsonschema  # noqa: E402
    except ImportError:
        jsonschema = None

try:
    from stjlib import StandardTranscriptionJSON  # noqa: E402
except ImportError:
    _ensure_vendor_path()
    try:
        from stjlib import StandardTranscriptionJSON  # noqa: E402
    except ImportError:
        StandardTranscriptionJSON = None

SCHEMA_PATH = PROJECT_ROOT / 'spec' / 'schema' / 'latest' / 'stj-schema.json'


def validate_with_schema(stj_file: str):
    """Validate an STJ file against the bundled JSON schema."""
    with open(stj_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not SCHEMA_PATH.exists():
        raise RuntimeError(f"Schema file not found: {SCHEMA_PATH}")

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.absolute_path) or "root"
        errors.append(f"{path}: {error.message}")

    return errors


def basic_validation(stj_file: str):
    """Lightweight fallback validation when dependencies are unavailable."""
    with open(stj_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []
    if not isinstance(data, dict):
        return ["root: STJ file must be a JSON object"]

    stj = data.get('stj')
    if not isinstance(stj, dict):
        issues.append("root: missing 'stj' object")
        return issues

    if not stj.get('version'):
        issues.append("stj.version: version is required")

    transcript = stj.get('transcript')
    if not isinstance(transcript, dict):
        issues.append("stj.transcript: transcript object is required")
        return issues

    segments = transcript.get('segments')
    if not isinstance(segments, list) or not segments:
        issues.append("stj.transcript.segments: at least one segment is required")
        return issues

    for idx, segment in enumerate(segments):
        if not isinstance(segment, dict):
            issues.append(f"segment[{idx}]: must be an object")
            continue
        if 'text' not in segment:
            issues.append(f"segment[{idx}]: text field is required")
        start = segment.get('start')
        end = segment.get('end')
        if start is None or end is None:
            issues.append(f"segment[{idx}]: start and end fields are required")
        elif not (isinstance(start, (int, float)) and isinstance(end, (int, float))):
            issues.append(f"segment[{idx}]: start/end must be numbers")
        elif start > end:
            issues.append(f"segment[{idx}]: start must be <= end")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate an STJ file.")
    parser.add_argument('stj_file', help="Path to the STJ file to validate.")
    args = parser.parse_args()

    try:
        if StandardTranscriptionJSON is not None:
            stj = StandardTranscriptionJSON.from_file(args.stj_file, validate=False)
            validation_issues = stj.validate(raise_exception=False)
        elif jsonschema is not None:
            validation_issues = validate_with_schema(args.stj_file)
        else:
            validation_issues = basic_validation(args.stj_file)

        if not validation_issues:
            print("Validation successful! No issues found.")
            sys.exit(0)

        print("Validation failed. Found the following issues:")
        for i, issue in enumerate(validation_issues, 1):
            print(f"\n{i}. {issue}")

        sys.exit(1)

    except FileNotFoundError as e:
        missing = e.filename if hasattr(e, 'filename') and e.filename else args.stj_file
        print(f"File not found: {missing}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error while processing file: Invalid JSON - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error while processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
