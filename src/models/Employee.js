const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Employee = sequelize.define('Employee', {
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
        name: {
            type: DataTypes.STRING,
            allowNull: false
        },
        bi: { // Bilhete de Identidade (Angolan ID)
            type: DataTypes.STRING,
            unique: true
        },
        nif: { // Número de Identificação Fiscal (Tax ID)
            type: DataTypes.STRING,
            unique: true
        },
        birthDate: {
            type: DataTypes.DATE
        },
        gender: {
            type: DataTypes.ENUM('M', 'F')
        },
        address: {
            type: DataTypes.TEXT
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
        position: {
            type: DataTypes.STRING,
            allowNull: false
        },
        department: {
            type: DataTypes.STRING,
            allowNull: false
        },
        salary: {
            type: DataTypes.DECIMAL(10, 2),
            allowNull: false
        },
        hireDate: {
            type: DataTypes.DATE,
            allowNull: false
        },
        status: {
            type: DataTypes.ENUM('active', 'inactive', 'vacation', 'leave'),
            defaultValue: 'active'
        },
        bankName: {
            type: DataTypes.STRING
        },
        bankAccount: {
            type: DataTypes.STRING
        },
        bankIban: {
            type: DataTypes.STRING
        }
    });

    return Employee;
};
