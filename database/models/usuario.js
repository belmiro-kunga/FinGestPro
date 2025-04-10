const { runQuery, getOne, getAll } = require('../connection');

class Usuario {
    static async criar(usuario) {
        const sql = `
            INSERT INTO usuarios (nome, email, senha, sincronizado)
            VALUES (?, ?, ?, 0)
        `;
        return await runQuery(sql, [usuario.nome, usuario.email, usuario.senha]);
    }

    static async atualizar(id, usuario) {
        const sql = `
            UPDATE usuarios 
            SET nome = ?, 
                email = ?, 
                senha = ?,
                sincronizado = 0
            WHERE id = ?
        `;
        return await runQuery(sql, [usuario.nome, usuario.email, usuario.senha, id]);
    }

    static async buscarPorId(id) {
        return await getOne('SELECT * FROM usuarios WHERE id = ?', [id]);
    }

    static async buscarPorEmail(email) {
        return await getOne('SELECT * FROM usuarios WHERE email = ?', [email]);
    }

    static async listarTodos() {
        return await getAll('SELECT * FROM usuarios');
    }

    static async listarNaoSincronizados() {
        return await getAll('SELECT * FROM usuarios WHERE sincronizado = 0');
    }

    static async marcarComoSincronizado(id) {
        const sql = `
            UPDATE usuarios 
            SET sincronizado = 1 
            WHERE id = ?
        `;
        return await runQuery(sql, [id]);
    }
}

module.exports = Usuario; 