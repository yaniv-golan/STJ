# Standard Transcription JSON (STJ) Format Specification

**Version**: 0.5
**Date**: 2024-10-24

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats such as SRT, WebVTT, TTML, SSA/ASS, and others.

The STJ format includes detailed transcription segments with associated metadata such as speaker information, timestamps, confidence scores, language codes, and styling options. It also allows for optional metadata about the transcription process, source input, and the transcriber application.

**File Extension**: `.stj.json`  
**MIME Type**: `application/vnd.stj+json`
**Character Encoding**: UTF-8

## Objectives

- **Interoperability**: Enable seamless data exchange between different transcription services and applications.
- **Superset of Existing Formats**: Incorporate features from common formats (SRT, WebVTT, TTML, etc.) to ensure compatibility and extensibility.
- **Extensibility**: Allow for future enhancements without breaking compatibility.
- **Clarity**: Provide a clear and well-documented structure for transcription data.
- **Utility**: Include useful metadata to support a wide range of use cases.
- **Best Practices Compliance**: Adhere to state-of-the-art best practices in metadata representation and documentation standards.

## Specification

The STJ files must include a `version` field within the `metadata` section to indicate the specification version they comply with. This facilitates compatibility and proper validation across different implementations.

### Version History

For a detailed list of changes between versions, please see the [CHANGELOG.md](../CHANGELOG.md) file.

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
- **version** *(mandatory)*: Specifies the STJ specification version the file adheres to.
  - **Format**: Semantic versioning (e.g., `"0.5.0"`)
  - **Pattern**: Must follow the regex pattern `^\d+\.\d+\.\d+$` to ensure semantic versioning.
- **source** *(optional)*: Information about the source of the audio/video.
  - **uri** *(string, optional)*: The URI of the source media.
    - MUST conform to the **URI Format Requirements** specified in the **Field Definitions and Constraints** section.
  - **duration** *(number, optional)*: Duration of the media in seconds.
  - **languages** *(array of strings, optional)*: List of languages present in the source media, ordered by prevalence.
