#!/usr/bin/env node

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const JSON5 = require('json5');
const path = require('path');
const iso639 = require('iso-639-1');

// Extract command-line arguments
const [, , stjFilePath, schemaFilePath] = process.argv;

// Validate input arguments
if (!stjFilePath || !schemaFilePath) {
  console.error('Usage: node stj-validator.js <stjFile> <schemaFile>');
  process.exit(1);
}

// Initialize AJV with allErrors option for detailed error reporting
const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Load and parse the JSON schema using JSON5
let schema;
try {
  const schemaData = fs.readFileSync(path.resolve(schemaFilePath), 'utf-8');
  schema = JSON5.parse(schemaData);
} catch (err) {
  console.error('Error reading schema file:', err.message);
  process.exit(1);
}

// Compile the schema
let validate;
try {
  validate = ajv.compile(schema);
} catch (e) {
  console.error('Schema Compilation Error:', e.message);
  process.exit(1);
}

// Load and parse the STJ data file using JSON5
let stjData;
try {
  const stjDataRaw = fs.readFileSync(path.resolve(stjFilePath), 'utf-8');
  stjData = JSON5.parse(stjDataRaw);
} catch (err) {
  console.error('Error reading STJ file:', err.message);
  process.exit(1);
}

// Perform schema validation
const valid = validate(stjData);
if (!valid) {
  console.error('Schema Validation Errors:', validate.errors);
  process.exit(1);
}

console.log('Schema validation passed.');

// Additional Validation Logic
try {
  validateStjData(stjData);
  console.log('All validation checks passed.');
} catch (error) {
  console.error('Validation Error:', error.message);
  process.exit(1);
}

// Validation Functions
function validateStjData(data) {
  validateLanguageCodes(data);
  validateSegments(data);
  validateSpeakersAndStyles(data);
}

function validateLanguageCodes(data) {
  const metadata = data.metadata || {};
  const sourceLanguages = metadata.source?.languages || [];
  const transcriptionLanguages = metadata.languages || [];
  const segmentLanguages = data.transcript.segments.map(seg => seg.language).filter(Boolean);

  const allLanguages = [...sourceLanguages, ...transcriptionLanguages, ...segmentLanguages];

  allLanguages.forEach(code => {
    if (!iso639.validate(code)) {
      throw new Error(`Invalid language code: ${code}`);
    }
  });
}

function validateSpeakersAndStyles(data) {
  const speakers = data.transcript.speakers || [];
  const styles = data.transcript.styles || [];
  const speakerIds = new Set(speakers.map(s => s.id));
  const styleIds = new Set(styles.map(s => s.id));

  data.transcript.segments.forEach(segment => {
    const speakerId = segment.speaker_id;
    if (speakerId && !speakerIds.has(speakerId)) {
      throw new Error(`Invalid speaker_id '${speakerId}' in segment starting at ${segment.start}`);
    }

    const styleId = segment.style_id;
    if (styleId && !styleIds.has(styleId)) {
      throw new Error(`Invalid style_id '${styleId}' in segment starting at ${segment.start}`);
    }
  });
}

function validateSegments(data) {
  const segments = data.transcript.segments;
  let previousEnd = -1;
  let hasTimingInfo = false;

  segments.forEach((segment, index) => {
    const { start, end, text, words, word_timing_mode, is_zero_duration } = segment;

    // Check if any segment has timing info
    if (start !== undefined || end !== undefined) {
      hasTimingInfo = true;
    }

    // If timing info exists, validate both start and end are present
    if (hasTimingInfo) {
      if (start === undefined || end === undefined) {
        throw new Error(`Segment ${index}: both start and end times must be present if either is provided`);
      }

      // Validate time values
      validateTimeValue(start, `segment ${index} start time`);
      validateTimeValue(end, `segment ${index} end time`);

      // Check basic timing constraints
      if (start > end) {
        throw new Error(`Segment start time ${start} is greater than end time ${end} in segment ${index}`);
      }

      if (start < previousEnd) {
        throw new Error(`Segments overlap or are out of order at time ${start} in segment ${index}`);
      }

      // Validate zero-duration segments
      validateZeroDuration(start, end, is_zero_duration, `segment ${index}`);

      // Zero-duration segments must not have words or word_timing_mode
      if (is_zero_duration) {
        if (words || word_timing_mode) {
          throw new Error(`Zero-duration segment at ${start} must not have words or word_timing_mode`);
        }
      }

      previousEnd = end;
    }

    // Validate words if present
    if (words) {
      validateWords(segment, index);
    }

    // Validate confidence scores
    if (segment.confidence !== undefined && segment.confidence !== null) {
      if (typeof segment.confidence !== 'number' ||
        segment.confidence < 0.0 ||
        segment.confidence > 1.0) {
        throw new Error(`Segment confidence ${segment.confidence} out of range [0.0, 1.0] in segment ${index}`);
      }
    }
  });

  // If any segment has timing info, all segments must have it
  if (hasTimingInfo) {
    segments.forEach((segment, index) => {
      if (segment.start === undefined || segment.end === undefined) {
        throw new Error(`Segment ${index} missing timing information when other segments have it`);
      }
    });
  }
}

