# Standard Transcription JSON (STJ) Format Specification

**Version**: 0.4  
**Date**: 2024-10-22

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats such as SRT, WebVTT, TTML, SSA/ASS, and others.

The STJ format includes detailed transcription segments with associated metadata such as speaker information, timestamps, confidence scores, language codes, and styling options. It also allows for optional metadata about the transcription process, source input, and the transcriber application.

**File Extension**: `.stj.json`  
**MIME Type**: `application/vnd.stj+json`

## Objectives

- **Interoperability**: Enable seamless data exchange between different transcription services and applications.
- **Superset of Existing Formats**: Incorporate features from common formats (SRT, WebVTT, TTML, etc.) to ensure compatibility and extensibility.
- **Extensibility**: Allow for future enhancements without breaking compatibility.
- **Clarity**: Provide a clear and well-documented structure for transcription data.
- **Utility**: Include useful metadata to support a wide range of use cases.
- **Best Practices Compliance**: Adhere to state-of-the-art best practices in metadata representation and documentation standards.

## Specification

### Version History

**Version 0.4 Changes**:

- **Added** `word_timing_mode` field in segments to indicate the completeness of word-level timing data.
- **Clarified** the relationship between segment-level text and word-level details, accounting for `word_timing_mode`.
- **Specified** validation requirements for all parts of the JSON, including segments, words, speakers, styles, and additional fields.
- **Provided** additional examples demonstrating the use of `word_timing_mode`.

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
  - **languages** *(array of strings, optional)*: List of languages present in the source media, ordered by prevalence.
- **languages** *(array of strings, optional)*: List of languages present in the transcription, ordered by prevalence.
- **confidence_threshold** *(number, optional)*: Confidence threshold used during transcription (0.0 - 1.0).
- **additional_info** *(object, optional)*: A key-value map for any additional metadata.

#### Clarification on `languages` Fields

The STJ format includes two `languages` fields within the `metadata` section to distinguish between the languages present in the source media and those represented in the transcription.

- **`metadata.source.languages`** *(array of strings, optional)*:
  - **Definition**: Languages expected or detected in the source media.
  - **Purpose**: Indicates the original languages spoken in the audio/video content.
  - **Use Case**: Useful for applications that need to know what languages are present in the source, perhaps for transcription, translation, or language detection purposes.

- **`metadata.languages`** *(array of strings, optional)*:
  - **Definition**: Languages present in the transcription.
  - **Purpose**: Indicates the languages included in the transcription data within the STJ file.
  - **Use Case**: Essential for applications processing the transcription to know what languages they need to handle. This list may differ from `metadata.source.languages` if the transcription excludes some source languages or includes translations into new languages.

#### Example

```json
"metadata": {
  "transcriber": {
    "name": "YAWT",
    "version": "0.4.0"
  },
  "created_at": "2023-10-20T12:00:00Z",
  "source": {
    "uri": "https://example.com/multilingual_media.mp4",
    "duration": 3600.5,
    "languages": ["en", "es"]  // Source languages: English and Spanish
  },
  "languages": ["fr"],          // Transcription language: French
  "confidence_threshold": 0.6,
  "additional_info": {
    "project": "International Conference",
    "client": "Global Events Inc."
  }
}
```

In this example, the source media contains English and Spanish, but the transcription has been translated into French.

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
  { "id": "Speaker1", "name": "Dr. Smith" },
  { "id": "Speaker2", "name": "Señora García" },
  { "id": "Speaker3", "name": "Monsieur Dupont" }
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
  - **start** *(number, mandatory)*: Start time of the word in seconds.
  - **end** *(number, mandatory)*: End time of the word in seconds.
  - **text** *(string, mandatory)*: The word text.
  - **confidence** *(number, optional)*: Confidence score for the word (0.0 - 1.0).
- **word_timing_mode** *(string, optional)*: Indicates the completeness of word-level timing data within the segment.
- **additional_info** *(object, optional)*: Any additional information about the segment.

