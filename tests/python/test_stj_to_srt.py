import os
import subprocess
import filecmp
import tempfile
import pytest
import stjlib
import json

@pytest.fixture
def base_dir():
    # Get the absolute path to the project root directory
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_stj_to_srt_conversion(base_dir):
    # Add version check
    print(f"Using stjlib version: {stjlib.__version__}")
    
    # Create a temporary STJ file with correct structure
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "created_at": "2023-10-19T15:30:00Z",
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.4.0"
                },
            },
            "transcript": {
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.0,
                        "text": "Hello, world!"
                    }
                ]
            }
        }
    }
    
    stj_tool = os.path.join(base_dir, 'tools', 'python', 'stj_to_srt.py')
    expected_srt = os.path.join(base_dir, 'tests', 'expected_outputs', 'expected_simple.srt')

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create temporary input file
        input_stj = os.path.join(temp_dir, 'input.stj.json')
        with open(input_stj, 'w', encoding='utf-8') as f:
            json.dump(stj_data, f, indent=2)
            
        output_srt = os.path.join(temp_dir, 'output_test.srt')
        
        # Run the conversion
        subprocess.run(['python', stj_tool, input_stj, output_srt], check=True)

        # Read and normalize both files for comparison
        with open(output_srt, 'r', encoding='utf-8') as f:
            actual_content = f.read().strip()
        with open(expected_srt, 'r', encoding='utf-8') as f:
            expected_content = f.read().strip()

        # Compare normalized content
        assert actual_content == expected_content, "SRT files do not match."

if __name__ == '__main__':
    pytest.main()
