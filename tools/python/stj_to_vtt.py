#!/usr/bin/env python3

import json
import webvtt
import argparse

def load_stj(stj_file_path):
    with open(stj_file_path, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    return stj_data

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = (total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def generate_vtt(stj_data, output_vtt_path):
    segments = stj_data['transcript']['segments']
    vtt = webvtt.WebVTT()
    for seg in segments:
        caption = webvtt.Caption()
        caption.start = format_timestamp(seg['start'])
        caption.end = format_timestamp(seg['end'])
        speaker = seg.get('speaker_id', '')
        text = seg['text']
        content = f"{speaker}: {text}" if speaker else text
        caption.text = content
        vtt.captions.append(caption)
    vtt.save(output_vtt_path)
    print(f"WebVTT file generated: {output_vtt_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert STJ to WebVTT")
    parser.add_argument('stj_file', help="Path to the STJ file")
    parser.add_argument('output_vtt', help="Path to the output VTT file")
    args = parser.parse_args()
    stj_data = load_stj(args.stj_file)
    generate_vtt(stj_data, args.output_vtt)

if __name__ == "__main__":
    main()
