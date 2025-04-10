const { ipcMain } = require('electron');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class SyncHandler {
  constructor() {
    this.db = new sqlite3.Database(path.join(__dirname, '../database/fingestpro.db'));
    this.initializeDatabase();
    this.setupIpcHandlers();
  }

  initializeDatabase() {
    // Create sync tracking table if it doesn't exist
    this.db.run(`
      CREATE TABLE IF NOT EXISTS sync_tracking (
        table_name TEXT,
        record_id INTEGER,
        last_sync INTEGER,
        sync_status INTEGER DEFAULT 0,
        PRIMARY KEY (table_name, record_id)
      )
    `);

    // Add sync_status column to relevant tables if they don't exist
    const tables = [
      'products',
      'categories',
      'customers',
      'sales',
      'stock_movements',
      'transactions',
      'employees',
      'departments'
    ];

    tables.forEach(table => {
      this.db.run(`
        ALTER TABLE ${table} 
        ADD COLUMN sync_status INTEGER DEFAULT 0
      `, (err) => {
        if (err && !err.message.includes('duplicate column')) {
          console.error(`Error adding sync_status to ${table}:`, err);
        }
      });
    });
  }

  setupIpcHandlers() {
    // Get unsynchronized records
    ipcMain.handle('get-unsynced-records', async () => {
      return new Promise((resolve, reject) => {
        const unsyncedRecords = {};
        
        const tables = [
          'products',
          'categories',
          'customers',
          'sales',
          'stock_movements',
          'transactions',
          'employees',
          'departments'
        ];

        let completedTables = 0;

        tables.forEach(table => {
          this.db.all(
            `SELECT * FROM ${table} WHERE sync_status = 0`,
            (err, rows) => {
              if (err) {
                console.error(`Error getting unsynced records from ${table}:`, err);
                unsyncedRecords[table] = [];
              } else {
                unsyncedRecords[table] = rows;
              }

              completedTables++;
              if (completedTables === tables.length) {
                resolve(unsyncedRecords);
              }
            }
          );
        });
      });
    });

    // Mark records as synchronized
    ipcMain.handle('mark-records-synced', async (event, { table, ids }) => {
      return new Promise((resolve, reject) => {
        const placeholders = ids.map(() => '?').join(',');
        const query = `
          UPDATE ${table}
          SET sync_status = 1
          WHERE id IN (${placeholders})
        `;

        this.db.run(query, ids, function(err) {
          if (err) {
            console.error(`Error marking records as synced in ${table}:`, err);
            reject(err);
          } else {
            resolve({ success: true, count: this.changes });
          }
        });
      });
    });

    // Save server updates
    ipcMain.handle('save-server-updates', async (event, updates) => {
      return new Promise((resolve, reject) => {
        const results = {};
        let completedTables = 0;

        Object.entries(updates).forEach(([table, records]) => {
          this.db.serialize(() => {
            this.db.run('BEGIN TRANSACTION');

            records.forEach(record => {
              const { id, ...data } = record;
              const columns = Object.keys(data).join(', ');
              const values = Object.values(data);
              const placeholders = values.map(() => '?').join(', ');

              const query = `
                INSERT OR REPLACE INTO ${table} (${columns})
                VALUES (${placeholders})
              `;

              this.db.run(query, values, function(err) {
                if (err) {
                  console.error(`Error saving update to ${table}:`, err);
                  results[table] = { success: false, error: err.message };
                } else {
                  results[table] = { success: true, count: this.changes };
                }
              });
            });

            this.db.run('COMMIT', (err) => {
              if (err) {
                console.error(`Error committing updates to ${table}:`, err);
                results[table] = { success: false, error: err.message };
              }

              completedTables++;
              if (completedTables === Object.keys(updates).length) {
                resolve(results);
              }
            });
          });
        });
      });
    });
  }
}

module.exports = new SyncHandler(); 