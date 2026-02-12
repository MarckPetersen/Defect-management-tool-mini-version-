/**
 * Comment Model
 * Represents a comment on a defect
 */

class Comment {
  constructor(data = {}) {
    this.id = data.id || null;
    this.defectId = data.defect_id || data.defectId || null;
    this.userId = data.user_id || data.userId || null;
    this.content = data.content || '';
    this.createdAt = data.created_at || data.createdAt || null;
    this.updatedAt = data.updated_at || data.updatedAt || null;
  }

  /**
   * Validates the comment data
   * @returns {Object} { valid: boolean, errors: array }
   */
  validate() {
    const errors = [];

    // Content validation
    if (!this.content || this.content.trim().length === 0) {
      errors.push('Content is required');
    }

    // Defect ID validation
    if (!this.defectId) {
      errors.push('Defect ID is required');
    }

    // User ID validation
    if (!this.userId) {
      errors.push('User ID is required');
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
      defect_id: this.defectId,
      user_id: this.userId,
      content: this.content
    };
  }

  /**
   * Converts the model to a JSON-ready object
   * @returns {Object}
   */
  toJSON() {
    return {
      id: this.id,
      defectId: this.defectId,
      userId: this.userId,
      content: this.content,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }

  /**
   * Static method to create a Comment from database row
   * @param {Object} row - Database row
   * @returns {Comment}
   */
  static fromDatabase(row) {
    return new Comment(row);
  }
}

module.exports = Comment;
