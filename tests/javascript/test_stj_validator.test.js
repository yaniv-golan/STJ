const { exec } = require('child_process');
const path = require('path');

const validator = path.join(__dirname, '..', '..', 'tools', 'javascript', 'stj-validator.js');
const schemaFile = path.join(__dirname, '..', '..', 'spec', 'latest', 'stj-schema.json');

// Helper function to run validator and check for expected error
function runValidatorTest(stjFileName, expectedErrorMessage, done) {
  const stjFile = path.join(__dirname, 'data', stjFileName);
  exec(`node ${validator} ${stjFile} ${schemaFile}`, (error, stdout, stderr) => {
    if (expectedErrorMessage) {
      expect(error).not.toBeNull();
      expect(stderr).toContain(expectedErrorMessage);
    } else {
      expect(error).toBeNull();
      expect(stdout).toContain('All validation checks passed.');
    }
    done();
  });
}

test('Valid STJ file passes validation', (done) => {
  const stjFile = path.join(__dirname, '..', '..', 'examples', 'simple.stj.json');
  exec(`node ${validator} ${stjFile} ${schemaFile}`, (error, stdout, stderr) => {
    expect(error).toBeNull();
    expect(stdout).toContain('All validation checks passed.');
    done();
  });
});

test('Invalid STJ file with overlapping segments fails validation', (done) => {
  runValidatorTest(
    'overlapping_segments.stj.json',
    'Segments overlap or are out of order at time 4.5',
    done
  );
});

test('Invalid STJ file with invalid language code fails validation', (done) => {
  runValidatorTest('invalid_language.stj.json', 'Invalid language code', done);
});

test('Invalid STJ file with invalid word_timing_mode fails validation', (done) => {
  runValidatorTest(
    'invalid_word_timing_mode.stj.json',
    'Concatenated words do not match segment text in segment starting at 0',
    done
  );
});

test('Invalid STJ file with zero-duration word without flag fails validation', (done) => {
  runValidatorTest(
    'zero_duration_word_without_flag.stj.json',
    "Zero-duration word at 1 without 'word_duration' set to 'zero'",
    done
  );
});

test('Invalid STJ file with invalid confidence scores fails validation', (done) => {
  runValidatorTest(
    'invalid_confidence_scores.stj.json',
    'Segment confidence 1.2 out of range [0.0, 1.0] in segment starting at 0',
    done
  );
});

test('Invalid STJ file with invalid speaker_id fails validation', (done) => {
  runValidatorTest(
    'invalid_speaker_id.stj.json',
    "Invalid speaker_id 'Speaker2' in segment starting at 0",
    done
  );
});

test('Invalid STJ file with word outside segment timings fails validation', (done) => {
  runValidatorTest(
    'word_outside_segment_timings.stj.json',
    'Word timings are outside segment timings in segment starting at 0',
    done
  );
});

test('Invalid STJ file with overlapping words fails validation', (done) => {
  runValidatorTest(
    'words_overlap_or_out_of_order.stj.json',
    'Words overlap or are out of order in segment starting at 0',
    done
  );
});