##### Example

```json
"segments": [
  {
    "start": 0.0,
    "end": 5.0,
    "text": "Bonjour tout le monde.",
    "speaker_id": "Speaker1",
    "confidence": 0.95,
    "language": "fr",
    "style_id": "Style1",
    "word_timing_mode": "complete",
    "words": [
      { "start": 0.0, "end": 1.0, "text": "Bonjour" },
      { "start": 1.0, "end": 2.0, "text": "tout" },
      { "start": 2.0, "end": 3.0, "text": "le" },
      { "start": 3.0, "end": 4.0, "text": "monde." }
    ]
  },
  {
    "start": 5.1,
    "end": 10.0,
    "text": "Gracias por estar aquí hoy.",
    "speaker_id": "Speaker2",
    "confidence": 0.93,
    "language": "es",
    "word_timing_mode": "partial",
    "words": [
      { "start": 5.1, "end": 5.5, "text": "Gracias" }
      // Remaining words are not included
    ]
  },
  {
    "start": 10.1,
    "end": 15.0,
    "text": "Hello everyone, and welcome.",
    "speaker_id": "Speaker3",
    "confidence": 0.92,
    "language": "en",
    "word_timing_mode": "none"
    // No words array provided
  }
]
```

In this example:

- The first segment has complete word-level data (`word_timing_mode`: `"complete"`).
- The second segment has partial word-level data (`word_timing_mode`: `"partial"`).
- The third segment has no word-level data (`word_timing_mode`: `"none"` or omitted).

### Handling Multiple Languages

- **Global Language Lists**:

  - **`metadata.source.languages`** *(array of strings, optional)*:
    - **Purpose**: Lists the languages detected or expected in the source media.
    - **Usage**: Helps in understanding the linguistic content of the source, which is vital for transcription services, translators, and language processing tools.

  - **`metadata.languages`** *(array of strings, optional)*:
    - **Purpose**: Lists the languages present in the transcription data.
    - **Usage**: Indicates which languages are included in the STJ file. This list may differ from `metadata.source.languages` if the transcription excludes some source languages or includes translations.

- **Segment-Level Language**:

  - Each segment specifies its language using the `language` field.
  - Useful for:
    - **Multilingual Transcriptions**: When the transcription includes multiple languages.
    - **Translations**: When segments have been translated into different languages.

#### Example Scenario: Translated Transcription

Imagine a video where presenters speak in English and Spanish, and the transcription has been translated entirely into French and German.

```json
"metadata": {
  "transcriber": {
    "name": "YAWT",
    "version": "0.4.0"
  },
  "created_at": "2023-10-20T12:00:00Z",
  "source": {
    "uri": "https://example.com/event.mp4",
    "duration": 5400.0,
    "languages": ["en", "es"]
  },
  "languages": ["fr", "de"],
  "additional_info": { ... }
},
"transcript": {
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "Bonjour à tous.",
      "speaker_id": "Speaker1",
      "confidence": 0.95,
      "language": "fr"
    },
    {
      "start": 5.1,
      "end": 10.0,
      "text": "Willkommen alle zusammen.",
      "speaker_id": "Speaker2",
      "confidence": 0.94,
      "language": "de"
    }
    // More segments...
  ]
}
```

In this example:

