import os
import subprocess
import filecmp
import tempfile
import pytest
import stjlib

@pytest.fixture
def base_dir():
    # Get the absolute path to the project root directory
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_stj_to_srt_conversion(base_dir):
    # Add version check
    print(f"Using stjlib version: {stjlib.__version__}")
    
    # Update path to include 'latest' directory
    stj_tool = os.path.join(base_dir, 'tools', 'python', 'stj_to_srt.py')
    stj_input = os.path.join(base_dir, 'examples', 'latest', 'simple.stj.json')  # Updated path
    expected_srt = os.path.join(base_dir, 'tests', 'expected_outputs', 'expected_simple.srt')

    # Add these checks
    assert os.path.exists(stj_tool), f"STJ tool not found at: {stj_tool}"
    assert os.path.exists(stj_input), f"Input file not found at: {stj_input}"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_srt = os.path.join(temp_dir, 'output_test.srt')
        
        # Add debug output
        print(f"Running conversion with:")
        print(f"Tool: {stj_tool}")
        print(f"Input: {stj_input}")
        print(f"Output: {output_srt}")
        
        # Run the conversion
        subprocess.run(['python', stj_tool, stj_input, output_srt], check=True)

        # Compare output with expected SRT file
        assert filecmp.cmp(output_srt, expected_srt), "SRT files do not match."

if __name__ == '__main__':
    pytest.main()
