/**
 * Database Seed Script
 * Populates database with sample data for testing
 */

const { query, close } = require('../connection');

async function seed() {
  try {
    console.log('Starting database seeding...');
    
    // Insert sample users
    console.log('Inserting sample users...');
    await query(`
      INSERT INTO users (username, email, full_name, role)
      VALUES 
        ('admin', 'admin@example.com', 'Admin User', 'admin'),
        ('jdoe', 'jdoe@example.com', 'John Doe', 'developer'),
        ('asmith', 'asmith@example.com', 'Alice Smith', 'tester'),
        ('bwilson', 'bwilson@example.com', 'Bob Wilson', 'manager')
      ON CONFLICT (username) DO NOTHING
    `);
    
    // Get user IDs
    const usersResult = await query('SELECT id, username FROM users LIMIT 4');
    const users = usersResult.rows;
    
    if (users.length >= 2) {
      const reporter = users[1].id; // John Doe
      const assignee = users[2].id; // Alice Smith
      
      // Insert sample defects
      console.log('Inserting sample defects...');
      await query(`
        INSERT INTO defects (title, description, severity, status, priority, type, assignee_id, reporter_id, environment, affected_version)
        VALUES 
          ('Login button not working', 'When clicking the login button, nothing happens. No error message is displayed.', 'Critical', 'Open', 1, 'Bug', $1, $2, 'Production', '1.0.0'),
          ('Add dark mode feature', 'Users have requested a dark mode option for the application.', 'Low', 'Open', 4, 'Enhancement', NULL, $2, 'Development', '2.0.0'),
          ('Page loading slowly', 'The dashboard page takes more than 5 seconds to load.', 'High', 'In Progress', 2, 'Bug', $1, $2, 'Production', '1.2.0'),
          ('Update API documentation', 'API documentation needs to be updated with new endpoints.', 'Medium', 'Open', 3, 'Documentation', NULL, $2, 'Development', '1.3.0')
      `, [assignee, reporter]);
      
      // Get defect IDs
      const defectsResult = await query('SELECT id FROM defects LIMIT 2');
      const defects = defectsResult.rows;
      
      if (defects.length > 0) {
        // Insert sample comments
        console.log('Inserting sample comments...');
        await query(`
          INSERT INTO comments (defect_id, user_id, content)
          VALUES 
            ($1, $2, 'I can reproduce this issue on Chrome browser.'),
            ($1, $3, 'Working on a fix for this issue.')
        `, [defects[0].id, reporter, assignee]);
      }
    }
    
    console.log('Database seeding completed successfully!');
    
  } catch (error) {
    console.error('Seeding failed:', error.message);
    throw error;
  } finally {
    await close();
  }
}

// Run seeding if called directly
if (require.main === module) {
  seed()
    .then(() => {
      console.log('Seed script completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Seed script failed:', error);
      process.exit(1);
    });
}

module.exports = { seed };
