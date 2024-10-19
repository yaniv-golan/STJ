# Standard Transcription JSON (STJ) Format Specification

**Version**: 0.1  
**Date**: 2023-10-19

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats such as SRT, WebVTT, TTML, SSA/ASS, and others.

The STJ format includes detailed transcription segments with associated metadata such as speaker information, timestamps, confidence scores, language codes, and styling options. It also allows for optional metadata about the transcription process, source input, and the transcriber application.

**File Extension**: `.stj.json`  
**MIME Type**: `application/vnd.stj+json`

## Objectives

- **Interoperability**: Enable seamless data exchange between different transcription services and applications.
- **Superset of Existing Formats**: Incorporate features from common formats (SRT, WebVTT, TTML, etc.) to ensure compatibility and extendibility.
- **Extensibility**: Allow for future enhancements without breaking compatibility.
- **Clarity**: Provide a clear and well-documented structure for transcription data.
- **Utility**: Include useful metadata to support a wide range of use cases.
- **Best Practices Compliance**: Adhere to state-of-the-art best practices in metadata representation and documentation standards.

## Specification

### Overview

The STJ file is a JSON object containing two main sections:

- `"metadata"`: Contains information about the transcription process, source input, and other relevant details.
- `"transcript"`: Contains the actual transcription data, including speaker information, segments, and optional styling.

```json
{
  "metadata": { ... },
  "transcript": { ... }
}
```

### Mandatory vs. Optional Fields

- **Mandatory Fields**: Essential for basic functionality and compatibility.
- **Optional Fields**: Provide additional information and features but are not required for basic use.

### Metadata Section

The `"metadata"` object includes optional and required fields providing context about the transcription.

#### Fields

- **transcriber** *(mandatory)*: Information about the transcriber application or service.
  - **name** *(string, mandatory)*: Name of the transcriber application.
  - **version** *(string, mandatory)*: Version of the transcriber application.
- **created_at** *(string, mandatory)*: ISO 8601 timestamp indicating when the transcription was created.
- **source** *(optional)*: Information about the source of the audio/video.
  - **uri** *(string, optional)*: The URI or file path of the source media.
  - **duration** *(number, optional)*: Duration of the media in seconds.
  - **languages** *(array of strings, optional)*: List of detected or expected languages in the media, ordered by prevalence.
- **languages** *(array of strings, optional)*: List of language codes present in the transcription, ordered by prevalence.
- **confidence_threshold** *(number, optional)*: Confidence threshold used during transcription (0.0 - 1.0).
- **additional_info** *(object, optional)*: A key-value map for any additional metadata.

#### Example

```json
"metadata": {
  "transcriber": {
    "name": "YAWT",
    "version": "0.4.0"
  },
  "created_at": "2023-10-19T15:30:00Z",
  "source": {
    "uri": "https://example.com/media.mp4",
    "duration": 3600.5,
    "languages": ["en", "es", "fr"]
  },
  "languages": ["en", "es", "fr"],
  "confidence_threshold": 0.6,
  "additional_info": {
    "project": "International Conference",
    "client": "Global Events Inc."
  }
}
```

### Transcript Section

The `"transcript"` object contains the transcription data, including speaker information, segments, and optional styling.

#### Fields

- **speakers** *(array, optional)*: List of speaker objects.
- **styles** *(array, optional)*: List of style definitions for formatting and positioning.
- **segments** *(array, mandatory)*: List of transcription segments.

#### Speakers

Each speaker object includes:

- **id** *(string, mandatory)*: Unique identifier for the speaker.
- **name** *(string, optional)*: Display name of the speaker.
- **additional_info** *(object, optional)*: Any additional information about the speaker.

##### Example

```json
"speakers": [
  {
    "id": "Speaker1",
    "name": "Dr. Smith"
  },
  {
    "id": "Speaker2",
    "name": "Señora García"
  },
  {
    "id": "Speaker3",
    "name": "Monsieur Dupont"
  }
]
```

#### Styles

Each style object includes:

- **id** *(string, mandatory)*: Unique identifier for the style.
- **formatting** *(object, optional)*: Text formatting options (e.g., bold, italic).
- **positioning** *(object, optional)*: On-screen positioning options.
- **additional_info** *(object, optional)*: Any additional information about the style.

##### Example

```json
"styles": [
  {
    "id": "Style1",
    "formatting": {
      "bold": true,
      "italic": false,
      "underline": false,
      "color": "#FFFFFF",
      "background_color": "#000000"
    },
    "positioning": {
      "align": "center",
      "line": "auto",
      "position": "50%",
      "size": "100%"
    }
  }
]
```

