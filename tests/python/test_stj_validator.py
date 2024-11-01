"""Tests for the STJ validator CLI tool.

This module tests the command-line interface of the STJ validator tool.
It uses pytest's tmp_path fixture to create temporary test files.
"""

import os
import subprocess
import pytest

# Get the absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_cli_valid_file():
    """Test CLI with a valid STJ file."""
    stj_file_path = os.path.join(PROJECT_ROOT, 'examples', 'latest', 'simple.stj.json')
    result = subprocess.run(
        ['python', 'tools/python/stj_validator.py', stj_file_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Validation successful!" in result.stdout

def test_cli_invalid_file(tmp_path):
    """Test CLI with an invalid STJ file.
    
    Args:
        tmp_path: Pytest fixture that provides a temporary directory unique to each test function.
                 See: https://docs.pytest.org/en/stable/tmpdir.html
    """
    # Create invalid test file in the temporary directory
    invalid_file = tmp_path / "invalid.stj.json"
    invalid_file.write_text('{"invalid": "json"}')
    
    result = subprocess.run(
        ['python', 'tools/python/stj_validator.py', str(invalid_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Validation failed" in result.stdout

def test_cli_missing_file():
    """Test CLI with a non-existent file."""
    result = subprocess.run(
        ['python', 'tools/python/stj_validator.py', 'nonexistent.stj.json'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "File not found" in result.stdout

def test_cli_no_arguments():
    """Test CLI with no arguments."""
    result = subprocess.run(
        ['python', 'tools/python/stj_validator.py'],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "error: the following arguments are required: stj_file" in result.stderr
