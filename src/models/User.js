/**
 * User Model
 * Represents a user in the defect management system
 */

class User {
  constructor(data = {}) {
    this.id = data.id || null;
    this.username = data.username || '';
    this.email = data.email || '';
    this.fullName = data.full_name || data.fullName || '';
    this.role = data.role || 'developer';
    this.createdAt = data.created_at || data.createdAt || null;
    this.updatedAt = data.updated_at || data.updatedAt || null;
  }

  /**
   * Validates the user data
   * @returns {Object} { valid: boolean, errors: array }
   */
  validate() {
    const errors = [];

    // Username validation
    if (!this.username || this.username.trim().length === 0) {
      errors.push('Username is required');
    }
    if (this.username && this.username.length > 100) {
      errors.push('Username must be 100 characters or less');
    }

    // Email validation
    if (!this.email || this.email.trim().length === 0) {
      errors.push('Email is required');
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (this.email && !emailRegex.test(this.email)) {
      errors.push('Email must be a valid email address');
    }

    // Role validation
    const validRoles = ['admin', 'manager', 'developer', 'tester', 'viewer'];
    if (this.role && !validRoles.includes(this.role)) {
      errors.push('Role must be one of: ' + validRoles.join(', '));
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
      username: this.username,
      email: this.email,
      full_name: this.fullName,
      role: this.role
    };
  }

  /**
   * Converts the model to a JSON-ready object
   * @returns {Object}
   */
  toJSON() {
    return {
      id: this.id,
      username: this.username,
      email: this.email,
      fullName: this.fullName,
      role: this.role,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }

  /**
   * Static method to create a User from database row
   * @param {Object} row - Database row
   * @returns {User}
   */
  static fromDatabase(row) {
    return new User(row);
  }
}

module.exports = User;
