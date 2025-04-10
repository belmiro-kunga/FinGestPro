const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Sale = sequelize.define('Sale', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        number: {
            type: DataTypes.STRING,
            unique: true,
            allowNull: false
        },
        type: {
            type: DataTypes.ENUM('sale', 'return'),
            defaultValue: 'sale'
        },
        customerId: {
            type: DataTypes.INTEGER
        },
        employeeId: {
            type: DataTypes.INTEGER,
            allowNull: false
        },
        date: {
            type: DataTypes.DATE,
            allowNull: false,
            defaultValue: DataTypes.NOW
        },
        subtotal: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false
        },
        taxTotal: {
            type: DataTypes.DECIMAL(10, 2),
            defaultValue: 0
        },
        discount: {
            type: DataTypes.DECIMAL(10, 2),
            defaultValue: 0
        },
        total: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false
        },
        paymentMethod: {
            type: DataTypes.ENUM('cash', 'card', 'transfer', 'check'),
            allowNull: false
        },
        paymentStatus: {
            type: DataTypes.ENUM('pending', 'paid', 'partial', 'cancelled'),
            defaultValue: 'pending'
        },
        notes: {
            type: DataTypes.TEXT
        },
        status: {
            type: DataTypes.ENUM('draft', 'completed', 'cancelled'),
            defaultValue: 'draft'
        }
    });

    return Sale;
};
