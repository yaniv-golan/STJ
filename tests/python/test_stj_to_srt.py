import os
import subprocess
import filecmp
import tempfile
import pytest

@pytest.fixture
def base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_stj_to_srt_conversion(base_dir):
    # Paths
    stj_tool = os.path.join(base_dir, '..', '..', 'tools', 'python', 'stj_to_srt.py')
    stj_input = os.path.join(base_dir, '..', '..', 'examples', 'simple.stj.json')
    expected_srt = os.path.join(base_dir, '..', 'expected_outputs', 'expected_simple.srt')
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_srt = os.path.join(temp_dir, 'output_test.srt')

        # Run the conversion
        subprocess.run(['python', stj_tool, stj_input, output_srt], check=True)

        # Compare output with expected SRT file
        assert filecmp.cmp(output_srt, expected_srt), "SRT files do not match."

if __name__ == '__main__':
    pytest.main()
