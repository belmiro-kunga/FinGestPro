const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Account = sequelize.define('Account', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false
        },
        type: {
            type: DataTypes.ENUM('CHECKING', 'SAVINGS', 'CREDIT', 'INVESTMENT'),
            allowNull: false
        },
        balance: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false,
            defaultValue: 0
        },
        userId: {
            type: DataTypes.INTEGER,
            allowNull: false
        },
        synced: {
            type: DataTypes.BOOLEAN,
            defaultValue: false
        }
    });

    return Account;
};
