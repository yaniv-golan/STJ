import json
import jsonschema

def test_simple_example_schema():
    """Test simple.stj.json against JSON schema."""
    # Load schema
    with open('spec/schema/latest/stj-schema.json') as f:
        schema = json.load(f)
    
    # Load STJ file
    with open('examples/latest/simple.stj.json') as f:
        data = json.load(f)
    
    # Validate against schema
    jsonschema.validate(instance=data, schema=schema)

def test_complex_example_schema():
    """Test complex.stj.json against JSON schema."""
    # Load schema
    with open('spec/schema/latest/stj-schema.json') as f:
        schema = json.load(f)
    
    # Load STJ file
    with open('examples/latest/complex.stj.json') as f:
        data = json.load(f)
    
    # Validate against schema
    jsonschema.validate(instance=data, schema=schema)