- The source media languages are English (`"en"`) and Spanish (`"es"`).
- The transcription languages are French (`"fr"`) and German (`"de"`).
- Each segment indicates the language of the transcribed text.

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
  - All other fields, including `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, `word_timing_mode`, etc.

## Field Definitions and Constraints

- **Time Fields**:
  - All time-related fields (`start`, `end`) are in seconds and can have fractional values to represent milliseconds.
  - **Constraints**:
    - `start` must not be greater than `end`.
    - Segments should not overlap in time.
    - For zero-duration words or segments (`start` equals `end`), include the appropriate duration field (`word_duration` or `segment_duration`) set to `"zero"`.
- **Confidence Scores**:
  - Confidence scores are floating-point numbers between `0.0` (no confidence) and `1.0` (full confidence). They are optional but recommended.
- **Language Codes**:
  - Use ISO 639-1 (two-letter codes) or ISO 639-3 (three-letter codes) for language representation.
- **Speaker IDs**:
  - If `speaker_id` is used, it must match an `id` in the `speakers` list.
- **Style IDs**:
  - If `style_id` is used, it must match an `id` in the `styles` list.
- **Text Fields**:
  - `text` fields should be in plain text format. Special formatting or markup should be handled via the `styles` mechanism.
- **`word_timing_mode` Field**:
  - **Purpose**: Indicates the completeness of word-level timing data within the segment.
  - **Allowed Values**:
    - `"complete"`: All words in the segment have timing data.
    - `"partial"`: Only some words have timing data.
    - `"none"`: No word-level timing data is provided.
  - **Constraints**:
    - If `words` array is present and covers all words, `word_timing_mode` may be omitted (defaulting to `"complete"`).
    - If `words` array is present but does not cover all words, `word_timing_mode` must be set to `"partial"`.
    - If `words` array is absent, `word_timing_mode` should be `"none"` or omitted.

## Validation Requirements

### Segment-Level Validation

- **Required Fields**:
  - `start` and `end` times are present and `start` ≤ `end`.
  - `text` is present and non-empty.
- **References**:
  - `speaker_id`, if present, must match an `id` in the `speakers` list.
  - `style_id`, if present, must match an `id` in the `styles` list.
- **Timing**:
  - Segments should not overlap in time.
- **Zero-Length Segments**:
  - If `start` equals `end`, include `segment_duration` set to `"zero"` in `additional_info`.

### Word-Level Validation

- **When `words` array is present**:
  - Each word object must have `text`, `start`, and `end`.
  - Word `start` and `end` times must be within the segment's `start` and `end` times.
  - Words should be ordered by `start` time.
  - Word timings should not overlap.
- **`word_timing_mode` Field**:
  - **When `word_timing_mode` is `"complete"` or omitted**:
    - The concatenation of all `text` fields in `words` must match the segment's `text`, except for differences in whitespace or punctuation.
  - **When `word_timing_mode` is `"partial"`**:
    - The `text` fields in `words` must be a subset of the words in the segment's `text`, in the same order.
- **Zero-Length Words**:
  - If a word's `start` equals `end`, include `word_duration` set to `"zero"` in `additional_info`.

### Overall Consistency

- **Language Codes**:
  - All language codes must be valid ISO 639 codes.
- **Confidence Scores**:
  - Confidence scores, if present, must be within the range [0.0, 1.0].
- **References**:
  - All `speaker_id` and `style_id` references must correspond to valid entries in the `speakers` and `styles` lists, respectively.
- **Unique IDs**:
  - All IDs used in `speakers` and `styles` must be unique within their respective arrays.

### Additional Validation

- **Time Fields**:
  - All time fields (`start`, `end`) must be non-negative numbers.
- **Segment Ordering**:
  - Segments should be ordered by their `start` times.
- **No Overlapping Segments**:
  - Segments should not overlap in time.
- **Additional Info Fields**:
  - The `additional_info` field, if used, should be an object containing key-value pairs.

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

## Final Remarks

The STJ format aims to be a comprehensive and flexible standard for transcription data representation. By incorporating features from existing formats and adhering to best practices, it strives to meet the needs of a wide range of applications and facilitate better interoperability in the field of speech transcription and subtitles.

---

**Note**: This specification is open for suggestions and improvements. Contributions from the community are welcome to refine and enhance the STJ format.

**Contact**: For feedback or contributions, please reach out via [The STJ Repository](https://github.com/yaniv-golan/STJ).
