# Changelog

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
