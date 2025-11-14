#!/usr/bin/env node

const fs = require('fs');
const webvtt = require('node-webvtt');
const moment = require('moment');
const process = require('process');
const { getTranscript } = require('./utils/stj-utils');

function loadSTJ(stjFilePath) {
  const data = fs.readFileSync(stjFilePath, 'utf8');
  return JSON.parse(data);
}

function formatTimestamp(seconds) {
  const duration = moment.duration(seconds, 'seconds');
  return moment.utc(duration.asMilliseconds()).format('HH:mm:ss.SSS');
}

function generateVTT(stjData, outputVttPath) {
  const transcript = getTranscript(stjData);
  const segments = transcript.segments || [];
  if (!Array.isArray(segments) || segments.length === 0) {
    throw new Error('Invalid STJ file: transcript must include segments');
  }
  const cues = [];
  for (let i = 0; i < segments.length; i++) {
    const seg = segments[i];
    const start = formatTimestamp(seg['start']);
    const end = formatTimestamp(seg['end']);
    const speaker = seg['speaker_id'] || '';
    const text = seg['text'];
    const content = speaker ? `${speaker}: ${text}` : text;
    cues.push({
      identifier: '',
      start: start,
      end: end,
      text: content,
      styles: ''
    });
  }
  const vttData = webvtt.compile({ cues: cues });
  fs.writeFileSync(outputVttPath, vttData);
  console.log(`WebVTT file generated: ${outputVttPath}`);
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: stj-to-vtt.js <stj_file> <output_vtt>');
    process.exit(1);
  }
  const stjFile = args[0];
  const outputVtt = args[1];
  const stjData = loadSTJ(stjFile);
  generateVTT(stjData, outputVtt);
}

if (require.main === module) {
  main();
}
