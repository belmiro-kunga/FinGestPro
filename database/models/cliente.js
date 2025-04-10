const { runQuery, getOne, getAll } = require('../connection');

class Cliente {
    static async criar(cliente) {
        const sql = `
            INSERT INTO clientes (nome, contacto, sincronizado)
            VALUES (?, ?, 0)
        `;
        return await runQuery(sql, [cliente.nome, cliente.contacto]);
    }

    static async atualizar(id, cliente) {
        const sql = `
            UPDATE clientes 
            SET nome = ?, 
                contacto = ?,
                sincronizado = 0
            WHERE id = ?
        `;
        return await runQuery(sql, [cliente.nome, cliente.contacto, id]);
    }

    static async buscarPorId(id) {
        return await getOne('SELECT * FROM clientes WHERE id = ?', [id]);
    }

    static async listarTodos() {
        return await getAll('SELECT * FROM clientes');
    }

    static async listarNaoSincronizados() {
        return await getAll('SELECT * FROM clientes WHERE sincronizado = 0');
    }

    static async marcarComoSincronizado(id) {
        const sql = `
            UPDATE clientes 
            SET sincronizado = 1 
            WHERE id = ?
        `;
        return await runQuery(sql, [id]);
    }
}

module.exports = Cliente; 