const { exec } = require('child_process');
const path = require('path');

test('Valid STJ file passes validation', (done) => {
  const validator = path.join(__dirname, '..', '..', 'tools', 'javascript', 'stj-validator.js');
  const stjFile = path.join(__dirname, '..', '..', 'examples', 'simple.stj.json');
  const schemaFile = path.join(__dirname, '..', '..', 'spec', 'schema', 'stj-schema.json');

  exec(`node ${validator} ${stjFile} ${schemaFile}`, (error, stdout, stderr) => {
    expect(error).toBeNull();
    expect(stdout).toContain('is valid according to the schema.');
    done();
  });
});
