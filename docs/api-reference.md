# API Reference

## Tools

### `stj_validator.py`

**Description**: Validates an STJ file against the STJ schema.

**Usage**:

```bash
python stj_validator.py <stj_file> <schema_file>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file to validate.
- `<schema_file>`: Path to the JSON schema file.

**Example**:

```bash
python stj_validator.py examples/multilingual.stj.json spec/schema/stj-schema.json
```

### `stj_to_srt.py`

**Description**: Converts an STJ file to an SRT subtitle file.

**Usage**:

```bash
python stj_to_srt.py <stj_file> <output_srt>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_srt>`: Path to the output SRT file.

**Example**:

```bash
python stj_to_srt.py examples/multilingual.stj.json output.srt
```

### `stj_to_vtt.py`

**Description**: Converts an STJ file to a WebVTT subtitle file.

**Usage**:

```bash
python stj_to_vtt.py <stj_file> <output_vtt>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_vtt>`: Path to the output VTT file.

**Example**:

```bash
python stj_to_vtt.py examples/multilingual.stj.json output.vtt
```

### `stj_to_ass.py`

**Description**: Converts an STJ file to an ASS (Advanced SubStation Alpha) subtitle file.

**Usage**:

```bash
python stj_to_ass.py <stj_file> <output_ass>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_ass>`: Path to the output ASS file.

**Example**:

```bash
python stj_to_ass.py examples/multilingual.stj.json output.ass
```

---

### `stj-validator.js`

**Description**: Validates an STJ file against the STJ schema using Node.js.

**Usage**:

```bash
node stj-validator.js <stj_file> <schema_file>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file to validate.
- `<schema_file>`: Path to the JSON schema file.

**Example**:

```bash
node stj-validator.js examples/multilingual.stj.json spec/schema/stj-schema.json
```

### `stj-to-srt.js`

**Description**: Converts an STJ file to an SRT subtitle file using Node.js.

**Usage**:

```bash
node stj-to-srt.js <stj_file> <output_srt>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_srt>`: Path to the output SRT file.

**Example**:

```bash
node stj-to-srt.js examples/multilingual.stj.json output.srt
```

### `stj-to-vtt.js`

**Description**: Converts an STJ file to a WebVTT subtitle file using Node.js.

**Usage**:

```bash
node stj-to-vtt.js <stj_file> <output_vtt>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_vtt>`: Path to the output VTT file.

**Example**:

```bash
node stj-to-vtt.js examples/multilingual.stj.json output.vtt
```

### `stj-to-ass.js`

**Description**: Converts an STJ file to an ASS (Advanced SubStation Alpha) subtitle file using Node.js.

**Usage**:

```bash
node stj-to-ass.js <stj_file> <output_ass>
```

**Arguments**:

- `<stj_file>`: Path to the STJ file.
- `<output_ass>`: Path to the output ASS file.

**Example**:

```bash
node stj-to-ass.js examples/multilingual.stj.json output.ass
```

---

## Modules

### Python

#### `stj_validator.py`

- **Function**: `validate_stj(stj_file, schema_file)`
  - Validates the STJ file against the schema.
- **Dependencies**:
  - `json`
  - `jsonschema`
  - `argparse`

#### `stj_to_srt.py`

- **Function**: `generate_srt(stj_data, output_srt_path)`
  - Converts STJ data to SRT format.
- **Dependencies**:
  - `json`
  - `srt`
  - `argparse`
  - `datetime.timedelta`

#### `stj_to_vtt.py`

- **Function**: `generate_vtt(stj_data, output_vtt_path)`
  - Converts STJ data to WebVTT format.
- **Dependencies**:
  - `json`
  - `webvtt`
  - `argparse`

#### `stj_to_ass.py`

- **Function**: `generate_ass(stj_data, output_ass_path)`
  - Converts STJ data to ASS format.
- **Dependencies**:
  - `json`
  - `argparse`
  - `datetime`

---

### JavaScript

#### `stj-validator.js`

- **Function**: `validateSTJ(stjFilePath, schemaFilePath)`
  - Validates the STJ file against the schema.
- **Dependencies**:
  - `fs`
  - `ajv`

#### `stj-to-srt.js`

- **Function**: `generateSRT(stjData, outputSrtPath)`
  - Converts STJ data to SRT format.
- **Dependencies**:
  - `fs`
  - `srt-parser-2`
  - `moment`

#### `stj-to-vtt.js`

- **Function**: `generateVTT(stjData, outputVttPath)`
  - Converts STJ data to WebVTT format.
- **Dependencies**:
  - `fs`
  - `node-webvtt`
  - `moment`

#### `stj-to-ass.js`

- **Function**: `generateASS(stjData, outputAssPath)`
  - Converts STJ data to ASS format.
- **Dependencies**:
  - `fs`
  - `process`

---

## Field Explanations

### `word_timing_mode`

- **Type**: String
- **Purpose**: Indicates the completeness of word-level timing data within a segment.
- **Allowed Values**:
  - `"complete"`
  - `"partial"`
  - `"none"`
- **Usage**: Used by applications to understand how to process the `words` array within a segment.

**Example**:

```json
{
  "word_timing_mode": "partial",
  "words": [
    { "start": 5.1, "end": 5.5, "text": "Gracias" }
    // Remaining words are not included
  ]
}
### `metadata.source.languages`

- **Type**: Array of strings (ISO 639-1 or ISO 639-3 codes)
- **Purpose**: Indicates the languages present in the source media.
- **Example**: `["en", "es", "de"]`

### `metadata.languages`

- **Type**: Array of strings (ISO 639-1 or ISO 639-3 codes)
- **Purpose**: Indicates the languages included in the transcription.
- **Example**: `["fr", "it"]`

---

## Notes on Language Fields

It's important to distinguish between the languages in the source media and those in the transcription, especially when translations are involved.

- **When the transcription is a direct transcription without translation**:
  - `metadata.source.languages` and `metadata.languages` may contain the same values.

- **When the transcription includes translations**:
  - `metadata.languages` will include the target language codes.
  - `metadata.source.languages` will remain unchanged, reflecting the original languages in the media.
