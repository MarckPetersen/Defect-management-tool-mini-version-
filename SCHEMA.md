# Database Schema Documentation

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ full_name       │
│ role            │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N (reporter_id)
         │ 1:N (assignee_id)
         │
         ▼
┌─────────────────────┐
│      defects        │
├─────────────────────┤
│ id (PK)             │
│ title               │
│ description         │
│ severity            │
│ status              │
│ priority            │
│ type                │
│ assignee_id (FK)    │◄──────┐
│ reporter_id (FK)    │       │
│ environment         │       │
│ affected_version    │       │
│ resolution          │       │
│ due_date            │       │
│ created_at          │       │
│ updated_at          │       │
└──────────┬──────────┘       │
           │                   │
           │ 1:N               │ N:1
           │                   │
     ┌─────┴──────┐      ┌────┴────────┐
     ▼            ▼      ▼             │
┌─────────┐  ┌─────────────┐           │
│comments │  │ attachments │           │
├─────────┤  ├─────────────┤           │
│id (PK)  │  │ id (PK)     │           │
│defect_id│  │ defect_id   │           │
│user_id  │──│ user_id     │───────────┘
│content  │  │ file_name   │
│created  │  │ file_path   │
│updated  │  │ file_size   │
└─────────┘  │ mime_type   │
             │ uploaded_at │
             └─────────────┘
```

## Table Details

### users
Stores user account information for the system.

**Columns:**
- `id`: Primary key, auto-incrementing integer
- `username`: Unique username (max 100 chars)
- `email`: Unique email address (max 255 chars)
- `full_name`: User's full name (optional)
- `role`: User role (admin, manager, developer, tester, viewer)
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp (auto-updated)

**Constraints:**
- Unique constraint on username
- Unique constraint on email

### defects
Main table for tracking defects, bugs, and enhancements.

**Columns:**
- `id`: Primary key, auto-incrementing integer
- `title`: Brief summary of the defect (max 255 chars, required)
- `description`: Detailed description (required)
- `severity`: Impact level (Low, Medium, High, Critical)
- `status`: Current state (Open, In Progress, Fixed, Closed, Reopened)
- `priority`: Priority level (1-5, where 1 is highest)
- `type`: Issue type (Bug, Enhancement, Task, Documentation)
- `assignee_id`: Foreign key to users (who is fixing it)
- `reporter_id`: Foreign key to users (who reported it)
- `environment`: Where found (Development, Staging, Production)
- `affected_version`: Product version affected
- `resolution`: Resolution reason (for closed items)
- `due_date`: Target completion date
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp (auto-updated)

**Constraints:**
- Check constraint on severity values
- Check constraint on status values
- Check constraint on priority range (1-5)
- Check constraint on type values
- Check constraint on environment values
- Check constraint on resolution values
- Foreign key to users (assignee_id) with SET NULL on delete
- Foreign key to users (reporter_id) with SET NULL on delete

**Indexes:**
- idx_defects_status on status
- idx_defects_severity on severity
- idx_defects_assignee on assignee_id
- idx_defects_reporter on reporter_id
- idx_defects_created_at on created_at

### comments
Discussion threads and comments on defects.

**Columns:**
- `id`: Primary key, auto-incrementing integer
- `defect_id`: Foreign key to defects (required)
- `user_id`: Foreign key to users (required)
- `content`: Comment text (required)
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp (auto-updated)

**Constraints:**
- Foreign key to defects with CASCADE on delete
- Foreign key to users with CASCADE on delete

**Indexes:**
- idx_comments_defect on defect_id

### attachments
File attachments associated with defects.

**Columns:**
- `id`: Primary key, auto-incrementing integer
- `defect_id`: Foreign key to defects (required)
- `user_id`: Foreign key to users (who uploaded)
- `file_name`: Original filename (max 255 chars)
- `file_path`: Storage path (max 500 chars)
- `file_size`: File size in bytes
- `mime_type`: MIME type of the file
- `uploaded_at`: Upload timestamp

**Constraints:**
- Foreign key to defects with CASCADE on delete
- Foreign key to users with CASCADE on delete

**Indexes:**
- idx_attachments_defect on defect_id

## Database Triggers

### update_updated_at_column()
Automatically updates the `updated_at` timestamp whenever a record is modified.

Applied to tables:
- users
- defects
- comments

## Data Integrity

The schema enforces data integrity through:

1. **Foreign Keys**: Ensures referential integrity between tables
2. **Check Constraints**: Validates enum values at the database level
3. **NOT NULL Constraints**: Ensures required fields are populated
4. **Unique Constraints**: Prevents duplicate usernames and emails
5. **Cascading Deletes**: Automatically cleans up related records
6. **Default Values**: Provides sensible defaults for optional fields

## Performance Optimizations

The schema includes several indexes for common query patterns:

1. **Status filtering**: Fast filtering by defect status
2. **Severity filtering**: Quick lookups by severity level
3. **User assignment**: Efficient queries for assigned/reported defects
4. **Date sorting**: Optimized sorting by creation date
5. **Related records**: Fast joins for comments and attachments

## Query Examples

### Find all critical open defects
```sql
SELECT * FROM defects 
WHERE severity = 'Critical' AND status = 'Open'
ORDER BY created_at DESC;
```

### Get defects assigned to a user
```sql
SELECT d.*, u.username as assignee_name
FROM defects d
LEFT JOIN users u ON d.assignee_id = u.id
WHERE d.assignee_id = 123;
```

### Get defect with all comments
```sql
SELECT d.*, c.content, c.created_at as comment_time, u.username
FROM defects d
LEFT JOIN comments c ON d.id = c.defect_id
LEFT JOIN users u ON c.user_id = u.id
WHERE d.id = 456
ORDER BY c.created_at ASC;
```

### Statistics by severity
```sql
SELECT severity, COUNT(*) as count
FROM defects
WHERE status != 'Closed'
GROUP BY severity
ORDER BY count DESC;
```
