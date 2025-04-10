const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Product = sequelize.define('Product', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        code: {
            type: DataTypes.STRING,
            allowNull: false,
            unique: true
        },
        barcode: {
            type: DataTypes.STRING,
            unique: true
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false
        },
        description: {
            type: DataTypes.TEXT
        },
        price: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false
        },
        cost: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false
        },
        stock: {
            type: DataTypes.DECIMAL(10, 2),
            defaultValue: 0
        },
        minStock: {
            type: DataTypes.DECIMAL(10, 2),
            defaultValue: 0
        },
        categoryId: {
            type: DataTypes.INTEGER,
            allowNull: false
        },
        unit: {
            type: DataTypes.STRING,
            allowNull: false,
            defaultValue: 'UN'
        },
        status: {
            type: DataTypes.ENUM('active', 'inactive'),
            defaultValue: 'active'
        },
        taxRate: {
            type: DataTypes.DECIMAL(5, 2),
            defaultValue: 0
        },
        lastPurchaseDate: {
            type: DataTypes.DATE
        },
        lastSaleDate: {
            type: DataTypes.DATE
        }
    });

    return Product;
};
