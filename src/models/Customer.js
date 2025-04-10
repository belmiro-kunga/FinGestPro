const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Customer = sequelize.define('Customer', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        code: {
            type: DataTypes.STRING,
            unique: true,
            allowNull: false
        },
        type: {
            type: DataTypes.ENUM('individual', 'company'),
            allowNull: false
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false
        },
        tradingName: { // Nome comercial para empresas
            type: DataTypes.STRING
        },
        nif: { // Número de Identificação Fiscal
            type: DataTypes.STRING,
            unique: true
        },
        bi: { // Bilhete de Identidade (para pessoas físicas)
            type: DataTypes.STRING,
            unique: true
        },
        address: {
            type: DataTypes.TEXT
        },
        city: {
            type: DataTypes.STRING
        },
        province: {
            type: DataTypes.STRING
        },
        phone: {
            type: DataTypes.STRING
        },
        email: {
            type: DataTypes.STRING,
            validate: {
                isEmail: true
            }
        },
        creditLimit: {
            type: DataTypes.DECIMAL(10, 2),
            defaultValue: 0
        },
        status: {
            type: DataTypes.ENUM('active', 'inactive', 'blocked'),
            defaultValue: 'active'
        },
        notes: {
            type: DataTypes.TEXT
        }
    });

    return Customer;
};
