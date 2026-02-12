/**
 * Attachment Model
 * Represents a file attachment on a defect
 */

class Attachment {
  constructor(data = {}) {
    this.id = data.id || null;
    this.defectId = data.defect_id || data.defectId || null;
    this.userId = data.user_id || data.userId || null;
    this.fileName = data.file_name || data.fileName || '';
    this.filePath = data.file_path || data.filePath || '';
    this.fileSize = data.file_size || data.fileSize || null;
    this.mimeType = data.mime_type || data.mimeType || null;
    this.uploadedAt = data.uploaded_at || data.uploadedAt || null;
  }

  /**
   * Validates the attachment data
   * @returns {Object} { valid: boolean, errors: array }
   */
  validate() {
    const errors = [];

    // File name validation
    if (!this.fileName || this.fileName.trim().length === 0) {
      errors.push('File name is required');
    }

    // File path validation
    if (!this.filePath || this.filePath.trim().length === 0) {
      errors.push('File path is required');
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
      file_name: this.fileName,
      file_path: this.filePath,
      file_size: this.fileSize,
      mime_type: this.mimeType
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
      fileName: this.fileName,
      filePath: this.filePath,
      fileSize: this.fileSize,
      mimeType: this.mimeType,
      uploadedAt: this.uploadedAt
    };
  }

  /**
   * Static method to create an Attachment from database row
   * @param {Object} row - Database row
   * @returns {Attachment}
   */
  static fromDatabase(row) {
    return new Attachment(row);
  }
}

module.exports = Attachment;
