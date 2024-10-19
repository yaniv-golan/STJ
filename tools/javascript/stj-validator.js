const fs = require('fs');
const Ajv = require('ajv');

function validateSTJ(stjFilePath, schemaFilePath) {
  const stjData = JSON.parse(fs.readFileSync(stjFilePath, 'utf8'));
  const schema = JSON.parse(fs.readFileSync(schemaFilePath, 'utf8'));

  const ajv = new Ajv();
  const validate = ajv.compile(schema);
  const valid = validate(stjData);

  if (valid) {
    console.log(`${stjFilePath} is valid according to the schema.`);
  } else {
    console.error('Validation errors:', validate.errors);
  }
}

const stjFilePath = process.argv[2];
const schemaFilePath = process.argv[3];

if (!stjFilePath || !schemaFilePath) {
  console.error('Usage: node stj-validator.js <stj_file> <schema_file>');
  process.exit(1);
}

validateSTJ(stjFilePath, schemaFilePath);
