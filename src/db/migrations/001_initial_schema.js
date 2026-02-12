/**
 * Database Migration Script
 * Sets up the initial database schema
 */

const fs = require('fs');
const path = require('path');
const { query, close } = require('../connection');

async function migrate() {
  try {
    console.log('Starting database migration...');
    
    // Read the schema SQL file
    const schemaPath = path.join(__dirname, '../schema/defects.sql');
    const schemaSql = fs.readFileSync(schemaPath, 'utf8');
    
    // Execute the schema SQL
    await query(schemaSql);
    
    console.log('Database migration completed successfully!');
    console.log('Created tables: users, defects, comments, attachments');
    console.log('Created indexes for performance optimization');
    console.log('Created triggers for automatic timestamp updates');
    
  } catch (error) {
    console.error('Migration failed:', error.message);
    throw error;
  } finally {
    await close();
  }
}

// Run migration if called directly
if (require.main === module) {
  migrate()
    .then(() => {
      console.log('Migration script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Migration script failed:', error);
      process.exit(1);
    });
}

module.exports = { migrate };
