# Standard Transcription JSON (STJ) Format Specification

**Version**: 0.6.0
**Date**: 2024-10-27

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats such as SRT, WebVTT, TTML, SSA/ASS, and others.

The STJ format includes detailed transcription segments with associated metadata such as speaker information, timestamps, confidence scores, language codes, and styling options. It also allows for optional metadata about the transcription process, source input, and the transcriber application.

## RFC 2119 Key Words

This document uses requirement level keywords as defined in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt):

- **MUST**, **REQUIRED**, **SHALL**: The requirement is absolute.
- **MUST NOT**, **SHALL NOT**: The behavior/feature is absolutely prohibited.
- **SHOULD**, **RECOMMENDED**: There may be valid reasons to ignore this requirement, but implications must be understood and carefully weighed.
- **SHOULD NOT**, **NOT RECOMMENDED**: There may be valid reasons to allow this behavior, but implications must be understood and carefully weighed.
- **MAY**, **OPTIONAL**: The item is truly optional.

These keywords are presented in **UPPERCASE** throughout this document to indicate their special meanings.

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

The STJ files **MUST** include a `version` field within the `stj` section to indicate the specification version they comply with. This facilitates compatibility and proper validation across different implementations.

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

#### Examples of invalid root structures

- Invalid: **Missing mandatory fields:**

```json
{
  "stj": {}                    
}
```

- Invalid: **Missing transcript:**

```json
{
  "stj": {
    "version": "0.6.0"
  }
}
```

- Invalid: **Missing stj root object:**

```json
{
  "version": "0.6.0",         // ERROR: Missing stj root object
  "transcript": {}
}
```

### Mandatory vs. Optional Fields

- **Mandatory Fields**: Essential for basic functionality and compatibility.
  - `stj.version`
  - `transcript.segments` (array)
  - `transcript.segments[].text`
- **Optional Fields**: Provide additional information and features but are not required for basic use: All other fields, including `metadata`, `start`, `end`, `speakers`, `styles`, `speaker_id`, `confidence`, `language`, `style_id`, `words`, `word_timing_mode`, etc.

**Note**: If any segment includes timing information, both `start` and `end` become mandatory for that segment and all other segments in the transcript.

### Metadata Section

The `"metadata"` object is **OPTIONAL** and **MAY** include fields providing context about the transcription. The metadata object MAY be empty to indicate metadata processing was attempted but found no properties.

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
  "created_at": "2024-10-20T12:00:00Z",
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

- **speakers** *(array, optional)*: List of speaker objects. May be empty to indicate speaker identification was attempted but no speakers were found.
- **styles** *(array, optional)*: List of style definitions for formatting and positioning. May be empty to indicate style processing was performed but no styles were defined.
- **segments** *(array, mandatory)*: List of transcription segments.

#### Speakers

Each speaker object includes:

- **id** *(string, mandatory)*: Unique identifier for the speaker.
  - MUST conform to the **Speaker ID Requirements** specified in the **Field Definitions and Constraints** section.
- **name** *(string, optional)*: Display name of the speaker. May be empty to indicate an anonymous or unnamed speaker.
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

- **start** *(number, conditionally mandatory)*: Start time of the segment in seconds. If present, `end` **MUST** also be present.
- **end** *(number, conditionally mandatory)*: End time of the segment in seconds. If present, `start` **MUST** also be present.
- **is_zero_duration***(boolean)*: Indicates that the segment has zero duration.
  - **MUST** be present and set to `true` when `start` equals `end`
  - **MUST NOT** be present when `start` does not equal `end`
  - If present, **MUST** be `true`
- **text** *(string, mandatory)*: Transcribed text of the segment.
- **speaker_id** *(string, optional)*: The `id` of the speaker from the `speakers` list.
- **confidence** *(number, optional)*: Confidence score for the segment (0.0 - 1.0).
- **language** *(string, optional)*: Language code for the segment (ISO 639-1 or ISO 639-3).
- **style_id** *(string, optional)*: The `id` of the style from the `styles` list.
- **words** *(array, optional)*: List of word-level details. When present (in "complete" or "partial" modes), must contain at least one word. Must be omitted entirely (not included as empty) when using `word_timing_mode: "none"` for segments where word timing isn't applicable or fails.
  - **start** *(number, mandatory)*: Start time of the word in seconds.
  - **end** *(number, mandatory)*: End time of the word in seconds.
  - **is_zero_duration***(boolean)*: Indicates that the word has zero duration.
    - **MUST** be present and set to `true` when `start` equals `end`
    - **MUST NOT** be present when `start` does not equal `end`
    - If present, **MUST** be `true`
  - **text** *(string, mandatory)*: The word text.
  - **confidence** *(number, optional)*: Confidence score for the word (0.0 - 1.0).
- **word_timing_mode** *(string, optional)*: Indicates the completeness of word-level timing data within the segment.
- **extensions** *(object, optional)*: Any additional information about the segment.

##### Example

