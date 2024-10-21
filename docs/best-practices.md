# Best Practices for Using STJ Format

## Introduction

The Standard Transcription JSON (STJ) format is designed to be flexible and comprehensive. Following best practices ensures consistency, interoperability, and ease of use across different applications and services.

## General Guidelines

### Consistent Field Usage

- **Mandatory Fields**: Always include all mandatory fields as specified in the STJ specification.
- **Optional Fields**: Use optional fields where appropriate to enhance the richness of the data.

### Data Types and Formats

- **Timestamps**: Represent all time fields (`start`, `end`) in seconds as floating-point numbers.
- **Language Codes**: Use standard ISO 639-1 or ISO 639-3 language codes.
- **Creation Timestamp**: Use the ISO 8601 format for the `created_at` field (e.g., `"2023-10-20T12:00:00Z"`).

### Naming Conventions

- **Field Names**: Use lowercase letters with underscores (`_`) for multi-word field names.
- **Identifiers**: Use unique strings for `id` fields in `speakers` and `styles`.

## Handling Languages

### Distinction Between Source and Transcription Languages

- **Source Languages (`metadata.source.languages`)**:
  - Represent the languages present in the original media.
  - Useful for understanding the content and planning transcription or translation processes.

- **Transcription Languages (`metadata.languages`)**:
  - Represent the languages included in the transcription.
  - May differ from source languages if translations are included.

### Per-Segment Language Annotation

- **Specify Language per Segment**:
  - Use the `language` field in each segment to indicate the language of the transcribed text.
  - Crucial for multilingual transcriptions and translations.

### Examples

- **Transcription with Translation**:
  - Source media contains English and Spanish.
  - Transcription includes translations into French and German.
  - `metadata.source.languages`: `["en", "es"]`
  - `metadata.languages`: `["fr", "de"]`

## Transcription Segments

### Time Alignment

- **Non-Overlapping Segments**: Ensure that segments do not overlap in time.
- **Sequential Order**: Segments should be ordered sequentially based on their `start` times.

### Speaker Identification

- **Consistent Speaker IDs**: Use consistent `speaker_id` values throughout the transcript.
- **Unknown Speakers**: If the speaker is unknown, omit the `speaker_id` field or use a placeholder like `"speaker_id": "Unknown"`.

### Language Annotation

- **Per-Segment Language**: Specify the `language` field for each segment in multilingual transcripts.
- **Default Language**: If the entire transcript is in a single language, specifying `language` in each segment is optional.

### Words Array

- **Detailed Word Data**: Include the `words` array in segments when word-level timing or confidence is needed.
- **Minimal Segments**: If word-level details are not required, omit the `words` array to reduce file size.

## Handling `word_timing_mode`

- **Complete Word Data**:
  - When `word_timing_mode` is `"complete"`, ensure that all words in the `text` field are represented in the `words` array.
- **Partial Word Data**:
  - When `word_timing_mode` is `"partial"`, include as many words as have timing data, and ensure they are in the correct order.
- **No Word Data**:
  - When there is no word-level timing data, you may omit the `words` array or set `word_timing_mode` to `"none"`.

## Styling

- **Use of Styles**: Define styles in the `styles` array and reference them in segments using `style_id`.
- **Default Styles**: If no styling is needed, omit the `styles` section.

## Confidence Scores

- **Including Confidence**: Provide `confidence` scores for segments and words when available.
- **Interpreting Confidence**: Use the `confidence_threshold` from metadata to determine if segments need review.

## Additional Information

- **Custom Data**: Use the `additional_info` field to include application-specific data.
- **Namespacing**: For custom fields, use a prefix (e.g., `x_custom_field`) to avoid conflicts with future specification updates.

## Metadata

### Accurate Source Information

- **Source URI**: Provide the `uri` in `metadata.source` if the source media is accessible.
- **Duration**: Ensure `duration` matches the actual length of the media.

### Creation Timestamp

- **ISO 8601 Format**: Use the ISO 8601 format for the `created_at` field (e.g., `"2023-10-20T12:00:00Z"`).

## Validation

- **Schema Validation**: Validate STJ files against the provided JSON schema to ensure compliance.
- **Automated Testing**: Incorporate validation into automated testing workflows.

## Interoperability

- **Compatibility**: When converting to other formats (e.g., SRT, VTT), ensure that essential information is preserved.
- **Extensions**: Avoid breaking changes when extending the format for specific needs.

## Performance Considerations

- **File Size**: Be mindful of file size, especially when including detailed word-level data.
- **Efficient Parsing**: Structure data to facilitate efficient parsing and processing by applications.

## Security

- **Data Sanitization**: Sanitize any user-generated content to prevent injection attacks.
- **Sensitive Information**: Avoid including sensitive personal information in the `additional_info` or other fields unless necessary and secured.

## Conclusion

By adhering to these best practices, you can ensure that your use of the STJ format is consistent, reliable, and compatible with a wide range of tools and applications.
