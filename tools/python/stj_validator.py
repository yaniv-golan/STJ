#!/usr/bin/env python3

import json
import jsonschema
import argparse
import sys
from iso639 import Lang
from datetime import datetime
from typing import List, Dict, Any, Optional, TypedDict

# Define TypedDicts for structured data
class Speaker(TypedDict):
    id: str
    name: str

class Style(TypedDict):
    id: str
    description: str

class Word(TypedDict):
    start: float
    end: float
    text: str
    confidence: Optional[float]

class Segment(TypedDict):
    start: float
    end: float
    text: str
    speaker_id: Optional[str]
    style_id: Optional[str]
    language: Optional[str]
    word_timing_mode: Optional[str]
    words: Optional[List[Word]]
    word_duration: Optional[str]
    confidence: Optional[float]

class Transcript(TypedDict):
    segments: List[Segment]
    speakers: Optional[List[Speaker]]
    styles: Optional[List[Style]]

class Metadata(TypedDict):
    transcriber: Dict[str, Any]
    created_at: str
    source: Optional[Dict[str, Any]]
    languages: Optional[List[str]]

class STJData(TypedDict):
    metadata: Metadata
    transcript: Transcript

def validate_language_code(lang_code: str) -> None:
    try:
        Lang(lang_code)
        # If the code is invalid, Lang() will raise a KeyError
    except KeyError:
        raise ValueError(f"Invalid language code: {lang_code}")

def validate_language_codes(language_list: List[str]) -> None:
    for lang_code in language_list:
        validate_language_code(lang_code)

def validate_speaker_ids(speakers: List[Speaker], segments: List[Segment]) -> None:
    speaker_ids = {speaker['id'] for speaker in speakers}
    for segment in segments:
        speaker_id = segment.get('speaker_id')
        if speaker_id and speaker_id not in speaker_ids:
            raise ValueError(f"Invalid speaker_id '{speaker_id}' in segment starting at {segment['start']}")

def validate_style_ids(styles: List[Style], segments: List[Segment]) -> None:
    style_ids = {style['id'] for style in styles}
    for segment in segments:
        style_id = segment.get('style_id')
        if style_id and style_id not in style_ids:
            raise ValueError(f"Invalid style_id '{style_id}' in segment starting at {segment['start']}")

def validate_segments(segments: List[Segment]) -> None:
    # Implement the logic to check for overlapping segments
    for i in range(len(segments) - 1):
        current_end = segments[i]['end']
        next_start = segments[i + 1]['start']
        if next_start < current_end:
            raise ValueError("Segments overlap or are out of order")

def validate_words(segment: Segment) -> None:
    # Implement the logic to validate word timings and text
    if segment.get('word_timing_mode') == 'complete':
        concatenated_words = ''.join(word['text'] for word in segment.get('words', []))
        if concatenated_words != segment['text'].replace(' ', ''):
            raise ValueError("Concatenated words do not match segment text")
    for word in segment.get('words', []):
        if word['start'] == word['end'] and segment.get('word_duration') != 'zero':
            raise ValueError(f"Zero-duration word at {word['start']} without 'word_duration' set to 'zero'")

def validate_confidence_scores(segments: List[Segment]) -> None:
    for segment in segments:
        confidence = segment.get('confidence')
        if confidence is not None and not (0.0 <= confidence <= 1.0):
            raise ValueError(f"Segment confidence {confidence} out of range [0.0, 1.0] in segment starting at {segment['start']}")
        for word in segment.get('words', []):
            word_confidence = word.get('confidence')
            if word_confidence is not None and not (0.0 <= word_confidence <= 1.0):
                raise ValueError(f"Word confidence {word_confidence} out of range [0.0, 1.0] in segment starting at {segment['start']}")

def validate_stj(stj_data: STJData, schema: Dict[str, Any]) -> None:
    # First, validate against the schema
    jsonschema.validate(instance=stj_data, schema=schema)
    print("Schema validation passed.")

    # Validate metadata languages
    metadata = stj_data.get('metadata', {})
    source_languages = metadata.get('source', {}).get('languages', [])
    transcription_languages = metadata.get('languages', [])

    try:
        validate_language_codes(source_languages)
        validate_language_codes(transcription_languages)
    except ValueError as e:
        raise ValueError(f"Language code validation error: {e}")

    # Validate segments
    transcript = stj_data.get('transcript', {})
    segments = transcript.get('segments', [])
    speakers = transcript.get('speakers', [])
    styles = transcript.get('styles', [])

    # Validate speaker and style IDs
    if speakers:
        validate_speaker_ids(speakers, segments)
    if styles:
        validate_style_ids(styles, segments)

    # Validate segments sequentially
    validate_segments(segments)

    # Validate each segment
    for segment in segments:
        validate_words(segment)
        # Validate language codes in segments
        segment_language = segment.get('language')
        if segment_language:
            validate_language_code(segment_language)

    # Validate confidence scores
    validate_confidence_scores(segments)

    print("All validation checks passed.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an STJ file against the schema and additional constraints.")
    parser.add_argument('stj_file', help="Path to the STJ file to validate.")
    parser.add_argument('schema_file', help="Path to the JSON schema file.")
    args = parser.parse_args()

    with open(args.stj_file, 'r', encoding='utf-8') as f:
        stj_data = json.load(f)
    with open(args.schema_file, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    try:
        validate_stj(stj_data, schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Schema validation error: {e.message}")
        sys.exit(1)
    except ValueError as e:
        print(f"Validation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
