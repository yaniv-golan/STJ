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

  segments.forEach(segment => {
    const { start, end, text, words, word_timing_mode } = segment;

    // Check start and end times
    if (start > end) {
      throw new Error(`Segment start time ${start} is greater than end time ${end}`);
    }

    // Check for overlapping segments
    if (start < previousEnd) {
      throw new Error(`Segments overlap or are out of order at time ${start}`);
    }

    // Check for zero-duration segments
    if (start === end) {
      const segmentDuration = segment.additional_info?.segment_duration;
      if (segmentDuration !== 'zero') {
        throw new Error(`Zero-duration segment at ${start} without 'segment_duration' set to 'zero'`);
      }
    }

    // Validate words within the segment
    validateWords(segment);

    // Validate confidence scores
    const confidence = segment.confidence;
    if (confidence !== undefined && (confidence < 0.0 || confidence > 1.0)) {
      throw new Error(`Segment confidence ${confidence} out of range [0.0, 1.0] in segment starting at ${start}`);
    }

    previousEnd = end;
  });
}

function validateWords(segment) {
  const words = segment.words || [];
  const wordTimingMode = segment.word_timing_mode || (words.length ? 'complete' : 'none');
  const { start: segmentStart, end: segmentEnd } = segment;

  if (!['complete', 'partial', 'none'].includes(wordTimingMode)) {
    throw new Error(`Invalid 'word_timing_mode' in segment starting at ${segmentStart}`);
  }

  if (wordTimingMode !== 'none' && words.length === 0) {
    throw new Error(`'word_timing_mode' is '${wordTimingMode}' but no words are provided in segment starting at ${segmentStart}`);
  }

  let previousWordEnd = segmentStart;
  let concatenatedWords = '';

  words.forEach(word => {
    const { start: wordStart, end: wordEnd, text: wordText } = word;

    // Check word timings
    if (wordStart > wordEnd) {
      throw new Error(`Word start time ${wordStart} is greater than end time ${wordEnd} in segment starting at ${segmentStart}`);
    }

    if (wordStart < segmentStart || wordEnd > segmentEnd) {
      throw new Error(`Word timings are outside segment timings in segment starting at ${segmentStart}`);
    }

    if (wordStart < previousWordEnd) {
      throw new Error(`Words overlap or are out of order in segment starting at ${segmentStart}`);
    }

    // Check for zero-duration words
    if (wordStart === wordEnd) {
      const wordDuration = word.additional_info?.word_duration;
      if (wordDuration !== 'zero') {
        throw new Error(`Zero-duration word at ${wordStart} without 'word_duration' set to 'zero'`);
      }
    }

    previousWordEnd = wordEnd;
    concatenatedWords += wordText + ' ';

    // Validate word confidence
    const wordConfidence = word.confidence;
    if (wordConfidence !== undefined && (wordConfidence < 0.0 || wordConfidence > 1.0)) {
      throw new Error(`Word confidence ${wordConfidence} out of range [0.0, 1.0] in segment starting at ${segmentStart}`);
    }
  });

  // Additional checks for 'complete' mode
  if (wordTimingMode === 'complete') {
    const segmentText = segment.text;
    const normalizedSegmentText = segmentText.replace(/\s+/g, '');
    const normalizedWordsText = concatenatedWords.replace(/\s+/g, '');

    if (normalizedWordsText !== normalizedSegmentText) {
      throw new Error(`Concatenated words do not match segment text in segment starting at ${segmentStart}`);
    }
  }
}