#### Segments

Each segment object includes:

- **start** *(number, mandatory)*: Start time of the segment in seconds.
- **end** *(number, mandatory)*: End time of the segment in seconds.
- **text** *(string, mandatory)*: Transcribed text of the segment.
- **speaker_id** *(string, optional)*: The `id` of the speaker from the `speakers` list.
- **confidence** *(number, optional)*: Confidence score for the segment (0.0 - 1.0).
- **language** *(string, optional)*: Language code for the segment (ISO 639-1 or ISO 639-3).
- **style_id** *(string, optional)*: The `id` of the style from the `styles` list.
- **words** *(array, optional)*: List of word-level details.
  - **start** *(number, optional)*: Start time of the word in seconds.
  - **end** *(number, optional)*: End time of the word in seconds.
  - **text** *(string, mandatory)*: The word text.
  - **confidence** *(number, optional)*: Confidence score for the word (0.0 - 1.0).
- **additional_info** *(object, optional)*: Any additional information about the segment.

##### Example

```json
"segments": [
  {
    "start": 0.0,
    "end": 5.2,
    "text": "Good morning, everyone.",
    "speaker_id": "Speaker1",
    "confidence": 0.95,
    "language": "en",
    "style_id": "Style1",
    "words": [
      {
        "start": 0.0,
        "end": 0.5,
        "text": "Good",
        "confidence": 0.98
      },
      {
        "start": 0.6,
        "end": 1.2,
        "text": "morning,",
        "confidence": 0.97
      },
      {
        "start": 1.3,
        "end": 1.8,
        "text": "everyone.",
        "confidence": 0.90
      }
    ]
  },
  {
    "start": 5.3,
    "end": 10.0,
    "text": "Gracias por estar aquí hoy.",
    "speaker_id": "Speaker2",
    "confidence": 0.93,
    "language": "es"
  },
  {
    "start": 10.1,
    "end": 15.0,
    "text": "Merci de nous rejoindre aujourd'hui.",
    "speaker_id": "Speaker3",
    "confidence": 0.92,
    "language": "fr"
  }
]
```

### Handling Multiple Languages

- **Global Language List**: The `languages` field in the `metadata` section provides an ordered list of all languages present in the media/transcript, from most to least prevalent.
- **Segment-Level Language**: Each segment specifies its language using the `language` field, allowing applications to handle multilingual content effectively.

### Optional vs. Mandatory Fields Summary

- **Mandatory Fields**:
  - `metadata.transcriber.name`
  - `metadata.transcriber.version`
  - `metadata.created_at`
  - `transcript.segments` (array)
  - `transcript.segments[].start`
  - `transcript.segments[].end`
  - `transcript.segments[].text`

