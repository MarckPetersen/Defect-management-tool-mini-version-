/**
 * Defect Model
 * Represents a defect/bug in the defect management system
 */

class Defect {
  constructor(data = {}) {
    this.id = data.id || null;
    this.title = data.title || '';
    this.description = data.description || '';
    this.severity = data.severity || 'Medium';
    this.status = data.status || 'Open';
    this.priority = data.priority || 3;
    this.type = data.type || 'Bug';
    this.assigneeId = data.assignee_id || data.assigneeId || null;
    this.reporterId = data.reporter_id || data.reporterId || null;
    this.environment = data.environment || 'Production';
    this.affectedVersion = data.affected_version || data.affectedVersion || null;
    this.resolution = data.resolution || null;
    this.dueDate = data.due_date || data.dueDate || null;
    this.createdAt = data.created_at || data.createdAt || null;
    this.updatedAt = data.updated_at || data.updatedAt || null;
  }

  /**
   * Validates the defect data
   * @returns {Object} { valid: boolean, errors: array }
   */
  validate() {
    const errors = [];

    // Title validation
    if (!this.title || this.title.trim().length === 0) {
      errors.push('Title is required');
    }
    if (this.title && this.title.length > 255) {
      errors.push('Title must be 255 characters or less');
    }

    // Description validation
    if (!this.description || this.description.trim().length === 0) {
      errors.push('Description is required');
    }

    // Severity validation
    const validSeverities = ['Low', 'Medium', 'High', 'Critical'];
    if (!validSeverities.includes(this.severity)) {
      errors.push('Severity must be one of: ' + validSeverities.join(', '));
    }

    // Status validation
    const validStatuses = ['Open', 'In Progress', 'Fixed', 'Closed', 'Reopened'];
    if (!validStatuses.includes(this.status)) {
      errors.push('Status must be one of: ' + validStatuses.join(', '));
    }

    // Priority validation
    if (this.priority < 1 || this.priority > 5) {
      errors.push('Priority must be between 1 and 5');
    }

    // Type validation
    const validTypes = ['Bug', 'Enhancement', 'Task', 'Documentation'];
    if (!validTypes.includes(this.type)) {
      errors.push('Type must be one of: ' + validTypes.join(', '));
    }

    // Environment validation
    const validEnvironments = ['Development', 'Staging', 'Production'];
    if (this.environment && !validEnvironments.includes(this.environment)) {
      errors.push('Environment must be one of: ' + validEnvironments.join(', '));
    }

    // Resolution validation (only for closed/fixed defects)
    if (this.resolution) {
      const validResolutions = ['Fixed', 'Duplicate', 'Won\'t Fix', 'Cannot Reproduce', 'Works as Designed'];
      if (!validResolutions.includes(this.resolution)) {
        errors.push('Resolution must be one of: ' + validResolutions.join(', '));
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Converts the model to a database-ready object
   * @returns {Object}
   */
  toDatabase() {
    return {
      title: this.title,
      description: this.description,
      severity: this.severity,
      status: this.status,
      priority: this.priority,
      type: this.type,
      assignee_id: this.assigneeId,
      reporter_id: this.reporterId,
      environment: this.environment,
      affected_version: this.affectedVersion,
      resolution: this.resolution,
      due_date: this.dueDate
    };
  }

  /**
   * Converts the model to a JSON-ready object
   * @returns {Object}
   */
  toJSON() {
    return {
      id: this.id,
      title: this.title,
      description: this.description,
      severity: this.severity,
      status: this.status,
      priority: this.priority,
      type: this.type,
      assigneeId: this.assigneeId,
      reporterId: this.reporterId,
      environment: this.environment,
      affectedVersion: this.affectedVersion,
      resolution: this.resolution,
      dueDate: this.dueDate,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }

  /**
   * Static method to create a Defect from database row
   * @param {Object} row - Database row
   * @returns {Defect}
   */
  static fromDatabase(row) {
    return new Defect(row);
  }
}

module.exports = Defect;
