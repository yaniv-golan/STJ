# Changelog

# Changelog

## [0.6.0] - 2024-10-27

### Changed

- **File Extension**:
  - Selected `.stj.json` as the single primary file extension for consistency.
  - Removed alternative extensions to prevent confusion and encourage standardization.

- **Root Structure**:
  - Moved the `version` field from the `metadata` section to the root `"stj"` object.
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

  - Removed ordering requirements within JSON objects to align with JSON standards.

- **Mandatory Fields**:
  - Clarified that `transcript.segments[].start` and `transcript.segments[].end` are optional fields that become mandatory when timing information is included.
  - Updated the "Mandatory vs. Optional Fields Summary" to reflect these changes.

- **Handling of Anonymous Speakers**:
  - Specified that the `name` field **MUST** be omitted for anonymous speakers.
  - Updated examples to remove the `"name": "Unknown"` entries for anonymous speakers.
  - Ensured consistency in representing anonymous speakers throughout the document.

- **Time Format Requirements**:
  - Corrected grammatical errors for clarity.
  - Removed ordering constraints within JSON objects.
  - Emphasized that `is_zero_duration` **MUST** be included when `start` equals `end`, and **MUST NOT** be included otherwise.

- **Extensions Field Requirements**:
  - Corrected formatting errors and improved clarity regarding custom namespace guidelines.
  - Emphasized that applications **MUST** report an error if a reserved namespace is used.
  - Provided clearer guidance on using prefixes like `"custom_"` for provisional namespaces.

- **Validation Approach**:
  - Reordered validation steps for logical flow, moving "Extensions Validation" after "Application-Specific Validation".
  - Updated the "Validation Sequence" to reflect this change.

- **Best Practices and Compliance**:
  - Removed any ordering requirements within JSON objects, as JSON objects are unordered collections.
  - Ensured that all examples and guidelines align with JSON standards and best practices.
  - Maintained consistency in terminology and formatting throughout the document.

### Fixed

- **JSON Examples**:
  - Corrected all JSON examples to ensure validity.
  - Removed comments within JSON code blocks, as they are not allowed in JSON syntax.

- **Formatting Errors**:
  - Corrected typographical errors and improved overall formatting for better readability.
  - Ensured consistent use of terminology and style throughout the document.

- **Consistency Issues**:
  - Addressed inconsistencies regarding the usage of `is_zero_duration`.
  - Confirmed the consistent treatment of overlapping segments as **WARNING** level issues across all relevant sections.

### Added

- **Clarification on File Extensions**:
  - Added explanations on the rationale for selecting a single primary file extension.
  - Encouraged standardization to prevent confusion among users and developers.

- **Clarification on `start` and `end` Fields**:
  - Provided clear guidance on when `start` and `end` fields are required.
  - Emphasized that they become mandatory when timing information is included.

### Removed

- **Ordering Constraints in JSON Objects**:
  - Removed any statements imposing ordering on fields within JSON objects.

### Clarified

- **Usage of `extensions` Field**:
  - Provided clearer guidance on the usage of custom namespaces within the `extensions` field.
  - Encouraged developers to use prefixes like `"custom_"` to avoid conflicts with reserved namespaces.

- **Validation Requirements**:
  - Specified that implementations **MUST** perform validation in the sequence outlined to ensure consistency and completeness.
  - Clarified the severity levels for validation issues and the appropriate handling for each.

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
