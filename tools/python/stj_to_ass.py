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
    from stjlib import StandardTranscriptionJSON  # noqa: E402
except ImportError:
    _ensure_vendor_path()
    from stjlib import StandardTranscriptionJSON  # noqa: E402

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 100)
    secs = int(secs)
    return f"{hours:01d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"

def generate_ass(stj_file_path, output_ass_path):
    # Load and validate STJ file using stjlib
    stj = StandardTranscriptionJSON.from_file(stj_file_path, validate=True)
    segments = stj.transcript.segments
    styles = stj.transcript.styles if hasattr(stj.transcript, 'styles') else []
    speakers = stj.transcript.speakers if hasattr(stj.transcript, 'speakers') else []

    # Build a mapping of style IDs to style definitions
    style_map = {}
    for style in styles:
        style_id = style.id
        # Here you can map STJ styles to ASS style formats.
        # For simplicity, we'll use default styles.
        style_map[style_id] = "Default"

    # Write the ASS file
    with open(output_ass_path, 'w', encoding='utf-8') as f:
        # Write headers
        f.write('[Script Info]\n')
        f.write('Title: STJ to ASS Conversion\n')
        f.write(f'ScriptType: v4.00+\n')
        f.write(f'Collisions: Normal\n')
        f.write(f'PlayResX: 1920\n')
        f.write(f'PlayResY: 1080\n')
        f.write('Timer: 100.0000\n')
        f.write('\n')

        # Styles
        f.write('[V4+ Styles]\n')
        f.write('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
                'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, '
                'Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n')
        f.write('Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,'
                '0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n')

        # Events
        f.write('\n[Events]\n')
        f.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

        for seg in segments:
            start = format_timestamp(seg.start)
            end = format_timestamp(seg.end)
            speaker_id = seg.speaker_id if hasattr(seg, 'speaker_id') else ''
            speaker_name = ''
            if speaker_id:
                speaker = next((s for s in speakers if s.id == speaker_id), {})
                speaker_name = getattr(speaker, 'name', speaker_id)
            text = seg.text.replace('\n', '\\N')  # Replace newlines
            style_id = seg.style_id if hasattr(seg, 'style_id') else 'Default'
            style_name = style_map.get(style_id, 'Default')
            f.write(f'Dialogue: 0,{start},{end},{style_name},{speaker_name},0000,0000,0000,,{text}\n')

    print(f"ASS file generated: {output_ass_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert STJ to ASS (SSA) subtitles")
    parser.add_argument('stj_file', help="Path to the STJ file")
    parser.add_argument('output_ass', help="Path to the output ASS file")
    args = parser.parse_args()
    generate_ass(args.stj_file, args.output_ass)

if __name__ == "__main__":
    main()
