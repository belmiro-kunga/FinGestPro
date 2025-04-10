const { sqliteConfig, mysqlConfig } = require('../config/database');

// Import models
const UserModel = require('./User');
const ProductModel = require('./Product');
const EmployeeModel = require('./Employee');
const CustomerModel = require('./Customer');
const SaleModel = require('./Sale');

// Initialize models for SQLite (local)
const User = UserModel(sqliteConfig);
const Product = ProductModel(sqliteConfig);
const Employee = EmployeeModel(sqliteConfig);
const Customer = CustomerModel(sqliteConfig);
const Sale = SaleModel(sqliteConfig);

// Initialize models for MySQL (remote)
const RemoteUser = UserModel(mysqlConfig);
const RemoteProduct = ProductModel(mysqlConfig);
const RemoteEmployee = EmployeeModel(mysqlConfig);
const RemoteCustomer = CustomerModel(mysqlConfig);
const RemoteSale = SaleModel(mysqlConfig);

// Define relationships for SQLite models
User.hasMany(Sale);
Sale.belongsTo(User);

Employee.hasMany(Sale);
Sale.belongsTo(Employee);

Customer.hasMany(Sale);
Sale.belongsTo(Customer);

// Define relationships for MySQL models
RemoteUser.hasMany(RemoteSale);
RemoteSale.belongsTo(RemoteUser);

RemoteEmployee.hasMany(RemoteSale);
RemoteSale.belongsTo(RemoteEmployee);

RemoteCustomer.hasMany(RemoteSale);
RemoteSale.belongsTo(RemoteCustomer);

module.exports = {
    // Local models (SQLite)
    User,
    Product,
    Employee,
    Customer,
    Sale,
    
    // Remote models (MySQL)
    RemoteUser,
    RemoteProduct,
    RemoteEmployee,
    RemoteCustomer,
    RemoteSale,
    
    // Database configs
    sqliteConfig,
    mysqlConfig
};
