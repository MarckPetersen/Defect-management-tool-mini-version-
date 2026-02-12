/**
 * Model Validation Test
 * Tests the defect model validation logic
 */

const { Defect, User, Comment, Attachment } = require('./src/models');

console.log('=== Testing Defect Management Tool Models ===\n');

// Test Defect Model
console.log('1. Testing Defect Model:');
const validDefect = new Defect({
  title: 'Test Bug',
  description: 'This is a test defect',
  severity: 'High',
  status: 'Open',
  priority: 2,
  type: 'Bug'
});

const defectValidation = validDefect.validate();
console.log('   Valid Defect:', defectValidation.valid ? '✓ PASS' : '✗ FAIL');
if (!defectValidation.valid) {
  console.log('   Errors:', defectValidation.errors);
}

// Test invalid defect
const invalidDefect = new Defect({
  title: '',
  description: '',
  severity: 'Invalid',
  priority: 10
});

const invalidValidation = invalidDefect.validate();
console.log('   Invalid Defect Detection:', !invalidValidation.valid ? '✓ PASS' : '✗ FAIL');
console.log('   Expected Errors:', invalidValidation.errors.length, 'errors found');

// Test User Model
console.log('\n2. Testing User Model:');
const validUser = new User({
  username: 'testuser',
  email: 'test@example.com',
  fullName: 'Test User',
  role: 'developer'
});

const userValidation = validUser.validate();
console.log('   Valid User:', userValidation.valid ? '✓ PASS' : '✗ FAIL');

const invalidUser = new User({
  username: '',
  email: 'invalid-email',
  role: 'invalid-role'
});

const invalidUserValidation = invalidUser.validate();
console.log('   Invalid User Detection:', !invalidUserValidation.valid ? '✓ PASS' : '✗ FAIL');

// Test Comment Model
console.log('\n3. Testing Comment Model:');
const validComment = new Comment({
  defectId: 1,
  userId: 1,
  content: 'This is a test comment'
});

const commentValidation = validComment.validate();
console.log('   Valid Comment:', commentValidation.valid ? '✓ PASS' : '✗ FAIL');

// Test Attachment Model
console.log('\n4. Testing Attachment Model:');
const validAttachment = new Attachment({
  defectId: 1,
  userId: 1,
  fileName: 'screenshot.png',
  filePath: '/uploads/screenshot.png',
  fileSize: 12345,
  mimeType: 'image/png'
});

const attachmentValidation = validAttachment.validate();
console.log('   Valid Attachment:', attachmentValidation.valid ? '✓ PASS' : '✗ FAIL');

// Test model serialization
console.log('\n5. Testing Model Serialization:');
const dbData = validDefect.toDatabase();
console.log('   toDatabase():', Object.keys(dbData).length > 0 ? '✓ PASS' : '✗ FAIL');

const jsonData = validDefect.toJSON();
console.log('   toJSON():', Object.keys(jsonData).length > 0 ? '✓ PASS' : '✗ FAIL');

// Test fromDatabase
console.log('\n6. Testing fromDatabase:');
const dbRow = {
  id: 1,
  title: 'DB Test',
  description: 'Test from DB',
  severity: 'Medium',
  status: 'Open',
  priority: 3,
  type: 'Bug'
};

const defectFromDb = Defect.fromDatabase(dbRow);
console.log('   fromDatabase():', defectFromDb.id === 1 && defectFromDb.title === 'DB Test' ? '✓ PASS' : '✗ FAIL');

console.log('\n=== All Model Tests Completed ===');
