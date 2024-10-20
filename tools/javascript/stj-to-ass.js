#!/usr/bin/env node
const fs = require('fs');
const process = require('process');
const path = require('path');

function loadSTJ(stjFilePath) {
  const data = fs.readFileSync(stjFilePath, 'utf8');
  return JSON.parse(data);
}

function formatTimestamp(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  const centiseconds = Math.floor((seconds - Math.floor(seconds)) * 100);
  return `${hours}:${minutes.toString().padStart(2, '0')}:${secs
    .toString()
    .padStart(2, '0')}.${centiseconds.toString().padStart(2, '0')}`;
}

function generateASS(stjData, outputAssPath) {
  const segments = stjData['transcript']['segments'];
  const styles = stjData['transcript']['styles'] || [];
  const speakers = stjData['transcript']['speakers'] || [];

  // Build a mapping of style IDs to style definitions
  const styleMap = {};
  styles.forEach((style) => {
    const styleId = style['id'];
    const formatting = style['formatting'] || {};
    const positioning = style['positioning'] || {};
    // For simplicity, we'll use default styles.
    styleMap[styleId] = 'Default';
  });

  const assLines = [];

  // Headers
  assLines.push('[Script Info]');
  assLines.push('Title: STJ to ASS Conversion');
  assLines.push('ScriptType: v4.00+');
  assLines.push('Collisions: Normal');
  assLines.push('PlayResX: 1920');
  assLines.push('PlayResY: 1080');
  assLines.push('Timer: 100.0000');
  assLines.push('');

  // Styles
  assLines.push('[V4+ Styles]');
  assLines.push(
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, ' +
      'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, ' +
      'Shadow, Alignment, MarginL, MarginR, MarginV, Encoding'
  );
  assLines.push(
    'Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,' +
      '0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'
  );

  // Events
  assLines.push('');
  assLines.push('[Events]');
  assLines.push(
    'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'
  );

  segments.forEach((seg) => {
    const start = formatTimestamp(seg['start']);
    const end = formatTimestamp(seg['end']);
    const speakerId = seg['speaker_id'] || '';
    let speakerName = '';
    if (speakerId) {
      const speaker = speakers.find((s) => s['id'] === speakerId) || {};
      speakerName = speaker['name'] || speakerId;
    }
    const text = seg['text'].replace(/\n/g, '\\N'); // Replace newlines
    const styleId = seg['style_id'] || 'Default';
    const styleName = styleMap[styleId] || 'Default';
    assLines.push(
      `Dialogue: 0,${start},${end},${styleName},${speakerName},0000,0000,0000,,${text}`
    );
  });

  fs.writeFileSync(outputAssPath, assLines.join('\n'));
  console.log(`ASS file generated: ${outputAssPath}`);
}

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: stj-to-ass.js <stj_file> <output_ass>');
    process.exit(1);
  }

  const stjFile = args[0];
  const outputAss = args[1];

  const stjData = loadSTJ(stjFile);
  generateASS(stjData, outputAss);
}

if (require.main === module) {
  main();
}
