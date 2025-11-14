#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENDOR_DIR = PROJECT_ROOT / 'vendor' / 'python'


def _ensure_vendor_path():
    if VENDOR_DIR.exists():
        vendor_path = str(VENDOR_DIR)
        if vendor_path not in sys.path:
            sys.path.append(vendor_path)


try:
    import webvtt  # noqa: E402
    from stjlib import StandardTranscriptionJSON  # noqa: E402
except ImportError:
    _ensure_vendor_path()
    import webvtt  # noqa: E402
    from stjlib import StandardTranscriptionJSON  # noqa: E402

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = (total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def generate_vtt(stj_file_path, output_vtt_path):
    # Load and validate STJ file using stjlib
    stj = StandardTranscriptionJSON.from_file(stj_file_path, validate=True)
    segments = stj.transcript.segments
    
    vtt = webvtt.WebVTT()
    for seg in segments:
        caption = webvtt.Caption()
        caption.start = format_timestamp(seg.start)
        caption.end = format_timestamp(seg.end)
        speaker = seg.speaker_id if hasattr(seg, 'speaker_id') else ''
        text = seg.text
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
    generate_vtt(args.stj_file, args.output_vtt)

if __name__ == "__main__":
    main()
