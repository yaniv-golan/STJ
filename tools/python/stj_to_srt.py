#!/usr/bin/env python3

import json
import srt
import argparse
from datetime import timedelta

def load_stj(stj_file_path):
    with open(stj_file_path, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    return stj_data

def generate_srt(stj_data, output_srt_path):
    segments = stj_data['transcript']['segments']
    subtitles = []
    for index, seg in enumerate(segments, start=1):
        start = timedelta(seconds=seg['start'])
        end = timedelta(seconds=seg['end'])
        speaker = seg.get('speaker_id', '')
        text = seg['text']
        content = f"{speaker}: {text}" if speaker else text
        subtitles.append(srt.Subtitle(index=index, start=start, end=end, content=content))
    srt_content = srt.compose(subtitles)
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    print(f"SRT file generated: {output_srt_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert STJ to SRT")
    parser.add_argument('stj_file', help="Path to the STJ file")
    parser.add_argument('output_srt', help="Path to the output SRT file")
    args = parser.parse_args()
    stj_data = load_stj(args.stj_file)
    generate_srt(stj_data, args.output_srt)

if __name__ == "__main__":
    main()