```json
{
  "stj": {
    "version": "0.6.0",
    "transcript": {
      "speakers": [
        {"id": "Speaker1", "name": "Speaker One"},
        {"id": "Speaker2", "name": "Speaker Two"},
        {"id": "Speaker3", "name": "Speaker Three"}
      ],
      "styles": [
        {
          "id": "Style1",
          "text": {
            "color": "#FFFFFF",
            "background": "#000000"
          }
        }
      ],
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
          "language": "en"
        }
      ]
    }
  }
}
```

In this example:

- The first segment has complete word-level data (`word_timing_mode`: `"complete"`).
- The second segment has partial word-level data (`word_timing_mode`: `"partial"`).
- The third segment is a zero-duration segment, which must not have word timing mode or words array.

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

**Note**: When optional fields are present but empty (empty arrays, objects, or strings), this indicates the field was processed but no content was found. When optional fields are omitted entirely, this indicates the field was not processed or is not applicable. See the Empty Value Constraints section under Structural Requirements for details.

## Field Definitions and Constraints

This section outlines the requirements and constraints for various fields used within the STJ format. It includes structural requirements, data type specifications, and detailed constraints for specific fields.

### Structural Requirements

### Default Behavior for Optional Fields

By default, optional fields **SHOULD** be omitted entirely when:

- The field is not applicable to the content
- The related feature or processing was not attempted
- There is no meaningful data to include

#### Empty Array Rules

- **Always Empty Allowed**:
  - `speakers`: When speaker identification attempted but none found
  - `styles`: When style processing performed but no styles defined
  
- **Never Empty Allowed**:
  - `segments`: Must contain at least one segment
  - `languages`: If present, **MUST** contain at least one entry
  - `words`: **MUST NOT** be empty in any word timing mode:
    - In "complete" mode: Must contain all words with timing
    - In "partial" mode: Must contain at least one word with timing
    - In "none" mode: Array must be entirely omitted
    - For segments where word timing fails or is not applicable: Use `word_timing_mode: "none"` and omit the array

#### Empty Object Rules

- **Always Empty Allowed**:
  - `metadata`: When processing occurred but found no properties
  - `extensions`: When processing occurred but found no valid extensions
- **Never Empty Allowed**:
  - Required object fields

#### Empty String Rules

- **Always Empty Allowed**:
  - `speaker.name`: For unnamed/anonymous speakers
- **Never Empty Allowed**:
  - All other string fields

When in doubt, omit optional fields entirely rather than including them as empty.

#### Empty Value Constraints

- **Null Values**:
  - Null values are **not allowed** for any field unless explicitly documented.
  - Optional fields **MUST** be omitted entirely rather than set to null unless explicitly documented as allowing null.
  - The `confidence` field **MAY** be null to indicate confidence scoring was attempted but failed.

##### Confidence Field Exception Details

The `confidence` field is allowed to be null because it represents three distinct states that need to be distinguishable:

1. **Field Omitted**: Confidence scoring was not attempted
2. **Null Value**: Confidence scoring was attempted but failed
3. **Numeric Value**: Confidence was successfully calculated (0.0 to 1.0)

Example:

```json
{
  "segments": [
    {
      "text": "Hello world",
      "confidence": null,     // Scoring attempted but failed
    },
    {
      "text": "Next segment" // No confidence scoring attempted
    },
    {
      "text": "Final segment",
      "confidence": 0.95     // Successfully scored
    }
  ]
}
```

Applications processing STJ files should:

- Treat a missing confidence field as "not attempted"
- Handle null confidence values as "attempted but failed"
- Process numeric confidence values normally

#### Empty Arrays

Optional arrays **MAY** be empty only in specific documented cases:

- **Mandatory Arrays**:
  - The `segments` array **MUST NOT** be empty.
    - **Severity if violated:** ERROR
  - The `languages` array, if present, **MUST** contain at least one entry.
    - **Severity if violated:** ERROR

- **Arrays That MAY Be Empty**:
  - `speakers`: Empty array indicates speaker identification was attempted but no speakers were found
  - `styles`: Empty array indicates style processing was performed but no styles were defined

- **Special Case - Words Array**:
  - The `words` array has specific rules:
    - In "complete" mode: **MUST** contain all words with timing
    - In "partial" mode: **MUST** contain at least one word
    - In "none" mode: **MUST NOT** be present at all (array must be omitted entirely)
    - Empty arrays are **NEVER** allowed in any mode
    - **Severity if violated:** ERROR
  - When word timing fails or isn't applicable:
    - Use `word_timing_mode: "none"`
    - Omit the `words` array entirely
    - Do not include an empty array

- **Default Behavior for Other Arrays**:
  - Arrays **SHOULD** be omitted entirely rather than included as empty unless explicitly documented as allowing empty state
  - Empty arrays in undocumented cases **SHOULD** result in a WARNING

##### Examples

Invalid cases:

```json
{
  "segments": [],        // Invalid: mandatory array must not be empty
  "languages": [],       // Invalid: if present, must contain at least one entry
  "word_timing_mode": "complete",
  "words": []           // Invalid: words array must not be empty when present
}
```

