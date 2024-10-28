# Standard Transcription JSON (STJ) Format Specification

**Version**: 0.6.0
**Date**: 2024-10-27

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats such as SRT, WebVTT, TTML, SSA/ASS, and others.

The STJ format includes detailed transcription segments with associated metadata such as speaker information, timestamps, confidence scores, language codes, and styling options. It also allows for optional metadata about the transcription process, source input, and the transcriber application.

## Version History

For a detailed list of changes between versions, please see the [CHANGELOG.md](../CHANGELOG.md) file.

## Objectives

- **Interoperability**: Enable seamless data exchange between different transcription services and applications.
- **Superset of Existing Formats**: Incorporate features from common formats (SRT, WebVTT, TTML, etc.) to ensure compatibility and extensibility.
- **Extensibility**: Allow for future enhancements without breaking compatibility.
- **Clarity**: Provide a clear and well-documented structure for transcription data.
- **Utility**: Include useful metadata to support a wide range of use cases.
- **Best Practices Compliance**: Adhere to state-of-the-art best practices in metadata representation and documentation standards.

## Specification

- **File Extensions**:
  - Primary (Recommended): `.stjson`
  - Alternative: `.stj`
  - Alternative: `.stj.json` (systems supporting double extensions)
- **MIME Type**: `application/vnd.stj+json`
- **Character Encoding**: UTF-8

The STJ files must include a `version` field within the `stj` section to indicate the specification version they comply with. This facilitates compatibility and proper validation across different implementations.

### MIME Type Registration

The MIME type `application/vnd.stj+json` is designated for the STJ format. This MIME type is currently pending registration with the Internet Assigned Numbers Authority (IANA). Implementations **SHOULD** use this MIME type when serving STJ files over HTTP or in other contexts where MIME types are applicable.

Until the registration is finalized, applications **MAY** use `application/json` as a fallback but **SHOULD** transition to `application/vnd.stj+json` once registration is complete.

### Root Structure

The STJ file **MUST** contain a single JSON object with the root property name `"stj"`. This root object MUST contain the mandatory fields `version` and `transcript`, and **MAY** include the optional `metadata` field.

```json
{
  "stj": {
    "version": "0.6.0",
    "transcript": { ... }
  }
}
```

