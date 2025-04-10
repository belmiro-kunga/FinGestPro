require('dotenv').config();
const express = require('express');
const compression = require('compression');
const cors = require('cors');
const path = require('path');
const { Sequelize } = require('sequelize');
const winston = require('winston');

// Configuração do logger
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple()
    }));
}

// Inicialização do Express
const app = express();

// Middleware
app.use(compression());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configuração dos arquivos estáticos
const staticOptions = {
    setHeaders: (res, filePath) => {
        const ext = path.extname(filePath);
        const mimeTypes = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
            '.ttf': 'font/ttf',
            '.eot': 'application/vnd.ms-fontobject'
        };
        if (mimeTypes[ext]) {
            res.setHeader('Content-Type', mimeTypes[ext]);
        }
    }
};

// Servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'src'), staticOptions));

// Rota principal
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'index.html'));
});

// Configuração do banco de dados
const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PASS,
    {
        host: process.env.DB_HOST,
        port: process.env.DB_PORT,
        dialect: 'mysql',
        logging: (msg) => logger.debug(msg)
    }
);

// Teste de conexão com o banco de dados
sequelize.authenticate()
    .then(() => {
        logger.info('Conexão com o banco de dados estabelecida com sucesso.');
    })
    .catch(err => {
        logger.error('Erro ao conectar ao banco de dados:', err);
    });

// Middleware de erro
app.use((err, req, res, next) => {
    logger.error(err.stack);
    res.status(500).send('Algo deu errado!');
});

// Inicialização do servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    logger.info(`Servidor rodando na porta ${PORT}`);
    if (process.env.NODE_ENV === 'development') {
        logger.info(`Acesse http://localhost:${PORT}`);
    }
}); 