Guidance: Arrays **SHOULD** be omitted entirely (rather than included as empty) when:

- The feature was not processed or is not applicable
- The presence of the array itself would be misleading

#### Empty Objects

- Empty objects are **not allowed** for required object fields.
  - **Severity if violated:** ERROR
- The following optional objects **MAY** be empty with specific semantic meanings:
  - `metadata`: Empty object indicates metadata processing occurred but found no properties
  - `extensions`: Empty object indicates extension processing occurred but found no valid extensions
- Other optional objects **SHOULD** be omitted entirely rather than included as empty unless they represent an intentionally empty state that needs to be distinguished from "not processed" or "not applicable".
  - **Severity if violated:** WARNING

#### Empty Strings

- Empty strings are **not allowed** for any field except where explicitly documented.
- The following string fields **MAY** be empty with specific semantic meanings:
  - `speaker.name`: Empty string indicates an intentionally unnamed or anonymous speaker
- All other optional string fields **MUST** be omitted entirely rather than included as empty strings.

#### Empty Value Validation Requirements

Implementations **MUST** validate:

1. **Mandatory Arrays**
   - The `segments` array **MUST NOT** be empty
   - **Severity**: ERROR

2. **Optional Arrays**
   - Empty arrays are allowed only for:
     - `speakers`
     - `styles`
     - Other documented cases where empty state has semantic meaning
   - **Severity**: WARNING for unexpected empty arrays

3. **Objects**
   - Required objects **MUST NOT** be empty
   - Optional objects may be empty only for:
     - `metadata`
     - `extensions`
     - Other documented cases
   - **Severity**: WARNING for unexpected empty objects

4. **Default Field Omission**
   - Optional fields **SHOULD** be omitted rather than included empty
   - **Severity**: INFO when fields could be omitted

#### Handling Empty Arrays and Objects Examples

**Invalid Example of an Empty Mandatory `segments` Array:**

```json
{
  "segments": []
}
```

Explanation: The `segments` array is mandatory and must contain at least one segment. An empty `segments` array is invalid.

##### Example Validation Messages

