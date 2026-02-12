/**
 * Database Connection
 * Manages PostgreSQL database connection pool
 */

const { Pool } = require('pg');
const dbConfig = require('../../config/database');

let pool = null;

/**
 * Get or create database connection pool
 * @returns {Pool}
 */
function getPool() {
  if (!pool) {
    pool = new Pool(dbConfig);
    
    pool.on('error', (err) => {
      console.error('Unexpected error on idle client', err);
      process.exit(1);
    });
  }
  
  return pool;
}

/**
 * Execute a query
 * @param {string} text - SQL query text
 * @param {Array} params - Query parameters
 * @returns {Promise<Object>}
 */
async function query(text, params) {
  const start = Date.now();
  const pool = getPool();
  
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: res.rowCount });
    return res;
  } catch (error) {
    console.error('Query error', { text, error: error.message });
    throw error;
  }
}

/**
 * Get a client from the pool for transactions
 * @returns {Promise<Client>}
 */
async function getClient() {
  const pool = getPool();
  return await pool.connect();
}

/**
 * Close the database connection pool
 * @returns {Promise<void>}
 */
async function close() {
  if (pool) {
    await pool.end();
    pool = null;
  }
}

module.exports = {
  query,
  getClient,
  getPool,
  close
};
