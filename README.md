# Defect Management Tool - Mini Version

A lightweight defect tracking system built with Node.js and PostgreSQL.

## Features

- **Defect Tracking**: Create, update, and track defects/bugs
- **User Management**: Multiple user roles (admin, manager, developer, tester, viewer)
- **Comments**: Add comments and discussions to defects
- **Attachments**: Upload files related to defects
- **Comprehensive Schema**: Well-structured database with proper relationships and constraints

## Database Schema

### Tables

1. **users** - Stores user information
   - id, username, email, full_name, role, created_at, updated_at

2. **defects** - Main defect tracking table
   - id, title, description, severity, status, priority, type
   - assignee_id, reporter_id, environment, affected_version
   - resolution, due_date, created_at, updated_at

3. **comments** - Comments on defects
   - id, defect_id, user_id, content, created_at, updated_at

4. **attachments** - File attachments for defects
   - id, defect_id, user_id, file_name, file_path, file_size, mime_type, uploaded_at

### Enumerations

- **Severity**: Low, Medium, High, Critical
- **Status**: Open, In Progress, Fixed, Closed, Reopened
- **Priority**: 1-5 (1 being highest)
- **Type**: Bug, Enhancement, Task, Documentation
- **Environment**: Development, Staging, Production
- **Resolution**: Fixed, Duplicate, Won't Fix, Cannot Reproduce, Works as Designed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MarckPetersen/Defect-management-tool-mini-version-.git
cd Defect-management-tool-mini-version-
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables (create a `.env` file):
```env
NODE_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=defect_management_dev
DB_USER=postgres
DB_PASSWORD=your_password
```

4. Create the database:
```bash
createdb defect_management_dev
```

5. Run database migrations:
```bash
node src/db/migrations/001_initial_schema.js
```

6. (Optional) Seed with sample data:
```bash
node src/db/migrations/002_seed_data.js
```

## Project Structure

```
.
├── config/
│   └── database.js          # Database configuration
├── src/
│   ├── db/
│   │   ├── connection.js    # Database connection pool
│   │   ├── migrations/      # Database migration scripts
│   │   │   ├── 001_initial_schema.js
│   │   │   └── 002_seed_data.js
│   │   └── schema/
│   │       └── defects.sql  # SQL schema definition
│   └── models/
│       ├── Defect.js        # Defect model
│       ├── User.js          # User model
│       ├── Comment.js       # Comment model
│       ├── Attachment.js    # Attachment model
│       └── index.js         # Models export
├── package.json
└── README.md
```

## Models

### Defect Model

```javascript
const { Defect } = require('./src/models');

// Create a new defect
const defect = new Defect({
  title: 'Bug in login',
  description: 'Users cannot login',
  severity: 'High',
  status: 'Open',
  priority: 1,
  type: 'Bug'
});

// Validate
const validation = defect.validate();
if (!validation.valid) {
  console.error(validation.errors);
}

// Convert to database format
const dbData = defect.toDatabase();
```

### User Model

```javascript
const { User } = require('./src/models');

const user = new User({
  username: 'jdoe',
  email: 'jdoe@example.com',
  fullName: 'John Doe',
  role: 'developer'
});
```

## Database Schema Features

- **Foreign Key Constraints**: Ensures referential integrity
- **Check Constraints**: Validates enum values at database level
- **Indexes**: Optimized for common query patterns
- **Triggers**: Automatic timestamp updates
- **Cascading Deletes**: Proper cleanup of related records

## Dependencies

- `pg`: PostgreSQL client for Node.js

Install dependencies:
```bash
npm install pg
```

## License

ISC