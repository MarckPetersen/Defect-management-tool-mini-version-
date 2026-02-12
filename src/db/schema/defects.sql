-- Defect Management Tool Database Schema

-- Users table to store user information
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'developer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Defects table to store defect/bug information
CREATE TABLE IF NOT EXISTS defects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')) DEFAULT 'Medium',
    status VARCHAR(20) CHECK (status IN ('Open', 'In Progress', 'Fixed', 'Closed', 'Reopened')) DEFAULT 'Open',
    priority INTEGER CHECK (priority BETWEEN 1 AND 5) DEFAULT 3,
    type VARCHAR(50) CHECK (type IN ('Bug', 'Enhancement', 'Task', 'Documentation')) DEFAULT 'Bug',
    assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reporter_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    environment VARCHAR(50) CHECK (environment IN ('Development', 'Staging', 'Production')) DEFAULT 'Production',
    affected_version VARCHAR(50),
    resolution VARCHAR(50) CHECK (resolution IN ('Fixed', 'Duplicate', 'Won''t Fix', 'Cannot Reproduce', 'Works as Designed')),
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table to store defect comments/discussions
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    defect_id INTEGER NOT NULL REFERENCES defects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attachments table to store file attachments related to defects
CREATE TABLE IF NOT EXISTS attachments (
    id SERIAL PRIMARY KEY,
    defect_id INTEGER NOT NULL REFERENCES defects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_defects_status ON defects(status);
CREATE INDEX IF NOT EXISTS idx_defects_severity ON defects(severity);
CREATE INDEX IF NOT EXISTS idx_defects_assignee ON defects(assignee_id);
CREATE INDEX IF NOT EXISTS idx_defects_reporter ON defects(reporter_id);
CREATE INDEX IF NOT EXISTS idx_defects_created_at ON defects(created_at);
CREATE INDEX IF NOT EXISTS idx_comments_defect ON comments(defect_id);
CREATE INDEX IF NOT EXISTS idx_attachments_defect ON attachments(defect_id);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_defects_updated_at BEFORE UPDATE ON defects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_comments_updated_at BEFORE UPDATE ON comments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