- **`version`**: Specifies the STJ specification version the file adheres to.
- **`transcript`**: Contains the actual transcription data, including segments (see the [Transcript Section](#transcript-section) for details).

The `"metadata"` field is optional and can be included to provide additional context (see the [Metadata Section](#metadata-section) for details).

```json
{
  "stj": {
    "version": "0.6.0",
    "metadata": { ... },
    "transcript": { ... }
  }
}
```

No additional properties are allowed at the root level.

### Mandatory vs. Optional Fields

- **Mandatory Fields**: Essential for basic functionality and compatibility.
  - `stj.version`
  - `transcript.segments` (array)
  - `transcript.segments[].text`
- **Optional Fields**: Provide additional information and features but are not required for basic use: All other fields, including `metadata`, `start`, `end`, `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, `word_timing_mode`, etc.

### Metadata Section

The `"metadata"` object is optional and can include fields providing context about the transcription.

#### Fields

- **transcriber** *(object, optional)*: Information about the transcriber application or service.
  - **name** *(string, optional)*: Name of the transcriber application.
  - **version** *(string, optional)*: Version of the transcriber application.
- **created_at** *(string, optional)*: ISO 8601 timestamp indicating when the transcription was created.
- **source** *(object, optional)*: Information about the source of the audio/video.
  - **uri** *(string, optional)*: The URI of the source media.
  - **duration** *(number, optional)*: Duration of the media in seconds.
  - **languages** *(array of strings, optional)*: List of languages present in the source media, ordered by prevalence.
- **languages** *(array of strings, optional)*: List of languages present in the transcription, ordered by prevalence.
- **confidence_threshold** *(number, optional)*: Confidence threshold used during transcription (0.0 - 1.0).
- **extensions** *(object, optional)*: A key-value map for any additional metadata.
  - MUST conform to the **Extensions Field Requirements** specified in the **Field Definitions and Constraints** section.
  **Note**: The `metadata` section is optional. Include it to provide additional context about the transcription as needed.

#### Example

```json
"metadata": {
  "transcriber": {
    "name": "YAWT",
    "version": "0.6.0"
  },
  "created_at": "2024-10-27T12:00:00Z"
},
```

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
    "languages": ["en", "es"] 
  },
  "languages": ["fr"],        
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
  { "id": "Speaker4" } 
]
```

In this example, Speaker4 is anonymous or unknown.

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
- **is_zero_duration***(boolean, mandatory if `start` equals `end`)*: Indicates that the segment has zero duration.
  - **MUST** be `true` if `start` equals `end`.
  - **MUST NOT** be included if `start` does not equal `end`.
- **text** *(string, mandatory)*: Transcribed text of the segment.
- **speaker_id** *(string, optional)*: The `id` of the speaker from the `speakers` list.
- **confidence** *(number, optional)*: Confidence score for the segment (0.0 - 1.0).
- **language** *(string, optional)*: Language code for the segment (ISO 639-1 or ISO 639-3).
- **style_id** *(string, optional)*: The `id` of the style from the `styles` list.
- **words** *(array, optional)*: List of word-level details.
  - **start** *(number, mandatory)*: Start time of the word in seconds.
  - **end** *(number, mandatory)*: End time of the word in seconds.
  - **is_zero_duration***(boolean, optional)*: Indicates that the word has zero duration.
    - **MUST** be `true` if `start` equals `end`.
    - **MUST NOT** be included if `start` does not equal `end`.
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
    ]
  },
  {
    "start": 10.1,
    "end": 10.1,
    "is_zero_duration": true,
    "text": "[Applause]",
    "speaker_id": "Speaker3",
    "confidence": 0.92,
    "language": "en",
    "word_timing_mode": "none"
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
{
 "stj": {
    "version": "0.6.0",
    "metadata": {
      "transcriber": {
        "name": "YAWT",
        "version": "0.4.0"
      },
      "created_at": "2024-10-20T12:00:00Z",
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
      ]
    }
  }
}
```

In this example:

- The source media languages are English (`"en"`) and Spanish (`"es"`).
- The transcription languages are French (`"fr"`) and German (`"de"`).
- Each segment indicates the language of the transcribed text.

### Optional vs. Mandatory Fields Summary

- **Mandatory Fields**:
  - `stj.version`
  - `transcript.segments` (array)
  - `transcript.segments[].text`
  - `transcript.segments[].start` (if timing information is relevant)
  - `transcript.segments[].end` (if timing information is relevant)

- **Optional Fields**:
  - `metadata` and all its subfields
  - `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, `word_timing_mode`, etc.

## Field Definitions and Constraints

This section outlines the requirements and constraints for various fields used within the STJ format. It includes structural requirements, data type specifications, and detailed constraints for specific fields.

### Structural Requirements

#### Empty Value Constraints

- **Null Values**:
  - Null values are **not allowed** for any field.
  - Optional fields **MUST** be omitted entirely rather than set to null.

#### Empty Arrays

- Empty arrays are **not allowed** for mandatory arrays (e.g., `segments`).
- Optional arrays (e.g., `speakers`, `styles`, `words`) **MUST** be omitted entirely rather than included as empty arrays.
- The `languages` array, if present, **MUST** contain at least one entry.
- **Words Array Constraints**:
  - If `word_timing_mode` is `"none"`, the `words` array **MUST NOT** be included.
  - If `word_timing_mode` is `"partial"`, the `words` array, if present, **MUST** contain at least one word object.

#### Empty Objects

- Empty objects are **not allowed** for any required object fields.
- Optional object fields **MUST** be omitted entirely rather than included as empty objects.
- The `extensions` object, if present, **MUST** contain at least one namespace.

#### Empty Strings

- Empty strings are **not allowed** for any field except where explicitly permitted.
- Optional string fields **MUST** be omitted entirely rather than included as empty strings.

#### Array Ordering Requirements

- **Ordered Arrays**:
  - The `segments` array **MUST** maintain temporal order based on `start` times.
  - The `words` array within segments **MUST** maintain temporal order based on `start` times.

- **Unordered Arrays**:
  - The `speakers` array order is **not significant**.
  - The `styles` array order is **not significant**.

#### String Content Requirements

- Leading and trailing whitespace in string values **MUST** be preserved.
- String values **MAY** contain multiple consecutive whitespace characters.
- Line breaks in string values **MUST** be preserved.

#### Number Format Requirements

- All numeric values **MUST** use JSON number format.
- Scientific notation is **not allowed**.
- Leading zeros are **not allowed** except for decimal values less than 1 (e.g., `0.5`).
- The negative zero value (`-0`) is **not allowed**.
- The values `Infinity`, `-Infinity`, and `NaN` are **not allowed**.

**Note:** Time values (e.g., `start`, `end`) have specific precision and format requirements as detailed in the [Time Format Requirements](#time-format-requirements) section. These requirements take precedence for time-related fields.

### Time Format Requirements

All time values in the STJ format (`start` and `end` fields) **MUST** follow these requirements:

#### Format Specifications

- **Type**: Non-negative decimal numbers.
- **Precision**: Up to 3 decimal places (millisecond precision).
- **Range**: `[0.000, 999999.999]` seconds.
- **Significant Digits**: Must not exceed 6 digits before the decimal point.
- **Formatting Rules**:
  - Leading zeros before the decimal point are **allowed** but not required.
  - Trailing zeros after the decimal point are **allowed** but not required.
  - The decimal point **MUST** be present if there are decimal places.
  - Scientific notation is **not allowed**.

#### Basic Constraints

- For any segment or word:
  - `start` **MUST NOT** be greater than `end`.
  - If either `start` **or** `end` is present, the other **MUST** also be present, and both **MUST** be valid according to format specifications.
- For zero-duration items (`start` equals `end`):
  - **MUST** include `is_zero_duration`: `true`.
  - For segments:
  
    - **MUST NOT** contain a `words` array.
    - **MUST NOT** specify a `word_timing_mode`.
  
  - The `is_zero_duration` field:
  
    - **MUST** be `true` if and only if `start` equals `end`.
    - **MUST NOT** be included when `start` does not equal `end`.
  
#### Examples of Valid Time Values

- `0` (zero seconds)
- `0.0` (zero seconds)
- `0.000` (zero seconds with full precision)
- `1.5` (one and a half seconds)
- `10.100` (ten seconds and one hundred milliseconds)
- `999999.999` (maximum allowed value)

#### Examples of Invalid Time Values

- `-1.0` (negative values not allowed)
- `1.5e3` (scientific notation not allowed)
- `1000000.0` (exceeds maximum value)
- `1.2345` (exceeds maximum precision)
- `1,5` (incorrect decimal separator)

### Character Encoding Requirements

#### Basic Requirements

- Files **MUST** be encoded in UTF-8.
- The UTF-8 Byte Order Mark (BOM) **MUST NOT** be used.
- JSON string values **MUST** follow [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) encoding rules.
- The full Unicode character set **MUST** be supported.

#### String Content Requirements

- All string values **MUST**:
  - Be valid UTF-8 encoded text.
  - Properly escape control characters (U+0000 through U+001F) using `\u` notation.
  - Properly handle surrogate pairs for supplementary plane characters.
- Forward slash (`/`) characters **MAY** be escaped but escaping is **not required**.
- Applications **MUST** properly handle and preserve escaped control characters when parsing and generating STJ files.
- **Unicode Normalization**:
  - All string values **SHOULD** be normalized to Unicode Normalization Form C (NFC).
  - Applications **MUST NOT** alter the normalization form of the text when storing or transmitting it, but **MAY** perform normalization internally for operations like comparison or searching.

### Confidence Scores

- **Type**: Floating-point numbers between `0.0` (no confidence) and `1.0` (full confidence).
- **Usage**: Optional but recommended for segments and words.
- **Purpose**: Provides an indication of the reliability of the transcribed text.

### Language Codes

#### Standards

- **Primary Standard**: ISO 639-1 (two-letter codes) **MUST** be used when available.
  - Examples: `"en"` for English, `"fr"` for French, `"es"` for Spanish.
- **Secondary Standard**: ISO 639-3 (three-letter codes) **MUST** be used only for languages without an ISO 639-1 code.
  - Example: `"yue"` for Cantonese (no ISO 639-1 code), but use `"zh"` for Mandarin Chinese (has ISO 639-1 code).

#### Consistency Requirements

- A single STJ file **MUST NOT** mix ISO 639-1 and ISO 639-3 codes for the same language.
- All references to a specific language within a file **MUST** use the same code consistently.
- When a language has both ISO 639-1 and ISO 639-3 codes, the ISO 639-1 code **MUST** be used.

#### Application Requirements

Applications **MUST**:

- Process both ISO 639-1 and ISO 639-3 codes.
- Validate that:
  - ISO 639-1 codes are used when available.
  - ISO 639-3 codes are only used for languages without ISO 639-1 codes.
  - Language codes are used consistently throughout the file.
- Reject files that:
  - Use ISO 639-3 codes for languages that have ISO 639-1 codes.
  - Mix different standards for the same language.
  - Contain invalid language codes.

### URI Format Requirements

#### Purpose

Defines the format and constraints for the `uri` field in the `metadata.source` object.

#### Format Specifications

- **Type**: String representing a Uniform Resource Identifier (URI) as defined in [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986.html).
- **Allowed Schemes**:
  - **Required Support**:
    - `http`
    - `https`
  - **Optional Support**:
    - Other schemes (e.g., `file`, `ftp`, `s3`, `rtsp`) **MAY** be used if appropriate.
- **Absolute URIs**:
  - The `uri` **SHOULD** be an absolute URI, including the scheme component.
  - Examples:
    - `"http://example.com/media/video.mp4"`
    - `"https://example.com/media/audio.mp3"`
    - `"file:///C:/Media/video.mp4"` (Windows)
    - `"file:///home/user/media/audio.mp3"` (Unix-like systems)
- **Relative URIs**:
  - Relative URIs or file paths **SHOULD NOT** be used.
  - If a relative URI is provided, consuming applications **MUST** resolve it relative to a known base URI.
  - **Note**: Relative URIs can lead to ambiguity and are discouraged.

#### Validation Rules

- The `uri` **MUST** conform to the syntax defined in RFC 3986.
- Implementations **SHOULD** validate the URI format and report errors if invalid.
- **Scheme Support**:
  - Implementations **MUST** support `http` and `https` schemes.
  - Support for other schemes is **optional** and may vary between implementations.

#### Security Considerations

- **Privacy**:
  - Be cautious when including URIs that may reveal sensitive information, such as local file paths or internal network addresses.
  - Consider omitting the `uri` or sanitizing it if privacy is a concern.
- **Security Risks**:
  - Applications consuming STJ files **SHOULD** handle URIs carefully to avoid security risks such as directory traversal or accessing unauthorized resources.

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

- **Type**: String.
- **Allowed Characters**: Letters (`A-Z`, `a-z`), digits (`0-9`), underscores (`_`), and hyphens (`-`).
- **Length Constraints**:
  - Minimum length: 1 character.
  - Maximum length: 64 characters.
- **Uniqueness**:
  - Speaker IDs **MUST** be unique within the `speakers` list.
  - `speaker_id` references in segments **MUST** match an `id` in the `speakers` list.
- **Case Sensitivity**:
  - Speaker IDs are case-sensitive; `Speaker1` and `speaker1` are considered different IDs.
- **Format Recommendations**:
  - Use meaningful identifiers when possible, e.g., `"Speaker_JohnDoe"`.
  - For anonymous speakers, use generic IDs like `"Speaker1"`, `"Speaker2"`, etc.

#### Representing Anonymous Speakers

- **When the Speaker is Unknown or Anonymous**:
  - Use a consistent placeholder ID, such as `"Speaker1"`, `"Speaker2"`, etc.
  - The `name` field **MUST** be omitted.
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
    "id": "Speaker1"
  }
  ```

- **Mixing Known and Anonymous Speakers**:

  ```json
  "speakers": [
    { "id": "Speaker1", "name": "John Doe"},
    { "id": "Speaker2"},
    { "id": "Speaker3"}
  ]
  ```

#### Validation Rules

- **ID Format Validation**:
  - IDs **MUST** only contain allowed characters.
  - IDs **MUST** meet the length constraints.
- **Uniqueness Validation**:
  - IDs in the `speakers` list **MUST** be unique.
  - Duplicate IDs **MUST** result in a validation error.
- **Reference Validation**:
  - All `speaker_id` references in segments **MUST** match an `id` in the `speakers` list.
  - Invalid references **MUST** result in a validation error.

#### Implementation Notes

- Applications **SHOULD** provide meaningful error messages when validation fails due to speaker ID issues.
- When generating STJ files:
  - Ensure that speaker IDs conform to the specified format requirements.
  - Assign consistent IDs to anonymous speakers to maintain differentiation.

### Style IDs

- If `style_id` is used in a segment, it **MUST** match an `id` in the `styles` list.
- Style IDs **MUST** adhere to the same format and uniqueness constraints as speaker IDs.

### Text Fields

- `text` fields **SHOULD** be in plain text format.
- Special formatting or markup **SHOULD** be handled via the `styles` mechanism.
- Line breaks and whitespace within `text` fields **MUST** be preserved.

### Word Timing Mode Field

#### Purpose

Indicates the completeness of word-level timing data within the segment.

#### Allowed Values

- `"complete"`: All words in the segment have timing data.
- `"partial"`: Only some words have timing data.
- `"none"`: No word-level timing data is provided.

#### Default Behavior

- When omitted and a `words` array is present with complete coverage: Treated as `"complete"`.
- When omitted and `words` array is absent: Treated as `"none"`.
- When omitted and `words` array is present but incomplete: Invalid—must explicitly specify `"partial"`.

#### Constraints

- For `"complete"`: All words **MUST** have timing data, and the concatenation of `words[].text` **SHOULD** match `segment.text`, accounting for whitespace and punctuation.
- For `"partial"`: Some words have timing data; the `words` array **MUST** contain at least one word object.
- For `"none"`: The `words` array **MUST NOT** be included.

### Extensions Field Requirements

#### Purpose

Allows for the inclusion of custom, application-specific metadata and format-specific properties without affecting compatibility with other implementations.

#### Structure

- The `extensions` field, if present, **MUST** be a JSON object.
- Each key in `extensions` **MUST** represent a namespace and **MUST** be a non-empty string.
- The value corresponding to each namespace **MUST** be a JSON object containing key-value pairs specific to that namespace.

#### Namespaces

##### Namespace Naming

- Namespaces **SHOULD** be concise and reflect the application, format, or organization.
- Examples include `"myapp"`, `"companyname"`, `"customformat"`.

##### Reserved Namespaces

- The following namespaces are **RESERVED** for future use by the STJ specification and **MUST NOT** be used for custom data:
  - `stj*` (reserved for STJ specification extensions)
  - `webvtt` (reserved for WebVTT format mappings)
  - `ttml` (reserved for TTML format mappings)
  - `ssa` (reserved for SSA/ASS format mappings)
  - `srt` (reserved for SubRip format mappings)
  - `dfxp` (reserved for DFXP/Timed Text format mappings)
  - `smptett` (reserved for SMPTE-TT format mappings)

**Applications MUST report an error** if a reserved namespace is used for custom data.

##### Custom Namespaces

Developers who need to include format-specific properties before official definitions are available:

- May use custom prefixes to create unique namespaces that avoid conflicts with reserved namespaces and clearly indicate their provisional nature, such as `"custom_webvtt"`, `"x_srt"`, or `"experimental_ttml"`.
- Be prepared to migrate their data to the official namespace once the STJ specification provides the definitions.

##### Examples

- **In a `segment` object**:

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

- **In a `style` object with format-specific properties**:

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

- **In a `metadata` object**:

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

#### Constraints

- Applications **MUST** ignore any namespaces in `extensions` that they do not recognize.
- The `extensions` field **SHOULD NOT** include essential data required for basic functionality.
- Nested objects and arrays **ARE ALLOWED** within each namespace.
- Keys within namespaces **MUST NOT** duplicate or conflict with standard fields of the containing object.

## Implementation Requirements

### Handling of Optional Fields

Implementations **MUST** support files that include only the mandatory elements: `stj.version`, and `transcript.segments` with `text` values.

Implementations **SHOULD** gracefully handle the absence of optional fields and provide reasonable defaults or omit related functionalities.

For example, if timing information is absent, applications may treat the transcription as untimed text.

### Time Value Processing

Implementations **MUST**:

- Parse time values with up to 3 decimal places.
- Preserve the precision of input values up to 3 decimal places.
- Round any input with more than 3 decimal places to 3 decimal places using IEEE 754 round-to-nearest-even.
- Validate all time values according to the [Time Format Requirements](#time-format-requirements) section.

Implementations **MUST** reject files that contain any of the following:

- Negative time values.
- Values exceeding 999999.999 seconds.
- Time values using scientific notation.

**Note:** Overlapping segments **SHOULD** be reported as warnings but do not require the file to be rejected.

### Error Handling

Implementations **MUST**:

- **For ERROR-level issues**:
  - Report the issues to the user.
  - **MUST NOT** proceed with processing the STJ file.
- **For WARNING-level issues**:
  - Report the issues to the user.
  - **MAY** proceed with processing, but **SHOULD** handle the potential inconsistencies.
- **For INFO-level issues**:
  - **MAY** report the issues to the user for informational purposes.
  - **MAY** proceed with processing without any changes.

Implementations **SHOULD** strive to provide meaningful feedback to users to improve the quality of STJ files.

## Validation Approach

Implementations of the STJ format **MUST** perform validation that categorizes issues by severity levels. This approach ensures that users are informed about the nature of any issues found in the STJ file and can take appropriate action based on the severity.

### Severity Levels

Validation issues are categorized into three severity levels:

1. **ERROR** (MUST violations)
   - Issues that make the STJ file invalid and unusable.
   - Examples:
     - Invalid JSON structure.
     - Missing mandatory fields (`stj.version`, `transcript.segments[].text`).
     - Malformed data types.

2. **WARNING** (SHOULD violations)
   - Issues that do not invalidate the STJ file but may lead to unexpected behavior.
   - Examples:
     - Duplicate speaker IDs.
     - Overlapping time segments.
     - Missing recommended fields.
     - Inconsistent language codes.

3. **INFO** (MAY violations)
   - Informational messages about optional best practices.
   - Examples:
     - Unused style definitions.
     - Missing optional metadata.
     - Unrecognized extensions.

### Validation Process

Implementations **SHOULD** follow these guidelines during validation:

- **Comprehensive Validation**:
  - Validate the entire STJ file, collecting all issues, rather than stopping at the first error.
- **Structured Reporting**:
  - Provide structured results with clear severity levels.
  - Include specific details about each issue.
- **Contextual Information**:
  - Include the JSON path to the problematic field.
  - Reference the relevant section of the specification.
  - Suggest possible fixes when appropriate.

### Response Format

Implementations **SHOULD** output validation results in a structured format, such as JSON, to facilitate automated processing.

**Example Response Format:**

```json
{
  "valid": false,
  "issues": [
    {
      "severity": "ERROR",
      "path": "transcript.segments[0].start",
      "code": "INVALID_TIME_FORMAT",
      "message": "Segment start time must be a non-negative number.",
      "specRef": "#time-format-requirements",
      "suggestion": "Ensure 'start' is a non-negative decimal number."
    },
    {
      "severity": "WARNING",
      "path": "transcript.segments[1]",
      "code": "OVERLAPPING_SEGMENTS",
      "message": "Segments should not overlap in time.",
      "specRef": "#segment-overlap",
      "suggestion": "Adjust segment timings to prevent overlap."
    },
    {
      "severity": "INFO",
      "path": "metadata",
      "code": "MISSING_METADATA",
      "message": "Including metadata can enhance the usefulness of the STJ file.",
      "specRef": "#metadata-section",
      "suggestion": "Consider adding a 'metadata' section."
    }
  ]
}
```

### Processing Instructions

Implementations **SHOULD** follow the validation sequence outlined in the [Validation Requirements](#validation-sequence) section to ensure consistency and completeness.

### Best Practices

- **Error Messages**:
  - Be specific and actionable.
  - Use consistent terminology.
  - Reference relevant specification sections.

- **Extensibility**:
  - Support custom validation rules if needed.
  - Allow users to filter or prioritize certain rules.

- **Performance**:
  - Optimize validation to handle large STJ files efficiently.
  - Avoid redundant checks by caching results when appropriate.

## Validation Requirements

### Validation Sequence

Implementations **SHOULD** perform validation in the following order:

1. **Structure Validation**:
   - Ensure the JSON structure is valid.
   - Validate that the root structure contains a single `"stj"` object with the required fields.
2. **Field Validation**:
   - Validate individual fields based on their definitions.
3. **Reference Validation**:
   - Check that references (e.g., `speaker_id`, `style_id`) are valid.
4. **Content Validation**:
   - Verify content-specific rules (e.g., timing overlaps).
5. **Application-Specific Validation**:
   - Perform any additional validations required by the application.
6. **Extensions Validation**:
   - Validate the `extensions` field structure and namespaces.

This sequence aligns with the guidelines provided in the [Validation Approach](#validation-approach) section.

### Error Reporting Requirements

Implementations **MUST**:

- Provide clear error messages when **ERROR** level issues are detected.
- Include the JSON path to the problematic field in error messages.
- **MUST NOT** process the STJ file further if **ERROR** level issues are present.
- **SHOULD** report **WARNING** and **INFO** level issues to guide users.
- Report multiple validation issues when possible, rather than stopping at the first error.

### Segment-Level Validation

- **Required Fields**:
  - `text` **MUST** be present and non-empty.
    - **Severity if violated:** ERROR
- **Time Fields**:
  - `start` and `end` times, if present, **MUST** conform to the [Time Format Requirements](#time-format-requirements) section.
    - **Severity if violated:** ERROR
  - If `start` equals end, `is_zero_duration` MUST be included and set to `true`.
    - **Severity if violated:** ERROR

- **References**:
  - `speaker_id`, if present, **MUST** match an `id` in the `speakers` list.
    - **Severity if violated:** ERROR
  - `style_id`, if present, **MUST** match an `id` in the `styles` list.
    - **Severity if violated:** ERROR

- **Segment Ordering**:
  - Segments **SHOULD** be ordered by their `start` times in ascending order.
    - **Severity if violated:** WARNING
  - For segments with identical start times, they **SHOULD** be ordered by their end times in ascending order.
    - **Severity if violated:** WARNING

- **Segment Overlap**:
  - Segments **SHOULD NOT** overlap in time.
    - **Severity if violated:** WARNING
  - **Guidelines for Overlapping Segments**:
    - Applications **SHOULD** handle overlapping segments gracefully, such as by merging or adjusting timings.
    - Overlapping segments **MAY** indicate issues with the data that users should review.

- **Zero-Duration Segments**:
  - **MUST** follow the zero-duration requirements defined in the [Time Format Requirements](#time-format-requirements) section.
    - **Severity if violated:** ERROR

### Word-Level Validation

- **When `words` array is present**:
  - Each word object **MUST** have `text`, `start`, and `end`.
    - **Severity if violated:** ERROR
  - All time values **MUST** conform to the [Time Format Requirements](#time-format-requirements) section.
    - **Severity if violated:** ERROR
  - Word timing constraints:
    - Word times **MUST** be within the parent segment's time range.
      - **Severity if violated:** ERROR
    - Words **MUST** be ordered by `start` time.
      - **Severity if violated:** ERROR
    - Word timings **SHOULD NOT** overlap.
      - **Severity if violated:** WARNING

### General Validation

- **URI Validation Requirements**:
  - The `uri` field in `metadata.source` **MUST** conform to the [URI Format Requirements](#uri-format-requirements).
    - **Severity if violated:** ERROR
  - Implementations **SHOULD** validate the URI format according to RFC 3986.
    - **Invalid URIs** **SHOULD** result in a **WARNING**.
  - **Relative URIs**:
    - Relative URIs **SHOULD NOT** be used.
      - **Severity if violated:** WARNING

- **Language Code Requirements**:
  - All language codes **MUST** be valid ISO 639 codes.
    - **Severity if violated:** ERROR
  - Language codes **SHOULD** be consistent throughout the file.
    - **Severity if violated:** WARNING

- **Confidence Score Requirements**:
  - Confidence scores, if present, **MUST** be within the range [0.0, 1.0].
    - **Severity if violated:** ERROR

- **Reference Requirements**:
  - **Speaker IDs**:
    - All `speaker_id` references in segments **MUST** correspond to valid `id` entries in the `speakers` list.
      - **Severity if violated:** ERROR
    - All IDs in the `speakers` array **MUST** be unique.
      - **Severity if violated:** ERROR
  - **Style IDs**:
    - All `style_id` references **MUST** correspond to valid entries in the `styles` list.
      - **Severity if violated:** ERROR
    - All IDs in the `styles` array **MUST** be unique.
      - **Severity if violated:** ERROR

- **Character Encoding Requirements**:
  - All text content **MUST** be valid UTF-8.
    - **Severity if violated:** ERROR
  - Control characters **MUST** be properly escaped.
    - **Severity if violated:** ERROR

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
- **Versioning**: The `version` field in the root `"stj"` object indicates the specification version. Applications **SHOULD** check this field to ensure compatibility.
- **Custom Fields**: Applications can add custom data within appropriately named namespaces in the `extensions` field to include application-specific data without affecting compatibility.

## Adherence to Best Practices

The STJ format follows best practices for data interchange formats, drawing inspiration from established standards like:

- **IETF RFC 8259**: The STJ format adheres to the JSON standard as specified in [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html).
- **ISO 639 Language Codes**: Uses standard language codes to ensure consistency.
- **Dublin Core Metadata Initiative (DCMI)**: The metadata fields are designed to align with DCMI principles where applicable.
- **Naming Conventions**: Field names are concise and use lowercase letters with underscores for readability.
- **Extensibility**: The format allows for future expansion without breaking existing implementations.

## Final Remarks

The STJ format is designed as a comprehensive and adaptable standard for transcription data representation. It establishes minimal mandatory requirements, allowing for straightforward implementations in basic scenarios while offering rich optional features for more complex applications.

By integrating elements from existing standards and following best practices, STJ aims to accommodate a wide range of use cases, promoting greater interoperability in speech transcription and subtitle applications. This flexible approach maximizes adoption potential and ensures future extensibility without compromising compatibility, providing a robust framework for diverse needs in the transcription and subtitle domain.

---

**Note**: This specification is open for suggestions and improvements. Contributions from the community are welcome to refine and enhance the STJ format.

**Contact**: For feedback or contributions, please reach out via [The STJ Repository](https://github.com/yaniv-golan/STJ).