- **Optional Fields**:
  - All other fields, including `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, etc.

## Field Definitions and Constraints

- **Time Fields**: All time-related fields (`start`, `end`) are in seconds and can have fractional values to represent milliseconds.
- **Confidence Scores**: Confidence scores are floating-point numbers between `0.0` (no confidence) and `1.0` (full confidence). They are optional but recommended.
- **Language Codes**: Use ISO 639-1 (two-letter codes) or ISO 639-3 (three-letter codes) for language representation.
- **Speaker IDs**: If `speaker_id` is used, it must match an `id` in the `speakers` list.
- **Style IDs**: If `style_id` is used, it must match an `id` in the `styles` list.
- **Timestamps**: `start` should be less than or equal to `end`. Segments should not overlap in time.

## Representing Confidence

Confidence scores provide an indication of the reliability of the transcribed text. They can be used to:

- Highlight low-confidence segments for manual review.
- Filter out words or segments below a certain confidence threshold.
- Provide visual cues in transcription editors or viewers.

Including both segment-level and word-level confidence scores allows applications to present detailed insights into transcription accuracy.

## Comparison with Existing Formats

The STJ format is designed to be a superset of common transcription and subtitle formats, incorporating their features and extending them where necessary.

### SRT (SubRip)

- **Sequence Numbers**: Not used in STJ, as sequence is implied by array order.
- **Timestamps**: STJ uses precise start and end times in seconds.
- **Text**: Supported via `text` field.
- **Styling**: Limited in SRT; STJ supports styling via `styles` and `style_id`.

### WebVTT

- **Text Formatting**: STJ can represent formatting via `styles`.
- **Positioning**: Supported via `styles.positioning`.
- **Cue Settings**: Can be represented in `styles`.

### TTML (Timed Text Markup Language)

- **Complex Styling**: STJ can represent complex styles and formatting.
- **Layout and Regions**: Can be mapped using `styles` and positioning options.
- **Multiple Languages**: STJ supports per-segment language codes.

### SSA/ASS

- **Advanced Styling**: STJ supports advanced styling through `styles`.
- **Karaoke Effects**: Not directly supported but can be extended via `additional_info`.

## Usage in Applications

The STJ format is designed to be easily parsed and utilized by a variety of applications, such as:

- **Transcription Editors**: Tools can load STJ files to display transcriptions with speaker labels, timestamps, and styling.
- **Subtitle Generators**: Applications can convert STJ segments into subtitle formats like SRT or WebVTT.
- **Speech Analytics**: Analyze transcriptions for sentiment, keyword extraction, or topic modeling.
- **Quality Assurance**: Reviewers can focus on low-confidence segments for correction.
- **Multilingual Support**: Applications can handle multilingual transcriptions by leveraging per-segment language data.

## Extensibility and Customization

- **Additional Metadata**: Use the `additional_info` fields in both `metadata` and individual objects to include custom data without affecting compatibility.
- **Versioning**: Include a `version` field in `metadata` if needed for future format updates.
- **Custom Fields**: Applications can add custom fields prefixed with `x_` to include application-specific data without affecting compatibility.

## Adherence to Best Practices

The STJ format follows best practices for data interchange formats, drawing inspiration from established standards like:

- **IETF RFC 8259**: The STJ format adheres to the JSON standard as specified in [RFC 8259](https://tools.ietf.org/html/rfc8259).
- **ISO 639 Language Codes**: Uses standard language codes to ensure consistency.
- **Dublin Core Metadata Initiative (DCMI)**: The metadata fields are designed to align with DCMI principles where applicable.
- **Naming Conventions**: Field names are concise and use lowercase letters with underscores for readability.
- **Extensibility**: The format allows for future expansion without breaking existing implementations.

## Python Code to Generate SRT and WebVTT Files from STJ

Below is Python code that demonstrates how to generate SRT and WebVTT (VTT) files from an STJ file.

### Prerequisites

- Python 3.x
- Install the `srt` and `webvtt-py` libraries:

```bash
pip install srt webvtt-py
```

### Code

```python
import json
import srt
from datetime import timedelta
import webvtt

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
        text = seg['text']
        subtitles.append(srt.Subtitle(index=index, start=start, end=end, content=text))
    srt_content = srt.compose(subtitles)
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    print(f"SRT file generated: {output_srt_path}")

def generate_vtt(stj_data, output_vtt_path):
    segments = stj_data['transcript']['segments']
    vtt = webvtt.WebVTT()
    for seg in segments:
        caption = webvtt.Caption()
        caption.start = format_timestamp(seg['start'])
        caption.end = format_timestamp(seg['end'])
        caption.text = seg['text']
        vtt.captions.append(caption)
    vtt.save(output_vtt_path)
    print(f"WebVTT file generated: {output_vtt_path}")

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    td = timedelta(seconds=int(seconds), milliseconds=milliseconds)
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

if __name__ == "__main__":
    stj_file = 'transcription.stj.json'
    srt_output = 'transcription.srt'
    vtt_output = 'transcription.vtt'

    stj_data = load_stj(stj_file)
    generate_srt(stj_data, srt_output)
    generate_vtt(stj_data, vtt_output)
```

### Explanation

- **load_stj**: Loads the STJ JSON data from a file.
- **generate_srt**: Converts the segments into SRT subtitles using the `srt` library.
- **generate_vtt**: Converts the segments into WebVTT subtitles using the `webvtt` library.
- **format_timestamp**: Formats the timestamp to the required format for WebVTT.

### Notes

- The code assumes that the `segments` array in the STJ file contains at least the mandatory fields: `start`, `end`, and `text`.
- Speaker information and styling are not included in the SRT and VTT outputs, as these formats have limited support for such features.
- For formats that support styling (e.g., SSA/ASS), additional code would be needed to include styling information from the STJ `styles`.

## Final Remarks

The STJ format aims to be a comprehensive and flexible standard for transcription data representation. By incorporating features from existing formats and adhering to best practices, it strives to meet the needs of a wide range of applications and facilitate better interoperability in the field of speech transcription and subtitles.

---

**Note**: This specification is open for suggestions and improvements. Contributions from the community are welcome to refine and enhance the STJ format.

**Contact**: For feedback or contributions, please reach out via [The STJ Repo]([mailto:contact@example.com](https://github.com/yaniv-golan/STJ).
