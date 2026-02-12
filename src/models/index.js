/**
 * Models index
 * Exports all model classes
 */

const Defect = require('./Defect');
const User = require('./User');
const Comment = require('./Comment');
const Attachment = require('./Attachment');

module.exports = {
  Defect,
  User,
  Comment,
  Attachment
};
