#!/usr/bin/env python3
import json
import argparse
import datetime

def load_stj(stj_file_path):
    with open(stj_file_path, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    return stj_data

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 100)
    secs = int(secs)
    return f"{hours:01d}:{minutes:02d}:{secs:02d}.{milliseconds:02d}"

def generate_ass(stj_data, output_ass_path):
    segments = stj_data['transcript']['segments']
    styles = stj_data['transcript'].get('styles', [])
    speakers = stj_data['transcript'].get('speakers', [])

    # Build a mapping of style IDs to style definitions
    style_map = {}
    for style in styles:
        style_id = style['id']
        formatting = style.get('formatting', {})
        position = style.get('positioning', {})
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
            start = format_timestamp(seg['start'])
            end = format_timestamp(seg['end'])
            speaker_id = seg.get('speaker_id', '')
            speaker_name = ''
            if speaker_id:
                speaker = next((s for s in speakers if s['id'] == speaker_id), {})
                speaker_name = speaker.get('name', speaker_id)
            text = seg['text'].replace('\n', '\\N')  # Replace newlines
            style_id = seg.get('style_id', 'Default')
            style_name = style_map.get(style_id, 'Default')
            f.write(f'Dialogue: 0,{start},{end},{style_name},{speaker_name},0000,0000,0000,,{text}\n')

    print(f"ASS file generated: {output_ass_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert STJ to ASS (SSA) subtitles")
    parser.add_argument('stj_file', help="Path to the STJ file")
    parser.add_argument('output_ass', help="Path to the output ASS file")
    args = parser.parse_args()

    stj_data = load_stj(args.stj_file)
    generate_ass(stj_data, args.output_ass)

if __name__ == "__main__":
    main()
