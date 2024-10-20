# Installation Guide

## Python Tools

### Prerequisites

- Python 3.6 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation Steps

1. **Navigate to the Python Tools Directory**

   ```bash
   cd tools/python/
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

The `requirements.txt` file includes:

- `srt>=3.5.2`
- `webvtt-py>=0.4.6`
- `jsonschema>=3.2.0`

## JavaScript Tools

### Prerequisites

- Node.js 12 or higher
- npm (comes with Node.js)

### Installation Steps

1. **Navigate to the JavaScript Tools Directory**

   ```bash
   cd tools/javascript/
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

### Dependencies

The `package.json` includes:

- `ajv`
- `moment`
- `node-webvtt`
- `srt-parser-2`

## Verifying Installation

To verify that the tools are installed correctly, you can run the following commands:

- **Python Validator:**

  ```bash
  python stj_validator.py ../../examples/simple.stj.json ../../spec/schema/stj-schema.json
  ```

- **JavaScript Validator:**

  ```bash
  node stj-validator.js ../../examples/simple.stj.json ../../spec/schema/stj-schema.json
  ```

If no errors are reported, the tools are installed and working properly.

## Troubleshooting

- **Python Issues:**

  - Ensure you're using the correct version of Python.
  - If you encounter permission issues, try running the command with `--user` or within a virtual environment.

- **JavaScript Issues:**

  - Ensure Node.js and npm are installed and updated.
  - If dependencies fail to install, check your internet connection or proxy settings.

---

For further assistance, please open an issue in the repository or contact the maintainers.