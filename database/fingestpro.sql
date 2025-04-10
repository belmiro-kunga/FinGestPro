CREATE DATABASE IF NOT EXISTS FinGestPro;
USE FinGestPro;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a default user (password: admin123)
INSERT INTO usuarios (username, password, nome_completo, email) 
VALUES ('admin', '$2b$10$YourHashedPasswordHere', 'Administrador', 'admin@fingestpro.com');
