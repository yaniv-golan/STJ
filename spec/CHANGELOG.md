# Changelog

## [0.6.0] - 2024-10-27

### Breaking Changes

- **File Extensions**:
  - Changed primary recommended extension from `.stj.json` to `.stjson`
  - Added `.stj` and `.stj.json` as alternative supported extensions
  - Applications should be updated to:
    - Recognize all three extensions (`.stjson`, `.stj`, `.stj.json`)
    - Use `.stjson` as default when creating new files
    - Continue supporting `.stj.json` for backward compatibility

- **Root Structure**:
  - Moved the `version` field from the `metadata` section to the root `"stj"` object
  - Updated the root structure to:

    ```json
    {
      "stj": {
        "version": "0.6.0",
        "metadata": { ... },
        "transcript": { ... }
      }
    }
    ```

  - Specified that no additional properties are allowed at the root level

- **Character Encoding Requirements**:
  - Changed UTF-8 Byte Order Mark (BOM) from optional to prohibited
  - Files **MUST** be encoded in UTF-8 without a BOM

### Changed

- **Mandatory Fields**:
  - Clarified that `transcript.segments[].start` and `transcript.segments[].end` are optional fields that become mandatory when timing information is included
  - Made the `metadata` section optional
  - Updated the "Mandatory vs. Optional Fields Summary" to reflect these changes

- **Handling of Anonymous Speakers**:
  - Specified that the `name` field **MUST** be omitted for anonymous speakers
  - Updated examples to remove the `"name": "Unknown"` entries for anonymous speakers
  - Ensured consistency in representing anonymous speakers throughout the document

- **Time Format Requirements**:
  - Specified the rounding rules for time values with more than 3 decimal places, using IEEE 754 round-to-nearest-even
  - Updated examples to illustrate the rounding behavior and edge cases
  - Emphasized that `is_zero_duration` **MUST** be included when `start` equals `end`, and **MUST NOT** be included otherwise
  - Added detailed processing requirements for time values, including validation severity levels

- **Extensions Field Requirements**:
  - Corrected formatting errors and improved clarity regarding custom namespace guidelines
  - Emphasized that applications **MUST** report an error if a reserved namespace is used
  - Provided clearer guidance on using prefixes like `"custom_"` for provisional namespaces

- **Validation Approach**:
  - Added explicit severity levels (ERROR, WARNING, INFO) for validation issues
  - Defined specific validation requirements and their corresponding severity levels
  - Added structured validation response format requirements
  - Reordered validation steps for logical flow
  - Added performance considerations for validation implementations
  - Required implementations to collect multiple validation issues when possible

- **Best Practices and Compliance**:
  - Removed any ordering requirements within JSON objects, as JSON objects are unordered collections
  - Ensured that all examples and guidelines align with JSON standards and best practices
  - Maintained consistency in terminology and formatting throughout the document

### Fixed

- **JSON Examples**:
  - Corrected all JSON examples to ensure validity
  - Removed comments within JSON code blocks, as they are not allowed in JSON syntax

- **Formatting Errors**:
  - Corrected typographical errors and improved overall formatting for better readability
  - Ensured consistent use of terminology and style throughout the document

- **Consistency Issues**:
  - Addressed inconsistencies regarding the usage of `is_zero_duration`
  - Updated examples to reflect the correct usage of `is_zero_duration`
  - Confirmed the consistent treatment of overlapping segments as **ERROR** level issues across all relevant sections

### Added

- **Empty Value Handling**:
  - Added explicit rules for handling empty arrays, objects, and strings
  - Specified which fields may be empty and which must be omitted
  - Added validation requirements for empty value handling

- **Validation Response Format**:
  - Added structured validation response format requirements
  - Specified required fields for validation responses (severity, path, code, message, etc.)
  - Added examples of proper validation response formatting

- **Clarification on `start` and `end` Fields**:
  - Provided clear guidance on when `start` and `end` fields are required
  - Emphasized that they become mandatory when timing information is included

- **RFC 2119 Key Words**:
  - Added a section defining the usage of requirement level keywords (MUST, SHOULD, etc.) as per RFC 2119
  - Ensured consistent use of these keywords throughout the document

### Removed

- **Ordering Constraints in JSON Objects**:
  - Removed any statements imposing ordering on fields within JSON objects

- **Mandatory `metadata` Section**:
  - Removed the requirement for the `metadata` section to be mandatory
  - Updated the specification to reflect that `metadata` is now optional

### Clarified

- **Usage of `extensions` Field**:
  - Provided clearer guidance on the usage of custom namespaces within the `extensions` field
  - Encouraged developers to use prefixes like `"custom_"` to avoid conflicts with reserved namespaces

- **Validation Requirements**:
  - Specified that implementations **MUST** perform validation in the sequence outlined to ensure consistency and completeness
  - Clarified the severity levels for validation issues and the appropriate handling for each
  - Added guidance on implementing error recovery strategies
  - Specified when recovery attempts are appropriate

- **Character Encoding Requirements**:
  - Clarified that the UTF-8 Byte Order Mark (BOM) **MUST NOT** be used
  - Provided guidance on proper handling of control characters and Unicode normalization

- **Time Value Processing**:
  - Clarified the processing and validation requirements for time values, including rounding rules and edge cases
  - Added examples to illustrate proper handling of time values

## [0.5.0] - 2024-10-24

### Added

- Comprehensive character encoding requirements:
  - Mandatory UTF-8 encoding with optional BOM
  - String content validation rules
  - Unicode normalization requirements
  - Character encoding validation requirements

- Detailed Speaker ID Requirements:
  - Format specifications for `speaker_id`
  - Allowed characters, length constraints
  - Uniqueness and case sensitivity rules
  - Guidelines for representing anonymous speakers

- Comprehensive time format requirements and constraints:
  - Specific implementation requirements for handling time values
  - Time value precision and range requirements
  - Consolidated time-related validation requirements

### Changed

- Renamed `additional_info` fields to `extensions` throughout the specification
- Introduced namespaces within the `extensions` field for structured custom data
- Reserved specific namespaces (`stj`, `webvtt`, `ttml`, `ssa`, `srt`, `dfxp`, `smptett`) for future official use
- Updated style definitions to use namespaced `extensions` instead of `x_` prefixed properties
- Changed zero-duration segment representation from `segment_duration` in `extensions` to a boolean `is_zero_duration` field
- Changed zero-duration word representation from `word_duration` in `extensions` to a boolean `is_zero_duration` field

### Clarified

- Default behavior of the `word_timing_mode` field when omitted:
  - Treated as `"complete"` when the `words` array is present with complete coverage
  - Treated as `"none"` when the `words` array is absent
  - Invalid when the `words` array is present but incomplete (must explicitly specify `"partial"`)
- Added explicit validation rules for each `word_timing_mode` value
- Standardized cross-references to the Time Format Requirements section throughout the document

## [0.4.0] - 2024-10-23

### Added

- `word_timing_mode` field in segments to indicate the completeness of word-level timing data
- Validation requirements for all parts of the JSON:
  - Segments
  - Words
  - Speakers
  - Styles
  - Additional fields

### Changed

- Clarified the relationship between segment-level text and word-level details, accounting for `word_timing_mode`

### Added

- Additional examples demonstrating the use of `word_timing_mode`
