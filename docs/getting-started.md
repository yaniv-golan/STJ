# Getting Started with STJ

Welcome to the Standard Transcription JSON (STJ) format! This guide will help you get started with using STJ files.

## Prerequisites

- Basic knowledge of JSON.
- Python 3.x or Node.js installed, depending on the tools you wish to use.

## Validating an STJ File

To validate an STJ file using the provided Python script:

```bash
python tools/python/stj_validator.py examples/simple.stj.json spec/schema/stj-schema.json
```

## Converting STJ to SRT

To convert an STJ file to SRT:

```bash
python tools/python/stj_to_srt.py examples/simple.stj.json output.srt
```

## Further Reading

[Contribution Guide](./docs/contributing.md)

[STJ Specification](./spec/stj-specification.md)
[API Reference](./docs/api-reference.md)
[Best Practices](./docs/best-practices.md)