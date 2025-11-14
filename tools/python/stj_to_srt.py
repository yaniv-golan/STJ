#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from datetime import timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENDOR_DIR = PROJECT_ROOT / 'vendor' / 'python'


def _ensure_vendor_path():
    if VENDOR_DIR.exists():
        vendor_path = str(VENDOR_DIR)
        if vendor_path not in sys.path:
            sys.path.append(vendor_path)


try:
    from stjlib import StandardTranscriptionJSON
    import srt  # noqa: E402
except ImportError:
    _ensure_vendor_path()
    from stjlib import StandardTranscriptionJSON
    import srt  # noqa: E402

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