function validateWords(segment, segmentIndex) {
  const words = segment.words || [];
  const wordTimingMode = segment.word_timing_mode || (words.length ? 'complete' : 'none');
  const { start: segmentStart, end: segmentEnd } = segment;

  // Validate word_timing_mode
  if (!['complete', 'partial', 'none'].includes(wordTimingMode)) {
    throw new Error(`Invalid 'word_timing_mode' in segment ${segmentIndex}`);
  }

  // Handle different word timing modes
  if (wordTimingMode === 'none') {
    if (words.length > 0) {
      throw new Error(`'word_timing_mode' is 'none' but words are provided in segment ${segmentIndex}`);
    }
    return;
  }

  // Validate words presence for non-'none' modes
  if (words.length === 0) {
    if (wordTimingMode === 'partial') {
      throw new Error(`'word_timing_mode' is 'partial' but no words are provided in segment ${segmentIndex}`);
    }
  }

  let previousWordEnd = segmentStart;
  let concatenatedWords = '';

  words.forEach((word, wordIndex) => {
    const { start: wordStart, end: wordEnd, text: wordText, is_zero_duration } = word;

    // Validate required fields
    if (!wordText) {
      throw new Error(`Missing word text in segment ${segmentIndex}, word ${wordIndex}`);
    }

    // Validate time values
    validateTimeValue(wordStart, `segment ${segmentIndex}, word ${wordIndex} start time`);
    validateTimeValue(wordEnd, `segment ${segmentIndex}, word ${wordIndex} end time`);

    // Check word timings
    if (wordStart > wordEnd) {
      throw new Error(`Word start time ${wordStart} is greater than end time ${wordEnd} in segment ${segmentIndex}, word ${wordIndex}`);
    }

    if (wordStart < segmentStart || wordEnd > segmentEnd) {
      throw new Error(`Word timings are outside segment timings in segment ${segmentIndex}, word ${wordIndex}`);
    }

    if (wordStart < previousWordEnd) {
      throw new Error(`Words overlap or are out of order in segment ${segmentIndex}, word ${wordIndex}`);
    }

    // Validate zero-duration words
    validateZeroDuration(wordStart, wordEnd, is_zero_duration, `word in segment ${segmentIndex}, word ${wordIndex}`);

    previousWordEnd = wordEnd;
    concatenatedWords += wordText + ' ';

    // Validate word confidence
    if (word.confidence !== undefined && word.confidence !== null) {
      if (typeof word.confidence !== 'number' ||
        word.confidence < 0.0 ||
        word.confidence > 1.0) {
        throw new Error(`Word confidence ${word.confidence} out of range [0.0, 1.0] in segment ${segmentIndex}, word ${wordIndex}`);
      }
    }
  });

  // Additional checks for 'complete' mode
  if (wordTimingMode === 'complete') {
    const segmentText = segment.text;
    const normalizedSegmentText = segmentText.replace(/\s+/g, '');
    const normalizedWordsText = concatenatedWords.trim().replace(/\s+/g, '');

    if (normalizedWordsText !== normalizedSegmentText) {
      throw new Error(`Concatenated words do not match segment text in segment ${segmentIndex}`);
    }
  }
}

// Add these utility functions at the top level
function validateTimeValue(time, context) {
  // Check basic type and format
  if (typeof time !== 'number') {
    throw new Error(`Invalid time value in ${context}: must be a number`);
  }

  // Check range and format requirements
  if (time < 0) {
    throw new Error(`Invalid time value in ${context}: negative values not allowed`);
  }

  if (time > 999999.999) {
    throw new Error(`Invalid time value in ${context}: exceeds maximum allowed value`);
  }

  // Convert to string and check format
  const timeStr = time.toString();
  if (timeStr.includes('e') || timeStr.includes('E')) {
    throw new Error(`Invalid time value in ${context}: scientific notation not allowed`);
  }

  // Check decimal places
  const parts = timeStr.split('.');
  if (parts[1] && parts[1].length > 3) {
    throw new Error(`Invalid time value in ${context}: maximum 3 decimal places allowed`);
  }
}

function validateZeroDuration(start, end, isZeroDuration, context) {
  if (start === end) {
    if (!isZeroDuration) {
      throw new Error(`Zero-duration ${context} must have 'is_zero_duration' set to true`);
    }
  } else {
    if (isZeroDuration) {
      throw new Error(`Non-zero-duration ${context} must not have 'is_zero_duration' field`);
    }
  }
}
