const { Sequelize } = require('sequelize');
const path = require('path');

// SQLite configuration (local/offline)
const sqliteConfig = new Sequelize({
    dialect: 'sqlite',
    storage: path.join(__dirname, '../../database.sqlite'),
    logging: false
});

// MySQL configuration (remote)
const mysqlConfig = new Sequelize({
    dialect: 'mysql',
    host: process.env.DB_HOST || 'localhost',
    username: process.env.DB_USER || 'root',
    password: process.env.DB_PASS || '',
    database: process.env.DB_NAME || 'fingestpro',
    logging: false
});

// Test database connections
async function testConnections() {
    try {
        await sqliteConfig.authenticate();
        console.log('SQLite connection established.');
    } catch (error) {
        console.error('Unable to connect to SQLite:', error);
    }

    try {
        await mysqlConfig.authenticate();
        console.log('MySQL connection established.');
    } catch (error) {
        console.error('Unable to connect to MySQL:', error);
    }
}

module.exports = {
    sqliteConfig,
    mysqlConfig,
    testConnections
};
