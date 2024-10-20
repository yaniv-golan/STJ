import unittest
import os
import subprocess
import filecmp

class TestSTJToSRT(unittest.TestCase):
    def test_stj_to_srt_conversion(self):
        # Paths
        stj_tool = os.path.join('..', '..', 'tools', 'python', 'stj_to_srt.py')
        stj_input = os.path.join('..', '..', 'examples', 'simple.stj.json')
        output_srt = 'output_test.srt'
        expected_srt = os.path.join('..', 'expected_outputs', 'expected_simple.srt')

        # Run the conversion
        subprocess.run(['python', stj_tool, stj_input, output_srt], check=True)

        # Compare output with expected SRT file
        self.assertTrue(filecmp.cmp(output_srt, expected_srt), "SRT files do not match.")

        # Clean up
        os.remove(output_srt)

if __name__ == '__main__':
    unittest.main()
