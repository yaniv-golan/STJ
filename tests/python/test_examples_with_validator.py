from stjlib import StandardTranscriptionJSON

def test_simple_example():
    """Test simple.stj.json with stjlib validation."""
    stj = StandardTranscriptionJSON.from_file('examples/latest/simple.stj.json')
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_complex_example():
    """Test complex.stj.json with stjlib validation."""
    stj = StandardTranscriptionJSON.from_file('examples/latest/complex.stj.json')
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues