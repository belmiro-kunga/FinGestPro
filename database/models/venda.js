const { runQuery, getOne, getAll } = require('../connection');

class Venda {
    static async criar(venda) {
        const sql = `
            INSERT INTO vendas (total, sincronizado)
            VALUES (?, 0)
        `;
        return await runQuery(sql, [venda.total]);
    }

    static async atualizar(id_local, venda) {
        const sql = `
            UPDATE vendas 
            SET total = ?,
                atualizado_em = CURRENT_TIMESTAMP,
                sincronizado = 0
            WHERE id_local = ?
        `;
        return await runQuery(sql, [venda.total, id_local]);
    }

    static async atualizarIdServidor(id_local, id_servidor) {
        const sql = `
            UPDATE vendas 
            SET id_servidor = ?,
                sincronizado = 1
            WHERE id_local = ?
        `;
        return await runQuery(sql, [id_servidor, id_local]);
    }

    static async buscarPorId(id_local) {
        return await getOne('SELECT * FROM vendas WHERE id_local = ?', [id_local]);
    }

    static async listarTodas() {
        return await getAll('SELECT * FROM vendas ORDER BY data DESC');
    }

    static async listarNaoSincronizadas() {
        return await getAll('SELECT * FROM vendas WHERE sincronizado = 0');
    }

    static async marcarComoSincronizada(id_local) {
        const sql = `
            UPDATE vendas 
            SET sincronizado = 1 
            WHERE id_local = ?
        `;
        return await runQuery(sql, [id_local]);
    }
}

module.exports = Venda; 