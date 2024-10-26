#!/usr/bin/env python3

import argparse
from stjlib import StandardTranscriptionJSON
from datetime import timedelta
import srt

def generate_srt(stj_file_path, output_srt_path):
    # Load and validate STJ file using stjlib
    stj = StandardTranscriptionJSON.from_file(stj_file_path, validate=True)
    segments = stj.transcript.segments
    
    subtitles = []
    for index, seg in enumerate(segments, start=1):
        start = timedelta(seconds=seg.start)
        end = timedelta(seconds=seg.end)
        speaker = seg.speaker_id if hasattr(seg, 'speaker_id') else ''
        text = seg.text
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
    generate_srt(args.stj_file, args.output_srt)

if __name__ == "__main__":
    main()
