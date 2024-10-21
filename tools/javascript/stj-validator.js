const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const fs = require('fs');
const path = require('path');

// Extract command-line arguments
const [ , , stjFilePath, schemaFilePath ] = process.argv;

// Validate input arguments
if (!stjFilePath || !schemaFilePath) {
  console.error('Usage: node stj-validator.js <stjFile> <schemaFile>');
  process.exit(1);
}

// Initialize AJV with allErrors option for detailed error reporting
const ajv = new Ajv({ allErrors: true });

// Integrate ajv-formats to support standard formats like "date-time"
addFormats(ajv);

// Load and parse the JSON schema
let schema;
try {
  schema = JSON.parse(fs.readFileSync(path.resolve(schemaFilePath), 'utf-8'));
} catch (err) {
  console.error('Error reading schema file:', err.message);
  process.exit(1);
}

// Compile the schema
let validate;
try {
  validate = ajv.compile(schema);
} catch (e) {
  console.error('Schema Compilation Error:', e.message);
  process.exit(1);
}

// Load and parse the STJ data file
let stjData;
try {
  stjData = JSON.parse(fs.readFileSync(path.resolve(stjFilePath), 'utf-8'));
} catch (err) {
  console.error('Error reading STJ file:', err.message);
  process.exit(1);
}

// Perform validation
const valid = validate(stjData);
if (valid) {
  console.log('The STJ file is valid according to the schema.');
  process.exit(0);
} else {
  console.error('Validation Errors:', validate.errors);
  process.exit(1);
}
