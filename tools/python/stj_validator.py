import json
import jsonschema
import argparse

def validate_stj(stj_file, schema_file):
    with open(stj_file, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=stj_data, schema=schema)
        print(f"{stj_file} is valid according to the schema.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate an STJ file against the schema.")
    parser.add_argument('stj_file', help="Path to the STJ file to validate.")
    parser.add_argument('schema_file', help="Path to the JSON schema file.")
    args = parser.parse_args()
    validate_stj(args.stj_file, args.schema_file)
