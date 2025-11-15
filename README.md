# Standard Transcription JSON (STJ) Format

[![Specification Version](https://img.shields.io/badge/Specification-v0.6.1-blue.svg)](https://yaniv-golan.github.io/STJ/spec/latest/)
[![CI Status](https://img.shields.io/github/actions/workflow/status/yaniv-golan/STJ/ci.yml?branch=main&label=tests)](https://github.com/yaniv-golan/STJ/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/github/actions/workflow/status/yaniv-golan/STJ/docs.yml?branch=main&label=docs)](https://yaniv-golan.github.io/STJ/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yaniv-golan/STJ/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/yaniv-golan/STJ)](https://github.com/yaniv-golan/STJ/releases)

[![GitHub issues](https://img.shields.io/github/issues/yaniv-golan/STJ)](https://github.com/yaniv-golan/STJ/issues)
[![Contributors](https://img.shields.io/github/contributors/yaniv-golan/STJ)](https://github.com/yaniv-golan/STJ/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/yaniv-golan/STJ?style=social)](https://github.com/yaniv-golan/STJ)

## Introduction

The **Standard Transcription JSON (STJ)** format is a proposed standard for representing transcribed audio and video data in a structured, machine-readable JSON format. It aims to provide a comprehensive and flexible framework that is a superset of existing transcription and subtitle formats.

[Read the full specification](spec/latest/stj-specification.md) • [Published docs site](https://yaniv-golan.github.io/STJ/)

## Repository Structure

- **/spec**: The STJ format specification and schemas.
- **/examples**: Sample STJ files demonstrating various features.
- **/tools**: Scripts and libraries for working with STJ files.
- **/docs**: Documentation and guides.
- **/tests**: Unit tests for tools and validators.
- **/integrations**: Examples of integrating STJ with other services.
- **/benchmarks**: Performance benchmarking scripts.
- **/.github**: GitHub configuration files.

## Getting Started

To get started with STJ, please refer to the [Getting Started Guide](docs/getting-started.md).

## Installation

### Python Tools

Before running the Python tools, install the required packages. It's recommended to use a virtual environment.

**Using a Virtual Environment:**

```bash
# Navigate to the tools/python/ directory
cd tools/python/

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Without a Virtual Environment:**

```bash
pip install -r tools/python/requirements.txt
```

### JavaScript Tools

Before running the JavaScript tools, install the required packages using `npm`.

```bash
# Navigate to the tools/javascript/ directory
cd tools/javascript/

# Install dependencies
npm install
```

For more detailed installation instructions and troubleshooting, please refer to the [Installation Guide](docs/installation.md).

## Running Tests

### Python Tests

To run the Python tests:

```bash
cd tests/python/
pytest
```

### JavaScript Tests

To run the JavaScript tests:

```bash
# Navigate to the JavaScript tools directory
cd tools/javascript/

# Install dependencies (if not already installed)
npm install

# Run tests
npm test
```

### Continuous Integration

The repository uses GitHub Actions for continuous integration. Tests are automatically run on every push and pull request. The CI pipeline runs both Python and JavaScript tests in parallel.

## Contributing

Contributions are welcome! Please read our [Contribution Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## Documentation

- [API Reference](docs/api-reference.md)
- [Best Practices](docs/best-practices.md)
- [STJ Specification](spec/latest/stj-specification.md)

## Projects using STJ

- [YAWT](https://github.com/yaniv-golan/YAWT)
- [STJLib](https://github.com/yaniv-golan/stjlib)

## License

This project is licensed under the [MIT License](LICENSE).
