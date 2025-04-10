const { sqliteConfig, mysqlConfig } = require('./database');
const { User, Transaction, Account } = require('../models');

async function initializeDatabase() {
    try {
        // Sync SQLite models
        await sqliteConfig.sync({ force: true });
        console.log('SQLite database synchronized');

        // Create default admin user
        await User.create({
            username: 'admin',
            password: 'admin123', // This will be hashed by the User model hooks
            name: 'Administrador',
            email: 'admin@fingestpro.com'
        });

        // Sync MySQL models if connection is available
        try {
            await mysqlConfig.sync({ force: true });
            console.log('MySQL database synchronized');
        } catch (error) {
            console.warn('Could not sync MySQL database:', error.message);
        }

        console.log('Database initialization completed');
    } catch (error) {
        console.error('Error initializing database:', error);
        process.exit(1);
    }
}

// Run if this file is executed directly
if (require.main === module) {
    initializeDatabase();
}

module.exports = initializeDatabase;
