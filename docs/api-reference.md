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
python stj_validator.py examples/complex.stj.json spec/schema/stj-schema.json
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
python stj_to_srt.py examples/complex.stj.json output.srt
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
python stj_to_vtt.py examples/complex.stj.json output.vtt
```

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
node stj-validator.js examples/complex.stj.json spec/schema/stj-schema.json
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
node stj-to-srt.js examples/complex.stj.json output.srt
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
node stj-to-vtt.js examples/complex.stj.json output.vtt
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
```
