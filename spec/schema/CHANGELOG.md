# CHANGELOG

## v0.6.0

### Added

- Introduced the `stj` top-level property, which encapsulates the entire schema.
- Implemented stricter validation for the `metadata` and `transcript` sections:
  - Enforced `minProperties` in objects for better compliance with the schema.
  - Added `minItems` validation for arrays (e.g., `languages` now requires at least one language).
  - Ensured stricter formatting rules for properties like `color`, `background`, `size`, and `position` in the `styles` section.
- Added `allOf` conditionals to validate that segments and words must have both `start` and `end` times when either is present.
- Added new constraints to the `extensions` field, enforcing `minProperties` and forbidding standard subtitle formats (e.g., `stj`, `webvtt`, etc.) to avoid conflicts.

### Changed

- `version` format validation updated to ensure semantic versioning patterns (e.g., `0.6.0`).
- Moved most properties inside the `stj` object, streamlining the schema structure.
- Enhanced the `confidence_threshold` validation to ensure it is between 0.0 and 1.0.
- Refined the `is_zero_duration` property across segments and words for additional precision handling.

### Removed

- `confidence` is no longer required in every segment or word, offering flexibility in cases where confidence data is unavailable.
- `word_timing_mode` options reduced, making this field optional with stricter values (`complete`, `partial`, `none`).
- The `additionalProperties: false` constraint now applied more widely across objects, ensuring strict validation of properties.

---

## v0.5.0

### Initial Version

- Defined the `metadata` and `transcript` sections, with required fields such as `created_at`, `version`, `transcriber`, and `segments`.
- Supported basic styling (`styles`) and segmentation (`segments`, `words`) with time precision.
- Allowed extensibility with the `extensions` property across several sections.
- Enforced semantic versioning patterns and `multipleOf` constraints on time-related properties.
