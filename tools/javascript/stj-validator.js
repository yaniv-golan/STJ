#!/usr/bin/env node

const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const JSON5 = require('json5');
const path = require('path');
const languageData = require('./data/language-codes.json');
const { getStjRoot } = require('./utils/stj-utils');

const ISO6393_TO_1 = {};
Object.entries(languageData.iso6393To1 || {}).forEach(([key, value]) => {
  if (key) {
    ISO6393_TO_1[key.toLowerCase()] = value;
  }
});

const ISO6391_CODES = new Set(
  (languageData.iso6391Codes || []).map(code => code.toLowerCase()).filter(Boolean)
);
const ISO6393_CODES = new Set(
  (languageData.iso6393Codes || []).map(code => code.toLowerCase()).filter(Boolean)
);
const ISO6393_WITHOUT_ISO6391 = new Set(
  [...ISO6393_CODES].filter(code => !ISO6393_TO_1[code])
);

// Validation Functions
function validateTimeValue(time, context) {
  if (typeof time !== 'number') {
    throw new Error(`Invalid time value in ${context}: must be a number`);
  }
  if (time < 0) {
    throw new Error(`Invalid time value in ${context}: negative values not allowed`);
  }
  if (time > 999999.999) {
    throw new Error(`Invalid time value in ${context}: exceeds maximum allowed value`);
  }
  const timeStr = time.toString();
  if (timeStr.includes('e') || timeStr.includes('E')) {
    throw new Error(`Invalid time value in ${context}: scientific notation not allowed`);
  }
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

function assertValidLanguageCode(code) {
  if (!code || typeof code !== 'string') {
    throw new Error(`Invalid language code: ${code}`);
  }
  const normalized = code.toLowerCase();
  if (ISO6391_CODES.has(normalized)) {
    return;
  }
  if (ISO6393_WITHOUT_ISO6391.has(normalized)) {
    return;
  }
  if (ISO6393_TO_1[normalized]) {
    throw new Error(
      `Invalid language code: ${code}. Use ISO 639-1 code '${ISO6393_TO_1[normalized]}' instead.`
    );
  }
  if (ISO6393_CODES.has(normalized)) {
    return;
  }
  throw new Error(`Invalid language code: ${code}`);
}

function validateLanguageCodes(stjRoot) {
  const metadata = stjRoot.metadata || {};
  const transcript = stjRoot.transcript || {};
  const segments = Array.isArray(transcript.segments) ? transcript.segments : [];
  const sourceLanguages = metadata.source?.languages || [];
  const transcriptionLanguages = metadata.languages || [];
  const segmentLanguages = segments.map(seg => seg.language).filter(Boolean);

  const allLanguages = [...sourceLanguages, ...transcriptionLanguages, ...segmentLanguages];
  allLanguages.forEach(assertValidLanguageCode);
}

function validateSpeakersAndStyles(transcript) {
  const speakers = transcript.speakers || [];
  const styles = transcript.styles || [];
  const segments = transcript.segments || [];
  const speakerIds = new Set(speakers.map(s => s.id));
  const styleIds = new Set(styles.map(s => s.id));

  segments.forEach(segment => {
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

function validateWords(segment, segmentIndex) {
  const words = segment.words || [];
  const wordTimingMode = segment.word_timing_mode || (words.length ? 'complete' : 'none');
  const { start: segmentStart, end: segmentEnd } = segment;

  if (!['complete', 'partial', 'none'].includes(wordTimingMode)) {
    throw new Error(`Invalid 'word_timing_mode' in segment ${segmentIndex}`);
  }

  if (wordTimingMode === 'none' && words.length > 0) {
    throw new Error(`'word_timing_mode' is 'none' but words are provided in segment ${segmentIndex}`);
  }

  if (words.length === 0 && wordTimingMode === 'partial') {
    throw new Error(`'word_timing_mode' is 'partial' but no words are provided in segment ${segmentIndex}`);
  }

  let previousWordEnd = segmentStart;
  let concatenatedWords = '';

  words.forEach((word, wordIndex) => {
    if (!word.text) {
      throw new Error(`Missing word text in segment ${segmentIndex}, word ${wordIndex}`);
    }

    validateTimeValue(word.start, `segment ${segmentIndex}, word ${wordIndex} start time`);
    validateTimeValue(word.end, `segment ${segmentIndex}, word ${wordIndex} end time`);

    if (word.start > word.end) {
      throw new Error(`Word start time ${word.start} is greater than end time ${word.end} in segment ${segmentIndex}, word ${wordIndex}`);
    }

    if (word.start < segmentStart || word.end > segmentEnd) {
      throw new Error(`Word timings are outside segment timings in segment ${segmentIndex}, word ${wordIndex}`);
    }

    if (word.start < previousWordEnd) {
      throw new Error(`Words overlap or are out of order in segment ${segmentIndex}, word ${wordIndex}`);
    }

    validateZeroDuration(word.start, word.end, word.is_zero_duration, `word in segment ${segmentIndex}, word ${wordIndex}`);

    previousWordEnd = word.end;
    concatenatedWords += word.text + ' ';

    if (word.confidence !== undefined && word.confidence !== null) {
      if (typeof word.confidence !== 'number' || word.confidence < 0.0 || word.confidence > 1.0) {
        throw new Error(`Word confidence ${word.confidence} out of range [0.0, 1.0] in segment ${segmentIndex}, word ${wordIndex}`);
      }
    }
  });

  if (wordTimingMode === 'complete') {
    const segmentText = segment.text;
    const normalizedSegmentText = segmentText.replace(/\s+/g, '');
    const normalizedWordsText = concatenatedWords.trim().replace(/\s+/g, '');

    if (normalizedWordsText !== normalizedSegmentText) {
      throw new Error(`Concatenated words do not match segment text in segment ${segmentIndex}`);
    }
  }
}

function validateSegments(transcript) {
  const segments = transcript.segments;
  let previousEnd = -1;
  let hasTimingInfo = false;

  segments.forEach((segment, index) => {
    if (segment.start !== undefined || segment.end !== undefined) {
      hasTimingInfo = true;
    }

    if (hasTimingInfo) {
      if (segment.start === undefined || segment.end === undefined) {
        throw new Error(`Segment ${index}: both start and end times must be present if either is provided`);
      }

      validateTimeValue(segment.start, `segment ${index} start time`);
      validateTimeValue(segment.end, `segment ${index} end time`);

      if (segment.start > segment.end) {
        throw new Error(`Segment start time ${segment.start} is greater than end time ${segment.end} in segment ${index}`);
      }

      if (segment.start < previousEnd) {
        throw new Error(`Segments overlap or are out of order at time ${segment.start}`);
      }

      validateZeroDuration(segment.start, segment.end, segment.is_zero_duration, `segment ${index}`);

      if (segment.is_zero_duration && (segment.words || segment.word_timing_mode)) {
        throw new Error(`Zero-duration segment at ${segment.start} must not have words or word_timing_mode`);
      }

      previousEnd = segment.end;
    }

    if (segment.words) {
      validateWords(segment, index);
    }

    if (segment.confidence !== undefined && segment.confidence !== null) {
      if (typeof segment.confidence !== 'number' || segment.confidence < 0.0 || segment.confidence > 1.0) {
        throw new Error(`Segment confidence ${segment.confidence} out of range [0.0, 1.0] in segment starting at ${segment.start}`);
      }
    }
  });

  if (hasTimingInfo) {
    segments.forEach((segment, index) => {
      if (segment.start === undefined || segment.end === undefined) {
        throw new Error(`Segment ${index} missing timing information when other segments have it`);
      }
    });
  }
}

function validateStjData(stjRoot) {
  if (!stjRoot || typeof stjRoot !== 'object') {
    throw new Error('Invalid STJ data: missing root');
  }
  const transcript = stjRoot.transcript;
  if (!transcript || !Array.isArray(transcript.segments)) {
    throw new Error('Invalid STJ data: transcript must include a segments array');
  }

  validateLanguageCodes(stjRoot);
  validateSegments(transcript);
  validateSpeakersAndStyles(transcript);
}

// Export the validation function for use as a module
async function validate(stjData, schemaPath) {
  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);

  let deferredStructureError = null;
  let stjRoot = null;

  try {
    stjRoot = getStjRoot(stjData);
    validateStjData(stjRoot);
  } catch (error) {
    if (typeof error.message === 'string' && error.message.toLowerCase().includes('invalid stj')) {
      deferredStructureError = error;
    } else {
      throw error;
    }
  }

  const schemaData = await fs.promises.readFile(path.resolve(schemaPath), 'utf-8');
  const schema = JSON5.parse(schemaData);

  const validateSchema = ajv.compile(schema);

  const valid = validateSchema(stjData);
  if (!valid) {
    throw new Error('Schema Validation Errors: ' + JSON.stringify(validateSchema.errors, null, 2));
  }

  if (deferredStructureError) {
    throw deferredStructureError;
  }

  if (!stjRoot) {
    stjRoot = getStjRoot(stjData);
  }
  validateStjData(stjRoot);
}

// Command-line interface
if (require.main === module) {
  const [, , stjFilePath, schemaFilePath] = process.argv;

  if (!stjFilePath || !schemaFilePath) {
    console.error('Usage: node stj-validator.js <stjFile> <schemaFile>');
    process.exit(1);
  }

  try {
    const stjData = JSON5.parse(fs.readFileSync(path.resolve(stjFilePath), 'utf-8'));
    validate(stjData, schemaFilePath)
      .then(() => {
        console.log('All validation checks passed.');
      })
      .catch(error => {
        console.error('Validation Error:', error.message);
        process.exit(1);
      });
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { validate };