- ERROR: "segments array must not be empty"
- WARNING: "empty array found for field 'custom_data' - consider omitting the field entirely"
- INFO: "empty metadata object found - consider omitting if no metadata processing was performed"

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
- Leading zeros are **not allowed** except for:
  - Decimal values less than 1 (e.g., `0.5`)
  - Time values, which follow the [Time Format Requirements](#time-format-requirements) specified in their dedicated section
- The negative zero value (`-0`) is **not allowed**.
- The values `Infinity`, `-Infinity`, and `NaN` are **not allowed**.

**Note:** For time-related fields (`start`, `end`), the [Time Format Requirements](#time-format-requirements) take precedence over these general number format requirements. See the [Time Format Requirements](#time-format-requirements) section for detailed specifications of time value formatting.

### Time Format Requirements

All time values in the STJ format (`start` and `end` fields) **MUST** follow these requirements:

#### Format Specifications {#format-specifications-1}

- **Type**: Non-negative decimal numbers
- **Precision Requirements**:
  - Input: Any number of decimal places allowed
  - Processing: Values with more than 3 decimal places MUST be rounded to 3 decimal places using IEEE 754 round-to-nearest-even
  - Storage: Maximum 3 decimal places (millisecond precision)
- **Range**: [0.000, 999999.999] seconds (after rounding).
  - The maximum value 999999.999 is inclusive. Any value that would round to greater than 999999.999 MUST be rejected, even if the unrounded value is less than 999999.999 (e.g., 999999.9994 is valid as it rounds to 999999.999, but 999999.9995 **MUST** be rejected as it would round to 1000000.000).
- **Significant Digits**: Must not exceed 6 digits before the decimal point
- **Formatting Rules**:
  - Leading zeros before the decimal point are allowed but not required
  - Trailing zeros after the decimal point are allowed but not required
  - The decimal point MUST be present if there are decimal places
  - Scientific notation is not allowed
  - Comma decimal separators are not allowed (**MUST** use period)

#### Basic Constraints

- For any segment or word:
  - `start` **MUST NOT** be greater than `end` (after rounding)
  - If either `start` or `end` is present, the other **MUST** also be present
  - Both values **MUST** be valid according to format specifications
- The `is_zero_duration` field:
  - **MUST** be present and set to `true` when `start` equals `end` (after rounding)
  - **MUST NOT** be present when `start` does not equal `end` (after rounding)
  - If present, **MUST** be `true`
  - For segments:
    - **MUST NOT** contain a `words` array
    - **MUST NOT** specify a `word_timing_mode`
- Including `is_zero_duration` when `start` does not equal `end` **MUST** result in an ERROR during validation

#### Examples of Time Values

Valid Input Values and Their Processing:

- `0` → stored as `0` or `0.0`
- `0.0` → stored as `0.0`
- `0.000` → stored as `0.000`
- `1.5` → stored as `1.5`
- `10.100` → stored as `10.100`
- `999999.999` → stored as `999999.999`

IEEE 754 Round-to-Nearest-Even Examples:

- `1.2345` → `1.235` (rounded up as 5 is even)
- `1.2335` → `1.234` (rounded up as 4 is even)
- `1.2325` → `1.232` (rounded down as 2 is even)
- `1.2315` → `1.232` (rounded up as 2 is even)
- `1.2305` → `1.230` (rounded down as 0 is even)

Edge Cases:

- `0.0005` → `0.001` (rounded up to even)
- `0.0015` → `0.002` (rounded up to even)
- `0.0025` → `0.002` (rounded down to even)
- `0.0035` → `0.004` (rounded up to even)
- `0.0045` → `0.004` (rounded down to even)

Invalid Values (Must Be Rejected):

- `-1.0` (negative values not allowed)
- `1.5e3` (scientific notation not allowed)
- `1000000.0` (exceeds maximum value)
- `999999.9995` (would round above maximum)
- `1,5` (incorrect decimal separator)
- Non-numeric values

**Note:** These requirements for time values take precedence over the general [Number Format Requirements](#number-format-requirements) when formatting time-related fields (`start` and `end`).

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
  - Mix standards across different languages.
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

#### Examples of invalid speaker references

- Invalid: **References non-existent speaker**

```json
{
  "speakers": [
    {"id": "Speaker1"}
  ],
  "segments": [{
    "speaker_id": "Speaker2"   
  }]
}
```

- Invalid: **Invalid character in ID**

```json
{
  "speakers": [
    {"id": "Speaker@1"},       
    {"id": "Speaker1"}
  ]
}
```

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

The `word_timing_mode` field indicates how word-level timing data is handled:

#### Allowed Values

- `"complete"`:
  - **MUST** include a `words` array
  - **MUST** have timing for every `word` in the segment
  - Concatenated `words[].text` **MUST** match segment `text` when normalized for whitespace
  - **MUST NOT** use for segments where word timing isn't applicable or fails
  
- `"partial"`:
  - **MUST** include a `words` array with at least one word
  - Words in array **MUST** appear in same order as in segment text
  
- `"none"`:
  - **MUST NOT** include a `words` array
  - Use for segments where:
    - Word timing wasn't attempted
    - Word timing isn't applicable (e.g., "[Music]", "[Applause]")
    - Word timing was attempted but failed

Empty `words` arrays are not allowed in any mode. For segments where:

- Word timing was attempted but failed
- Word timing isn't applicable
- Word timing wasn't attempted
Use `word_timing_mode: "none"` and omit the words array entirely.

#### Default Behavior

- When `word_timing_mode` is omitted and a `words` array is present with complete coverage: Treated as `"complete"`
- When `word_timing_mode` is omitted and no `words` array is present: Treated as `"none"`
- When `word_timing_mode` is omitted and `words` array is present but incomplete: Invalid—**MUST** explicitly specify `"partial"`

Note: Empty `words` arrays are never allowed. Use `word_timing_mode: "none"` and omit the array entirely when word timing isn't applicable, fails, or wasn't attempted.

#### Word Object Requirements

When word timing information is included (modes "complete" or "partial"), the `words` array **MUST** be present and each word object **MUST** include:

- `text` (string): The word text
- `start` (number): Start time in seconds
- `end` (number): End time in seconds
- `confidence` (number, optional): Confidence score for the word

Time values MUST follow the Time Format Requirements defined in this specification.

Note: For segments where word timing is not applicable or fails, use `word_timing_mode: "none"` and omit the `words` array entirely.

### Extensions Field Requirements

The `extensions` field allows applications to include custom data without affecting core STJ functionality.

#### Structure

- The `extensions` field, if present, **MUST** be a JSON object
- Each key in `extensions` **MUST** represent a namespace and **MUST** be a non-empty string
- Each namespace **MUST** contain a valid JSON object

#### Processing Rules

- Applications **MUST** ignore any namespaces they don't recognize
- Core STJ fields are authoritative for standard processing
- Extension data **MAY** provide supplementary information but **MUST NOT** override core field behavior

#### Reserved Namespaces

The following namespaces are **RESERVED** for future use by the STJ specification:

- `stj*` (reserved for STJ specification extensions)
- `webvtt` (reserved for WebVTT format mappings)
- `ttml` (reserved for TTML format mappings)
- `ssa` (reserved for SSA/ASS format mappings)
- `srt` (reserved for SubRip format mappings)
- `dfxp` (reserved for DFXP/Timed Text format mappings)
- `smptett` (reserved for SMPTE-TT format mappings)

Applications **MUST** report an error if a reserved namespace is used by applications for custom data

#### Best Practices

While not required, extension providers are encouraged to:

- Document the purpose and usage of their extension fields
- Use clear, descriptive namespace names
- Be especially clear when extension fields relate to core STJ concepts

#### Examples

Basic extension:

```json
"extensions": {
  "myapp": {
    "custom_field": "value",
    "analysis_data": {
      "property": "value"
    }
  }
}
```

Extension with format-specific properties:

```json
"extensions": {
  "custom_webvtt": {
    "line": "auto",
    "position": "50%"
  }
}
```

## Implementation Requirements

This section defines how implementations should process STJ files, including handling of optional fields, validation processing, and error reporting. It focuses on the practical aspects of implementing the specification.

### Handling of Optional Fields

Implementations **MUST** support files that include only the mandatory elements: `stj.version`, and `transcript.segments` with `text` values.

Implementations **SHOULD** gracefully handle the absence of optional fields and provide reasonable defaults or omit related functionalities.

For example, if timing information is absent, applications may treat the transcription as untimed text.

### Field-Specific Format Precedence

When multiple format requirements apply to a field, specific requirements take precedence over general requirements. The precedence order is:

1. Field-specific requirements (e.g., [Time Format Requirements](#time-format-requirements) for time fields)
2. Type-specific requirements (e.g., general [Number Format Requirements](#number-format-requirements))
3. Global format requirements

Examples:

- Time values may include leading zeros as specified in [Time Format Requirements](#time-format-requirements), despite the general prohibition in [Number Format Requirements](#number-format-requirements)
- Language codes must follow their specific format requirements regardless of general string formatting rules

### Time Value Processing

#### Processing Requirements

Implementations **MUST**:

1. **Input Validation**:
   - Accept numeric values with any number of decimal places
   - Accept time values with or without leading zeros
   - Verify decimal separator is period (.)
   - Check value is non-negative
   - Check value is not in scientific notation
   - Reject if exceeds maximum range (even if would round to valid value)
   - Example: reject `999999.9995` even though it would round to `1000000.000`, which exceeds the maximum allowed value of `999999.999`

2. **Precision Processing**:
   - Round values > 3 decimal places using IEEE 754 round-to-nearest-even
   - Preserve original precision up to 3 decimal places
   - Do not normalize to 3 decimal places
   - Example: `1.5` remains `1.5`, not normalized to `1.500`

3. **Output Requirements**:
   - Store values with maximum 3 decimal places
   - Preserve existing decimal places up to 3
   - Preserve leading zeros in time values when present
   - Not add or remove leading zeros when processing time values
   - Include decimal point if original value had decimal places
   - Do not add/remove trailing zeros

#### Time Value Validation Severity

- **ERROR Level** (Must reject file):
  - Negative values
  - Values exceeding range (before or after rounding)
  - Scientific notation
  - Non-numeric values
  - Incorrect decimal separator
  - Missing required time field when its pair is present

- **INFO Level**:
  - Rounding of values with more than 3 decimal places
  - Preservation of existing precision (not normalizing to 3 decimal places)

#### Error Handling for Time Values

Implementations **MUST**:

- **For Invalid Time Values (ERROR level)**:
  - Report specific validation failure (e.g., "negative value", "exceeds range")
  - Include the invalid value in error message
  - Reject the entire STJ file
  - Example message: "Error: Invalid time value -1.0 at segment[0].start (negative values not allowed)"

- **For Rounded Time Values (INFO level)**:
  - MAY report when rounding has occurred
  - Include original and rounded values in message
  - Example message: "Info: Time value 1.2345 rounded to 1.235 at segment[2].end"

Implementations **SHOULD**:

- Collect all time value errors before rejecting file
- Provide line/position information for errors when possible
- Include guidance in error messages about valid time formats

**Note**: These time value requirements apply to all time fields in the STJ format, including segment times (`start`, `end`) and word-level timing data. For validation severity levels and error handling requirements, see the [Validation Requirements](#validation-requirements) section.

### Error Handling

Implementations **MUST**:

- **For ERROR-level issues**:
  - Report the issues to the user or calling process.
  - **MUST NOT** proceed with processing the STJ file.
  - **Example ERROR issues**:
    - Overlapping segments.
    - Unordered segments.
    - Invalid references.
    - Missing required fields.
    - Malformed data.

- **For WARNING-level issues**:
  - Report the issues to the user or calling process.
  - **MAY** proceed with processing, but should do so cautiously.
  - **Example WARNING issues**:
    - Use of deprecated fields.
    - Non-standard language codes.

- **For INFO-level issues**:
  - Reporting is optional.
  - Processing should proceed normally.
  - **Example INFO issues**:
    - Suggestions for metadata enhancements.

Implementations **SHOULD** strive to provide meaningful feedback to users to improve the quality of STJ files.

## Validation Requirements

Implementations of the STJ format **MUST** perform validation that categorizes issues by severity levels. This section defines what must be validated, including validation rules and their associated severity levels. This approach ensures that:

- Users are informed about the nature of any issues found in STJ files
- Appropriate actions can be taken based on severity
- Validation is consistent across implementations

For details on how to implement these validation requirements, see the Implementation Requirements section.

### Severity Levels

The STJ specification uses three severity levels to indicate the impact of validation issues:

#### ERROR

- Definition: Critical issues that make the file semantically invalid or could cause incorrect processing
- Result: File MUST be rejected
- Examples:
  - Missing required fields
  - Invalid field types or values
  - Time value violations
  - Overlapping segments
  - Unordered segments
  - Invalid references
  - Malformed data

#### WARNING

- Definition: Issues that indicate potential problems but don't invalidate the file
- Result: Processing MAY continue with caution
- Examples:
  - Use of deprecated fields
  - Non-standard language codes
  - Non-optimal patterns
  - Unnecessary empty arrays/objects

#### INFO

- Definition: Suggestions for improvements or notifications of automatic adjustments
- Result: Processing continues normally
- Examples:
  - Time value rounding occurred
  - Metadata completeness suggestions
  - Efficiency recommendations
  - Style definition optimizations

### Validation Sequence

Implementations **SHOULD** perform validation in the following order:

1. **Structure Validation**:
   - JSON structure validity
   - Root object requirements
   - Required fields presence
   - Array and object structure rules

2. **Field Validation**:
   - Data type requirements
   - Value constraints
   - Format requirements

3. **Reference Validation**:
   - Speaker ID references
   - Style ID references
   - Language code consistency

4. **Content Validation**:
   - Segment timing rules
   - Word timing rules
   - Text content requirements

5. **Application-Specific Validation**:
   - Implementation-specific requirements
   - Custom extensions

This sequence aligns with the guidelines provided in the [Validation Requirements](#validation-requirements) section.

### Validation Categories and Rules

This section provides an overview of all validation requirements organized by category. Detailed rules can be found in their referenced sections.

#### Structure Validation

##### Basic File Structure

- JSON structure and encoding: See [Character Encoding Requirements](#character-encoding-requirements)
- Root object requirements: See [Root Structure](#root-structure)
- Additional properties restrictions: See [Root Structure](#root-structure)
- File extension requirements: See [Specification](#specification)

##### Empty Value Rules

- Null value restrictions: See [Empty Value Constraints](#empty-value-constraints)
- Empty array handling: See [Empty Array Rules](#empty-array-rules)
- Empty object handling: See [Empty Object Rules](#empty-object-rules)
- Empty string handling: See [Empty String Rules](#empty-string-rules)

##### Array Structure

- Array ordering requirements: See [Array Ordering Requirements](#array-ordering-requirements)
- Mandatory vs optional arrays: See [Empty Array Rules](#empty-array-rules)

#### Field-Specific Validation

##### Time Values

- Format and range requirements: See [Time Format Requirements](#time-format-requirements)
- Precision and rounding rules: See [Time Format Requirements](#time-format-requirements)
- Basic constraints: See [Basic Constraints](#basic-constraints) under Time Format Requirements
- Zero-duration requirements: See [Basic Constraints](#basic-constraints) under Time Format Requirements

##### Language Codes

- Standard requirements: See [Language Codes > Standards](#standards)
- Consistency requirements: See [Language Codes > Consistency Requirements](#consistency-requirements)
- Application requirements: See [Language Codes > Application Requirements](#application-requirements)

##### Speaker and Style IDs

- Format specifications: See [Speaker IDs > Format Specifications](#format-specifications)
- Uniqueness requirements: See [Speaker IDs > Validation Rules](#validation-rules)
- Reference validation: See [Speaker IDs > Examples of invalid speaker references](#examples-of-invalid-speaker-references)
- Style ID requirements: See [Style IDs](#style-ids)

##### URI Validation

- Format specifications: See [URI Format Requirements](#uri-format-requirements)
- Scheme support: See [URI Format Requirements > Format Specifications](#format-specifications-1)
- Security considerations: See [URI Format Requirements > Security Considerations](#security-considerations)

##### Metadata Validation

- Field requirements: See [Metadata Section > Fields](#fields)
- Language specifications: See [Metadata Section > Clarification on languages Fields](#clarification-on-languages-fields)

#### Content Validation

##### Segment Validation

- Required fields: See [Segment-Level Validation > Required Fields](#required-fields)
- Time field requirements: See [Segment-Level Validation > Time Fields](#time-fields)
- Reference validation: See [Segment-Level Validation > References](#references)
- Ordering requirements: See [Segment-Level Validation > Segment Ordering](#segment-ordering)
- Overlap restrictions: See [Segment-Level Validation > Segment Overlap](#segment-overlap)
- Zero-duration rules: See [Segment-Level Validation > Zero-Duration Segments](#zero-duration-segments)

##### Word Level Validation

- Required field validation: See [Word-Level Validation > Required Field Validation](#required-field-validation)
- Timing validation: See [Word-Level Validation > Timing Validation](#timing-validation)
- Mode-specific validation: See [Word-Level Validation > Mode-Specific Validation](#mode-specific-validation)
- Text alignment requirements: See [Word Text Alignment > Requirements](#requirements)

##### Extensions Validation

- Structure requirements: See [Extensions Field Requirements > Structure](#structure)
- Reserved namespace protection: See [Extensions Field Requirements > Reserved Namespaces](#reserved-namespaces)
- Processing rules: See [Extensions Field Requirements > Processing Rules](#processing-rules)

### Error Reporting Requirements

Implementations **MUST**:

- Provide clear error messages when **ERROR** level issues are detected.
- Include the JSON path to the problematic field in error messages.
- **MUST NOT** process the STJ file further if **ERROR** level issues are present.
- **SHOULD** report **WARNING** and **INFO** level issues to guide users.
- Report multiple validation issues when possible, rather than stopping at the first error.

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

### Segment-Level Validation {#segment-level-validation}

#### Required Fields {#required-fields}
- `text` **MUST** be present and non-empty.
  - **Severity if violated:** ERROR

#### Time Fields {#time-fields}
  - `start` and `end` times, if present, **MUST** conform to the [Time Format Requirements](#time-format-requirements) section.
    - **Severity if violated:** ERROR
  - If `start` equals end, `is_zero_duration` **MUST** be included and set to `true`.
    - **Severity if violated:** ERROR

#### References {#references}
  - `speaker_id`, if present, **MUST** match an `id` in the `speakers` list.
    - **Severity if violated:** ERROR
  - `style_id`, if present, **MUST** match an `id` in the `styles` list.
    - **Severity if violated:** ERROR

#### Segment Ordering {#segment-ordering}
  - Segments **MUST** be ordered by their `start` times in ascending order.
    - **Severity if violated:** ERROR
    - **Rationale**: Unordered segments can disrupt processing logic and lead to incorrect media synchronization.
  - For segments with identical start times, they **MUST** be ordered by their end times in ascending order.
    - **Severity if violated:** ERROR
    - **Rationale**: Consistent ordering is essential for predictable processing and display.
  - For segments with identical start and end times, the original array order **MUST** be preserved.
    - **Severity if violated:** ERROR
    - **Rationale**: Maintaining original order ensures stable sorting and preserves intended sequence of simultaneous events.

#### Segment Overlap {#segment-overlap}
  - Segments **MUST NOT** overlap in time.
    - **Severity if violated:** ERROR
    - **Rationale**: Overlapping segments create ambiguity about which text applies at what time and can cause rendering issues.
  - **Error Recovery Guidelines**:
    - While overlapping segments make an STJ file invalid, applications processing potentially invalid files **SHOULD** implement error recovery strategies rather than fail completely.
    - Recovery strategies **MAY** include:
      - Merging overlapping segments
      - Adjusting segment timings to eliminate overlaps
      - Alerting users to review and correct the overlaps
    - Applications implementing recovery strategies **MUST** still report the overlap as an ERROR during validation.

#### Zero-Duration Segments {#zero-duration-segments}
  - **MUST** follow the zero-duration requirements defined in the [Time Format Requirements](#time-format-requirements) section.
    - **Severity if violated:** ERROR
    - The presence of `is_zero_duration` when `start` does not equal `end` **MUST** result in an ERROR

#### Timing Consistency
  - If any segment in a transcript includes timing information (`start` and `end`), all segments in that transcript MUST include timing information.
    - **Severity if violated:** ERROR
    - **Rationale**: Mixed timed/untimed segments create ambiguity in processing and display.

#### Overlapping Segments Examples

**Example of Non-Compliant Overlapping Segments:**

```json
{
  "segments": [
    {
      "start": 5.0,
      "end": 10.0,
      "text": "First segment"
    },
    {
      "start": 8.0,
      "end": 12.0,
      "text": "Second segment"
    }
  ]
}
```

*Explanation*: The second segment starts at 8.0 seconds, which is before the end of the first segment at 10.0 seconds. This creates an overlap between 8.0 and 10.0 seconds, violating the requirement that segments **MUST NOT** overlap.

### Word-Level Validation

#### Required Field Validation

When the `words` array is present:

- Each word object **MUST** have:
  - `text` (string, non-empty)
  - `start` (number)
  - `end` (number)
  - **Severity if violated:** ERROR

#### Timing Validation

- Word times MUST be within the parent segment's time range
  - **Severity if violated:** ERROR
- Words MUST be ordered by `start` time
  - **Severity if violated:** ERROR
- Word timings SHOULD NOT overlap
  - **Severity if violated:** WARNING

#### Mode-Specific Validation

##### Complete Mode (`word_timing_mode: "complete"`)

The `words` array:

- **MUST** be present and non-empty
- **MUST** have concatenated `words[].text` match segment `text` when normalized for whitespace
- **MUST** have timing data for each word
- **Severity if violated:** ERROR

##### Partial Mode (`word_timing_mode: "partial"`)

The `words` array:

- **MUST** be present and contain at least one word
- **MUST** have each `words[].text` match a substring in segment `text`
- **MUST** have words appear in the same order as in segment `text`
- **Severity if violated:** ERROR

##### None Mode (`word_timing_mode: "none"`)

The `words` array:

- **MUST NOT** be present (array must be completely omitted, not included as empty)
- Use this mode for segments where:
  - Word timing wasn't attempted
  - Word timing isn't applicable
  - Word timing was attempted but failed
- **Severity if violated:** ERROR

#### Example of Failed Word Timing

```json
{
  "start": 15.0,
  "end": 20.0,
  "text": "Background noise made word timing impossible",
  "word_timing_mode": "none"
  // Note: words array is entirely omitted, not included as empty
}
```

### Word Text Alignment

#### Requirements

1. **Word Order**
   - Words in the `words` array MUST appear in the same order as they do in the segment's `text` field.
   - The text of each word in `words[].text` MUST match its corresponding occurrence in the segment's `text` field.

2. **Text Matching**
   - Implementations MUST preserve the exact text content of words, including:
     - Case sensitivity
     - Punctuation
     - Special characters
     - Whitespace within word boundaries (if any)

3. **Tokenization**
   - For `word_timing_mode: "complete"`:
     - The concatenated `words[].text` MUST match the segment's `text` when normalized for inter-word whitespace.
   - For `word_timing_mode: "partial"`:
     - Each `words[].text` MUST match a corresponding substring in the segment's `text`.
     - Words MUST be tokenized consistently within a segment.

#### Examples

1. **Complete Word Timing**:

```json
{
  "text": "Hello, world!",
  "word_timing_mode": "complete",
  "words": [
    {"text": "Hello,", "start": 0.0, "end": 0.5},
    {"text": "world!", "start": 0.6, "end": 1.0}
  ]
}
```

2. **Partial Word Timing:**

```json
{
  "text": "Hello, wonderful world!",
  "word_timing_mode": "partial",
  "words": [
    {"text": "Hello,", "start": 0.0, "end": 0.5},
    {"text": "world!", "start": 1.0, "end": 1.5}
  ]
}
```

3. **Complex Punctuation Example:**

```json
{
  "text": "\"Don't,\" she said, \"go there!\"",
  "word_timing_mode": "partial",
  "words": [
    {"text": "\"Don't,\"", "start": 0.0, "end": 0.5},
    {"text": "there!\"", "start": 1.0, "end": 1.5}
  ]
}
```

### Word Timing Implementation Notes

#### Tokenization Recommendations

1. **Basic Tokenization**
   - Split on whitespace as a baseline approach
   - Preserve punctuation attached to words
   - Keep contractions as single tokens
   - Maintain quotation marks with their associated words

2. **Edge Cases**
   - Multi-word expressions (e.g., "New York") should be treated as single tokens if timed as one unit
   - Hyphenated words should be kept as single tokens
   - Numbers, dates, and times should be treated as single tokens

#### Text Alignment Strategies

1. **For Complete Mode**:
   - Validate that all words are present
   - Compare normalized text (removing extra whitespace) to detect missing or extra words
   - Report specific mismatches to aid debugging

2. **For Partial Mode**:
   - Use string matching to verify word presence and order
   - Consider implementing fuzzy matching for robustness
   - Cache tokenization results for efficiency

#### Performance Considerations

- Consider caching tokenization results
- Use efficient string matching algorithms for validation
- Implement incremental validation for large documents

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
  - Language codes **MUST** use ISO 639-1 codes when available.
    - **Severity if violated:** ERROR
  - Language codes **MUST** be consistent throughout the file, using ISO 639-1 where available and ISO 639-3 only for languages without ISO 639-1 codes.
    - **Severity if violated:** ERROR

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

- **Time Value Requirements**:
  - All time values **MUST** conform to the [Time Format Requirements](#time-format-requirements) and Processing Requirements.
    - **Severity if violated:** ERROR
  - Input validation requirements **MUST** be checked before rounding.
    - **Severity if violated:** ERROR
  - Leading zeros in time values **MUST** be preserved if present.
    - **Severity if violated:** ERROR
  - Rounding of time values with more than 3 decimal places **MUST** be reported.
    - **Severity level:** INFO
  - Precision preservation requirements **MUST** be followed.
    - **Severity level:** INFO

### Extensions Field Validation

- **Structure Validation:**
  - The `extensions` field, if present, **MUST** be a JSON object
  - Namespaces **MUST** be strings and **MUST NOT** be empty
  - Values corresponding to namespaces **MUST** be JSON objects

- **Reserved Namespaces Validation:**
  - Namespaces listed as **RESERVED** **MUST NOT** be used by applications for custom data
  - Applications **MUST** report an error if a reserved namespace is used

- **Content Validation:**
  - Applications **MUST** ignore any namespaces they don't recognize
  - Values within namespaces **MAY** be validated based on application-specific requirements

- **Core Field Priority:**
  - When processing STJ files, applications **MUST** use core field values for standard functionality
  - Extension data **MUST NOT** override or alter the behavior of core fields

### Style Processing

Implementations:

- **MAY** support none, some, or all style properties
- **MUST** ignore style properties they don't support
- **MUST** document which style properties they support
- **SHOULD** provide reasonable fallback behavior for unsupported properties

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