- **languages** *(array of strings, optional)*: List of languages present in the transcription, ordered by prevalence.
- **confidence_threshold** *(number, optional)*: Confidence threshold used during transcription (0.0 - 1.0).
- **extensions** *(object, optional)*: A key-value map for any additional metadata.
  - MUST conform to the **Extensions Field Requirements** specified in the **Field Definitions and Constraints** section.

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
  "version": "0.5.0",
  "source": {
    "uri": "https://example.com/multilingual_media.mp4",
    "duration": 3600.5,
    "languages": ["en", "es"]  // Source languages: English and Spanish
  },
  "languages": ["fr"],          // Transcription language: French
  "confidence_threshold": 0.6,
  "extensions": {
    "project_info": {
      "project": "International Conference",
      "client": "Global Events Inc."
    }
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
  - MUST conform to the **Speaker ID Requirements** specified in the **Field Definitions and Constraints** section.
- **name** *(string, optional)*: Display name of the speaker.
- **extensions** *(object, optional)*: Any additional information about the speaker.

##### Example

```json
"speakers": [
  { "id": "Speaker1", "name": "Dr. Smith" },
  { "id": "Speaker2", "name": "Señora García" },
  { "id": "Speaker3", "name": "Monsieur Dupont" },
  { "id": "Speaker4", "name": "Unknown" } // Anonymous speaker
]
```

#### Styles

Each style object defines text presentation rules that can be referenced by segments. Basic formatting features are defined in a format-agnostic way, while advanced features can be implemented using `extensions`.

##### Required Fields

- **id** *(string, mandatory)*: Unique identifier for the style
  - MUST be non-empty
  - MUST be unique within the styles array

##### Optional Fields

- **text** *(object, optional)*: Text appearance
  - **color** *(string, optional)*: Text color in #RRGGBB format
  - **background** *(string, optional)*: Background color in #RRGGBB format
  - **bold** *(boolean, optional)*: Bold text
  - **italic** *(boolean, optional)*: Italic text
  - **underline** *(boolean, optional)*: Underlined text
  - **size** *(string, optional)*: Size as percentage, e.g. "120%"

- **display** *(object, optional)*: Visual presentation settings
  - **align** *(string, optional)*: Text alignment
    - Allowed values: `"left"`, `"center"`, `"right"`
    - Default: `"left"`
  - **vertical** *(string, optional)*: Vertical position
    - Allowed values: `"top"`, `"middle"`, `"bottom"`
    - Default: `"bottom"`
  - **position** *(object, optional)*: Precise positioning
    - **x** *(string, optional)*: Horizontal position as percentage
    - **y** *(string, optional)*: Vertical position as percentage

- **extensions** *(object, optional)*: Additional styling information
  - MAY contain format-specific styling properties organized under namespaces.
  - Format-specific properties SHOULD be placed within appropriately named namespaces in `extensions`.
  - Examples:
    - Under the `custom_webvtt` namespace:

      ```json
      "extensions": {
        "custom_webvtt": {
          "line": "auto",
          "position": "50%",
          "size": "100%"
        }
      }
      ```

    - Under the `custom_ssa` namespace:

      ```json
      "extensions": {
        "custom_ssa": {
          "effect": "karaoke",
          "outline": 2,
          "shadow": 1
        }
      }
      ```

##### Examples

Basic style:

```json
{
  "id": "speaker_1",
  "text": {
    "color": "#2E4053",
    "bold": true,
    "size": "110%"
  }
}
```

Style with positioning:

```json
{
  "id": "caption_style",
  "text": {
    "color": "#FFFFFF",
    "background": "#000000"
  },
  "display": {
    "align": "center",
    "vertical": "bottom",
    "position": {
      "x": "50%",
      "y": "90%"
    }
  }
}
```

Style with format-specific features:

```json
{
  "id": "advanced_style",
  "text": {
    "color": "#FFFFFF"
  },
  "extensions": {
    "custom_ssa": {
      "effect": "karaoke",
      "outline": 2,
      "shadow": 1
    }
  }
}
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
- **extensions** *(object, optional)*: Any additional information about the segment.

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
  "version": "0.5.0",
  "source": {
    "uri": "https://example.com/event.mp4",
    "duration": 5400.0,
    "languages": ["en", "es"]
  },
  "languages": ["fr", "de"],
  "extensions": { ... }
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
  - `metadata.version`
  - `transcript.segments` (array)
  - `transcript.segments[].start`
  - `transcript.segments[].end`
  - `transcript.segments[].text`

- **Optional Fields**:
  - All other fields, including `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, `word_timing_mode`, etc.

## Field Definitions and Constraints

### Time Format Requirements

All time values in the STJ format (`start` and `end` fields) must follow these requirements:

#### Format Specifications

- Must be represented as non-negative decimal numbers
- Must have a precision of up to 3 decimal places (millisecond precision)
- Must not exceed 6 significant digits before the decimal point
- Values must be in the range [0.000, 999999.999]
- Leading zeros before the decimal point are allowed but not required
- Trailing zeros after the decimal point are allowed but not required
- The decimal point must be present if there are decimal places
- Scientific notation is not allowed

#### Basic Constraints

- For any segment or word:
  - `start` must not be greater than `end`
  - Both `start` and `end` must be present and valid according to format specifications
- For zero-duration items (`start` equals `end`):
  - Must include `is_zero_duration`: `true`
  - For segments:
    - Must not contain a `words` array
    - Must not specify a `word_timing_mode`
- The `is_zero_duration` field:
  - Must be `true` if and only if `start` equals `end`
  - Must be `false` or omitted for items where `start` does not equal `end`
  - Must not be included with value `false` when `start` equals `end`

#### Examples of Valid Time Values

- `0` (zero seconds)
- `0.0` (zero seconds)
- `0.000` (zero seconds with full precision)
- `1.5` (one and a half seconds)
- `10.100` (ten and one hundred milliseconds)
- `999999.999` (maximum allowed value)

#### Examples of Invalid Time Values

- `-1.0` (negative values not allowed)
- `1.5e3` (scientific notation not allowed)
- `1000000.0` (exceeds maximum value)
- `1.2345` (exceeds maximum precision)
- `1,5` (incorrect decimal separator)

### Character Encoding Requirements

#### Basic Requirements

- Files MUST be encoded in UTF-8
- The UTF-8 Byte Order Mark (BOM) is optional
- JSON string values MUST follow RFC 8259 encoding rules
- The full Unicode character set MUST be supported

#### String Content Requirements

- All string values MUST:
  - Be valid UTF-8 encoded text
  - Properly escape control characters (U+0000 through U+001F)
  - Properly handle surrogate pairs for supplementary plane characters
- Forward slash (`/`) characters MAY be escaped but escaping is not required
- Unicode normalization:
  - All string values SHOULD be normalized to Unicode Normalization Form C (NFC)
  - Applications MUST preserve the normalization form of input text
  - Applications MAY normalize text for comparison or search operations

### Confidence Scores

Confidence scores are floating-point numbers between `0.0` (no confidence) and `1.0` (full confidence). They are optional but recommended.

### Language Codes

ISO 639-1 (two-letter codes) is the primary standard and MUST be used when the language has an ISO 639-1 code.

- Example: Use "en" for English, "fr" for French, "es" for Spanish

ISO 639-3 (three-letter codes) MUST only be used for languages that do not have an ISO 639-1 code.

- Example: Use "yue" for Cantonese (no ISO 639-1 code), but use "zh" for Mandarin Chinese (has ISO 639-1 code)

#### Consistency Requirements

- A single STJ file MUST NOT mix ISO 639-1 and ISO 639-3 codes for the same language
- All references to a specific language within a file MUST use the same code consistently
- When a language has both ISO 639-1 and ISO 639-3 codes, the ISO 639-1 code MUST be used

#### Application Requirements

Applications MUST:

- Process both ISO 639-1 and ISO 639-3 codes
- Validate that:
  - ISO 639-1 codes are used when available
  - ISO 639-3 codes are only used for languages without ISO 639-1 codes
  - Language codes are used consistently throughout the file
- Reject files that:
  - Use ISO 639-3 codes for languages that have ISO 639-1 codes
  - Mix different standards for the same language
  - Contain invalid language codes

### URI Format Requirements

#### Purpose

Defines the format and constraints for the `uri` field in the `metadata.source` object.

#### Format Specifications

- **Type**: String representing a Uniform Resource Identifier (URI) as defined in [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986.html).
- **Allowed Schemes**:
  - **Recommended**:
    - `http`
    - `https`
    - `file`
  - **Optional**:
    - Other schemes (e.g., `ftp`, `s3`, `rtsp`) MAY be used if appropriate.
- **Absolute URIs**:
  - The `uri` SHOULD be an absolute URI, including the scheme component.
  - Examples:
    - `"http://example.com/media/video.mp4"`
    - `"https://example.com/media/audio.mp3"`
    - `"file:///C:/Media/video.mp4"` (Windows)
    - `"file:///home/user/media/audio.mp3"` (Unix-like systems)
- **Relative URIs**:
  - Relative URIs or file paths SHOULD NOT be used.
  - If a relative URI is provided, consuming applications MUST resolve it relative to a known base URI.
  - **Note**: Relative URIs can lead to ambiguity and are discouraged.

#### Validation Rules

- The `uri` MUST conform to the syntax defined in RFC 3986.
- Implementations SHOULD validate the URI format and report errors if invalid.
- **Scheme Support**:
  - **Required Support**:
    - Implementations MUST support `http` and `https` schemes.
  - **Optional Support**:
    - Support for other schemes is OPTIONAL and may vary between implementations.

#### Security Considerations

- **Privacy**:
  - Be cautious when including URIs that may reveal sensitive information, such as local file paths or internal network addresses.
  - Consider omitting the `uri` or sanitizing it if privacy is a concern.
- **Security Risks**:
  - Applications consuming STJ files SHOULD handle URIs carefully to avoid security risks such as directory traversal or accessing unauthorized resources.

#### Examples

- **HTTP URI**:

  ```json
  "uri": "http://example.com/media/video.mp4"
  ```

- **HTTPS URI**:

  ```json
  "uri": "https://example.com/media/audio.mp3"
  ```

- **File URI (Windows Path)**:

  ```json
  "uri": "file:///C:/Media/video.mp4"
  ```

- **File URI (Unix Path)**:

  ```json
  "uri": "file:///home/user/media/audio.mp3"
  ```

- **S3 URI (Optional Scheme)**:

  ```json
  "uri": "s3://bucket-name/path/to/object"
  ```

### Speaker IDs

#### Format Specifications

- **Type**: String
- **Allowed Characters**: Letters (A-Z, a-z), digits (0-9), underscores (_), and hyphens (-).
- **Length Constraints**:
  - Minimum length: 1 character
  - Maximum length: 64 characters
- **Uniqueness**:
  - Speaker IDs MUST be unique within the `speakers` list.
  - `speaker_id` references in segments MUST match an `id` in the `speakers` list.
- **Case Sensitivity**:
  - Speaker IDs are case-sensitive; `Speaker1` and `speaker1` are considered different IDs.
- **Format Recommendations**:
  - Use meaningful identifiers when possible, e.g., `Speaker_JohnDoe`.
  - For anonymous speakers, use generic IDs like `Speaker1`, `Speaker2`, etc.

#### Representing Anonymous Speakers

- **When the Speaker is Unknown or Anonymous**:
  - Use a consistent placeholder ID, such as `Speaker1`, `Speaker2`, etc.
  - The `name` field MAY be omitted or set to a placeholder like `"Unknown"` or `"Anonymous"`.
- **Consistency**:
  - Maintain consistent IDs for anonymous speakers throughout the transcript to differentiate between different speakers.
  - If speaker diarization is uncertain, it is acceptable to assign the same `speaker_id` to multiple segments where the speaker is believed to be the same.

#### Examples

- **Known Speaker**:

  ```json
  {
    "id": "Speaker_JohnDoe",
    "name": "John Doe"
  }
  ```

- **Anonymous Speaker**:

  ```json
  {
    "id": "Speaker1",
    "name": "Unknown"
  }
  ```

- **Multiple Anonymous Speakers**:

  ```json
  "speakers": [
    { "id": "Speaker1", "name": "Unknown" },
    { "id": "Speaker2", "name": "Unknown" },
    { "id": "Speaker3", "name": "Unknown" }
  ]
  ```

#### Validation Rules

- **ID Format Validation**:
  - IDs MUST only contain allowed characters.
  - IDs MUST meet the length constraints.
- **Uniqueness Validation**:
  - IDs in the `speakers` list MUST be unique.
  - Duplicate IDs MUST result in a validation error.
- **Reference Validation**:
  - All `speaker_id` references in segments MUST match an `id` in the `speakers` list.
  - Invalid references MUST result in a validation error.

#### Implementation Notes

- **Applications** SHOULD provide meaningful error messages when validation fails due to speaker ID issues.
- **When Generating STJ Files**:
  - Ensure that speaker IDs conform to the specified format requirements.
  - Assign consistent IDs to anonymous speakers to maintain differentiation.

### Style IDs

If `style_id` is used, it must match an `id` in the `styles` list.

### Text Fields

`text` fields should be in plain text format. Special formatting or markup should be handled via the `styles` mechanism.

### Word Timing Mode Field

#### Purpose

Indicates the completeness of word-level timing data within the segment.

#### Allowed Values

- `"complete"`: All words in the segment have timing data
- `"partial"`: Only some words have timing data
- `"none"`: No word-level timing data is provided

#### Default Behavior

- When omitted and `words` array is present with complete coverage: treated as `"complete"`
- When omitted and `words` array is absent: treated as `"none"`
- When omitted and `words` array is present but incomplete: invalid - must explicitly specify `"partial"`

#### Constraints

- For `"complete"`: All words must have timing data
- For `"partial"`: Some words must have timing data
- For `"none"`: Must not include `words` array

### Extensions Field Requirements

#### Purpose

The `extensions` field allows for the inclusion of custom, application-specific metadata and format-specific properties without affecting compatibility with other implementations.

#### Structure

- The `extensions` field, if present, **MUST** be a JSON object.
- Each key in `extensions` **MUST** represent a namespace and **MUST** be a non-empty string.
- The value corresponding to each namespace **MUST** be a JSON object containing key-value pairs specific to that namespace.

#### Namespaces

- **Namespace Naming:**
  - Namespaces **SHOULD** be concise and reflect the application, format, or organization.
  - Examples include `myapp`, `companyname`, `customformat`.
- **Reserved Namespaces:**
  - The following namespaces are **RESERVED** for future use by the STJ specification and **MUST NOT** be used for custom data:
    - `stj` (reserved for STJ specification extensions)
    - `webvtt` (reserved for WebVTT format mappings)
    - `ttml` (reserved for TTML format mappings)
    - `ssa` (reserved for SSA/ASS format mappings)
    - `srt` (reserved for SubRip format mappings)
    - `dfxp` (reserved for DFXP/Timed Text format mappings)
    - `smptett` (reserved for SMPTE-TT format mappings)
- **Developer Guidance:**
  - Developers who need to include format-specific properties before official definitions are available may:
    - Use a custom namespace that clearly indicates its provisional nature, such as `custom_webvtt` or `experimental_ttml`.
    - Be prepared to migrate their data to the official namespace once the STJ specification provides the definitions.

#### Constraints

- Applications **MUST** ignore any namespaces in `extensions` that they do not recognize.
- The `extensions` field **SHOULD NOT** include essential data required for basic functionality.
- Nested objects and arrays **ARE ALLOWED** within each namespace.
- Keys within namespaces **MUST NOT** duplicate or conflict with standard fields of the containing object.
- **Reserved Namespaces Validation:**
  - Namespaces listed as **RESERVED** in the specification **MUST NOT** be used by applications for custom data.
  - Applications **MUST** report an error if a reserved namespace is used.

#### Examples

- **In a `segment` object:**

  ```json
  "extensions": {
    "myapp": {
      "custom_property": "value",
      "analysis_data": {
        "sentiment_score": 0.85,
        "keywords": ["innovation", "technology"]
      }
    },
    "analytics": {
      "emotion": "happy",
      "confidence": 0.9
    }
  }
  ```

- **In a `style` object with format-specific properties:**

  ```json
  {
    "id": "caption_style",
    "text": {
      "color": "#FFFFFF",
      "background": "#000000"
    },
    "display": {
      "align": "center",
      "vertical": "bottom"
    },
    "extensions": {
      "custom_webvtt": {
        "line": "auto",
        "position": "50%",
        "size": "100%"
      },
      "myapp": {
        "custom_style_property": "value"
      }
    }
  }
  ```

- **In a `metadata` object:**

  ```json
  "extensions": {
    "project_info": {
      "project": "International Conference",
      "client": "Global Events Inc."
    },
    "notes": {
      "review_status": "approved",
      "reviewer": "John Doe"
    }
  }
  ```

**Note:** Standard fields defined in the STJ specification **MUST NOT** be duplicated within any namespace in `extensions`. For example, including a key `"start"` within a namespace is prohibited if it conflicts with the mandatory `"start"` field of the segment.

## Implementation Requirements

### Time Value Processing

Implementations MUST:

- Parse time values with up to 3 decimal places
- Preserve the precision of input values up to 3 decimal places
- Round any input with more than 3 decimal places to 3 decimal places using IEEE 754 round-to-nearest-even
- Validate all time values according to the Time Format Requirements section

Implementations MUST reject files that contain any of the following:

- Negative time values
- Values exceeding 999999.999 seconds
- Time values using scientific notation
- Overlapping segments

## Validation Requirements

### Segment-Level Validation

- **Required Fields**:
  - `start` and `end` times MUST conform to the Time Format Requirements section
  - `text` MUST be present and non-empty
- **References**:
  - `speaker_id`, if present, MUST match an `id` in the `speakers` list
  - `style_id`, if present, MUST match an `id` in the `styles` list
- **Segment Ordering**:
  - Segments MUST be ordered by their `start` times in ascending order
  - For segments with identical start times, they MUST be ordered by their end times in ascending order
- **Segment Overlap**:
  - Segments MUST NOT overlap in time
  - For any two segments S1 and S2 where S1 appears before S2 in the segments array:
    - S1.end MUST be less than or equal to S2.start
    - Examples of valid segment ordering:
      - Adjacent segments: S1(0.0, 1.0), S2(1.0, 2.0)
      - Segments with gap: S1(0.0, 1.0), S2(2.0, 3.0)
    - Examples of invalid segment ordering:
      - Overlapping segments: S1(0.0, 2.0), S2(1.0, 3.0)
      - Out of order segments: S1(1.0, 2.0), S2(0.0, 3.0)
- **Zero-Duration Segments**:
  - MUST follow the zero-duration requirements defined in the Time Format Requirements section
  - Zero-duration segments MAY share the same timestamp

### Word-Level Validation

- **When `words` array is present**:
  - Each word object must have `text`, `start`, and `end`
  - All time values must conform to the Time Format Requirements section
  - Word timing constraints:
    - Word times must be within the parent segment's time range
    - Words must be ordered by `start` time
    - Word timings must not overlap
- **Word Timing Mode Requirements**:
  - When `"complete"` (or omitted with complete coverage):
    - The concatenation of all `text` fields in `words` must match the segment's `text`, except for differences in whitespace or punctuation
  - When `"partial"`:
    - The `text` fields in `words` must be a subset of the words in the segment's `text`, in the same order
  - When `"none"` (or omitted without `words` array):
    - Must not contain `words` array
- **Zero-Duration Words**:
  - Must follow the zero-duration requirements defined in the Time Format Requirements section

### General Validation

- **URI Validation Requirements**:
  - The `uri` field in `metadata.source` MUST conform to the **URI Format Requirements** specified in the **Field Definitions and Constraints** section.
  - Implementations SHOULD validate the URI format according to RFC 3986.
  - Invalid URIs SHOULD result in a validation error or warning.
  - **Scheme Support**:
    - Implementations MUST support `http` and `https` schemes.
    - Support for other schemes is OPTIONAL.
  - **Relative URIs**:
    - Relative URIs SHOULD NOT be used.
    - If present, they MUST be resolved relative to a known base URI by the consuming application.

- **Language Code Requirements**:
  - All language codes must be valid ISO 639 codes
  - Language codes must be consistent with the requirements defined in the Language Codes section

- **Confidence Score Requirements**:
  - Confidence scores, if present, must be within the range [0.0, 1.0]

- **Reference Requirements**:
  - **Speaker IDs**:
    - All `speaker_id` references in segments MUST correspond to valid `id` entries in the `speakers` list.
    - All `id` values in the `speakers` list MUST conform to the **Speaker ID Requirements** specified in the **Field Definitions and Constraints** section.
    - All IDs in the `speakers` array MUST be unique.
    - IDs MUST only contain allowed characters and meet length constraints.
  - **Style IDs**:
    - All `style_id` references must correspond to valid entries in the `styles` list.
    - All IDs in the `styles` array MUST be unique.

- **Character Encoding Requirements**:
  - All text content must be valid UTF-8
  - All JSON string values must follow RFC 8259 encoding rules
  - Control characters must be properly escaped
  - Surrogate pairs must be properly formed
  - BOM must be handled correctly if present

### Extensions Field Validation

- **Structure Validation:**
  - The `extensions` field, if present, **MUST** be a JSON object.
  - Namespaces **MUST** be strings and **MUST NOT** be empty.
  - Values corresponding to namespaces **MUST** be JSON objects.

- **Reserved Namespaces Validation:**
  - Namespaces listed as **RESERVED** in the specification **MUST NOT** be used by applications for custom data.
  - Applications **MUST** report an error if a reserved namespace is used.

- **Content Validation:**
  - Applications **MUST** ignore any namespaces or keys within `extensions` that they do not recognize.
  - Values within namespaces **MAY** be validated based on application-specific requirements.

- **Conflict Resolution:**
  - If a key within a namespace in `extensions` conflicts with a standard field, the standard field's value **MUST** take precedence.
  - Applications **MUST** report an error if a conflict is detected.

### Style Processing

Implementations:

- MAY support none, some, or all style properties
- MUST ignore style properties they don't support
- MUST document which style properties they support
- SHOULD provide reasonable fallback behavior for unsupported properties

When converting STJ to other formats, implementations:

- SHOULD document how STJ style properties map to the target format's capabilities
- MAY omit style properties that cannot be represented in the target format

Advanced styling features (such as animations, karaoke effects, or complex positioning) SHOULD be implemented using format-specific properties within the `extensions` field under a namespace corresponding to the format.

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

- **Text Formatting**: Basic formatting supported via core style properties
- **Positioning**: Basic positioning supported via display properties
- **Advanced Features**: Can be represented via properties within the `custom_webvtt` namespace in `extensions`

### TTML (Timed Text Markup Language)

- **Basic Styling**: Supported via core style properties
- **Advanced Features**: Can be represented via properties within the `custom_ttml` namespace in `extensions`
- **Multiple Languages**: Supported via segment-level language codes

### SSA/ASS

- **Basic Styling**: Supported via core style properties
- **Advanced Features**: Can be represented via properties within the `custom_ssa` namespace in `extensions`

## Usage in Applications

The STJ format is designed to be easily parsed and utilized by a variety of applications, such as:

- **Transcription Editors**: Tools can load STJ files to display transcriptions with speaker labels, timestamps, and styling.
- **Subtitle Generators**: Applications can convert STJ segments into subtitle formats like SRT or WebVTT.
- **Speech Analytics**: Analyze transcriptions for sentiment, keyword extraction, or topic modeling.
- **Quality Assurance**: Reviewers can focus on low-confidence segments for correction.
- **Multilingual Support**: Applications can handle multilingual transcriptions by leveraging per-segment language data.

## Extensibility and Customization

- **Additional Metadata**: Use the `extensions` fields in both `metadata` and individual objects to include custom data without affecting compatibility.
- **Versioning**: Include a `version` field in `metadata` if needed for future format updates.
- **Custom Fields**: Applications can add custom data within appropriately named namespaces in the `extensions` field to include application-specific data without affecting compatibility.

## Adherence to Best Practices

The STJ format follows best practices for data interchange formats, drawing inspiration from established standards like:

- **IETF RFC 8259**: The STJ format adheres to the JSON standard as specified in [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html).
- **ISO 639 Language Codes**: Uses standard language codes to ensure consistency.
- **Dublin Core Metadata Initiative (DCMI)**: The metadata fields are designed to align with DCMI principles where applicable.
- **Naming Conventions**: Field names are concise and use lowercase letters with underscores for readability.
- **Extensibility**: The format allows for future expansion without breaking existing implementations.

## Final Remarks

The STJ format aims to be a comprehensive and flexible standard for transcription data representation. By incorporating features from existing formats and adhering to best practices, it strives to meet the needs of a wide range of applications and facilitate better interoperability in the field of speech transcription and subtitles.

---

**Note**: This specification is open for suggestions and improvements. Contributions from the community are welcome to refine and enhance the STJ format.

**Contact**: For feedback or contributions, please reach out via [The STJ Repository](https://github.com/yaniv-golan/STJ).
