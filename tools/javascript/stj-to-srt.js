#!/usr/bin/env node

const fs = require('fs');
const srtParser = require('srt-parser-2');
const moment = require('moment');
const process = require('process');
const { getTranscript } = require('./utils/stj-utils');

function loadSTJ(stjFilePath) {
  const data = fs.readFileSync(stjFilePath, 'utf8');
  return JSON.parse(data);
}

function formatTimestamp(seconds) {
  const duration = moment.duration(seconds, 'seconds');
  return moment.utc(duration.asMilliseconds()).format('HH:mm:ss,SSS');
}

function generateSRT(stjData, outputSrtPath) {
  const transcript = getTranscript(stjData);
  const segments = transcript.segments || [];
  if (!Array.isArray(segments) || segments.length === 0) {
    throw new Error('Invalid STJ file: transcript must include segments');
  }
  const subtitles = [];
  for (let i = 0; i < segments.length; i++) {
    const seg = segments[i];
    const index = i + 1;
    const start = formatTimestamp(seg['start']);
    const end = formatTimestamp(seg['end']);
    const speaker = seg['speaker_id'] || '';
    const text = seg['text'];
    const content = speaker ? `${speaker}: ${text}` : text;
    subtitles.push({
      id: index.toString(),
      startTime: start,
      endTime: end,
      text: content
    });
  }
  const parser = new srtParser();
  const srtContent = parser.toSrt(subtitles);
  fs.writeFileSync(outputSrtPath, srtContent);
  console.log(`SRT file generated: ${outputSrtPath}`);
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: stj-to-srt.js <stj_file> <output_srt>');
    process.exit(1);
  }
  const stjFile = args[0];
  const outputSrt = args[1];
  const stjData = loadSTJ(stjFile);
  generateSRT(stjData, outputSrt);
}

if (require.main === module) {
  main();
}
