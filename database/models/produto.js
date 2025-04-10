const { runQuery, getOne, getAll } = require('../connection');

class Produto {
    static async criar(produto) {
        const sql = `
            INSERT INTO produtos (nome, preco, estoque, sincronizado)
            VALUES (?, ?, ?, 0)
        `;
        return await runQuery(sql, [produto.nome, produto.preco, produto.estoque]);
    }

    static async atualizar(id, produto) {
        const sql = `
            UPDATE produtos 
            SET nome = ?, 
                preco = ?, 
                estoque = ?,
                atualizado_em = CURRENT_TIMESTAMP,
                sincronizado = 0
            WHERE id = ?
        `;
        return await runQuery(sql, [produto.nome, produto.preco, produto.estoque, id]);
    }

    static async buscarPorId(id) {
        return await getOne('SELECT * FROM produtos WHERE id = ?', [id]);
    }

    static async listarTodos() {
        return await getAll('SELECT * FROM produtos');
    }

    static async listarNaoSincronizados() {
        return await getAll('SELECT * FROM produtos WHERE sincronizado = 0');
    }

    static async marcarComoSincronizado(id) {
        const sql = `
            UPDATE produtos 
            SET sincronizado = 1 
            WHERE id = ?
        `;
        return await runQuery(sql, [id]);
    }
}

module.exports = Produto; 