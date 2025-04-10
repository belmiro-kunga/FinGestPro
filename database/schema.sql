-- Tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER NOT NULL DEFAULT 0,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sincronizado INTEGER DEFAULT 0
);

-- Tabela de vendas
CREATE TABLE IF NOT EXISTS vendas (
    id_local INTEGER PRIMARY KEY AUTOINCREMENT,
    id_servidor INTEGER,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    sincronizado INTEGER DEFAULT 0,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    sincronizado INTEGER DEFAULT 0
);

-- Tabela de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contacto TEXT,
    sincronizado INTEGER DEFAULT 0
);

-- Índices para otimização
CREATE INDEX IF NOT EXISTS idx_produtos_sincronizado ON produtos(sincronizado);
CREATE INDEX IF NOT EXISTS idx_vendas_sincronizado ON vendas(sincronizado);
CREATE INDEX IF NOT EXISTS idx_usuarios_sincronizado ON usuarios(sincronizado);
CREATE INDEX IF NOT EXISTS idx_clientes_sincronizado ON clientes(sincronizado); 