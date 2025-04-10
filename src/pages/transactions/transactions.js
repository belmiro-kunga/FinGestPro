const { ipcRenderer } = require('electron');
const { Transaction, Account } = require('../../models');
const { Op } = require('sequelize');

// Estado global
let currentPage = 1;
const pageSize = 10;
let totalPages = 1;
let filters = {
    search: '',
    type: 'all',
    accountId: 'all',
    startDate: null,
    endDate: null
};

// Elementos DOM
const transactionsTable = document.getElementById('transactionsTable');
const searchInput = document.getElementById('searchInput');
const typeFilter = document.getElementById('typeFilter');
const accountFilter = document.getElementById('accountFilter');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const modal = document.getElementById('transactionModal');
const transactionForm = document.getElementById('transactionForm');
const newTransactionBtn = document.getElementById('newTransactionBtn');

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    await loadAccounts();
    await loadTransactions();
    setupEventListeners();
});

// Carregar contas
async function loadAccounts() {
    try {
        const accounts = await Account.findAll();
        const accountOptions = accounts.map(account => 
            `<option value="${account.id}">${account.name}</option>`
        ).join('');
        
        // Adicionar opções ao filtro de contas
        accountFilter.innerHTML += accountOptions;
        
        // Adicionar opções ao formulário
        const accountSelect = transactionForm.querySelector('[name="accountId"]');
        accountSelect.innerHTML = accountOptions;
    } catch (error) {
        console.error('Erro ao carregar contas:', error);
    }
}

// Carregar transações
async function loadTransactions() {
    try {
        const where = buildWhereClause();
        
        const { count, rows } = await Transaction.findAndCountAll({
            where,
            include: [{ model: Account }],
            order: [['date', 'DESC']],
            limit: pageSize,
            offset: (currentPage - 1) * pageSize
        });

        totalPages = Math.ceil(count / pageSize);
        updatePagination();
        renderTransactions(rows);
    } catch (error) {
        console.error('Erro ao carregar transações:', error);
    }
}

// Construir cláusula WHERE para filtros
function buildWhereClause() {
    const where = {};

    if (filters.search) {
        where.description = { [Op.like]: `%${filters.search}%` };
    }

    if (filters.type !== 'all') {
        where.type = filters.type;
    }

    if (filters.accountId !== 'all') {
        where.accountId = filters.accountId;
    }

    if (filters.startDate && filters.endDate) {
        where.date = {
            [Op.between]: [filters.startDate, filters.endDate]
        };
    }

    return where;
}

// Renderizar transações na tabela
function renderTransactions(transactions) {
    transactionsTable.innerHTML = transactions.map(transaction => `
        <tr>
            <td>${formatDate(transaction.date)}</td>
            <td>${transaction.description}</td>
            <td>${transaction.category}</td>
            <td>${transaction.Account.name}</td>
            <td class="${transaction.type === 'INCOME' ? 'positive' : 'negative'}">
                R$ ${formatAmount(transaction.amount)}
            </td>
            <td>
                <button onclick="editTransaction(${transaction.id})" class="btn-icon">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="deleteTransaction(${transaction.id})" class="btn-icon">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Configurar event listeners
function setupEventListeners() {
    // Filtros
    searchInput.addEventListener('input', debounce(() => {
        filters.search = searchInput.value;
        currentPage = 1;
        loadTransactions();
    }, 300));

    typeFilter.addEventListener('change', () => {
        filters.type = typeFilter.value;
        currentPage = 1;
        loadTransactions();
    });

    accountFilter.addEventListener('change', () => {
        filters.accountId = accountFilter.value;
        currentPage = 1;
        loadTransactions();
    });

    startDateInput.addEventListener('change', () => {
        filters.startDate = startDateInput.value;
        currentPage = 1;
        loadTransactions();
    });

    endDateInput.addEventListener('change', () => {
        filters.endDate = endDateInput.value;
        currentPage = 1;
        loadTransactions();
    });

    // Modal
    newTransactionBtn.addEventListener('click', () => openModal());
    
    const closeBtn = modal.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => closeModal());

    transactionForm.addEventListener('submit', handleTransactionSubmit);
}

// Funções do Modal
function openModal(transaction = null) {
    if (transaction) {
        // Modo edição
        transactionForm.dataset.id = transaction.id;
        Object.keys(transaction).forEach(key => {
            const input = transactionForm.querySelector(`[name="${key}"]`);
            if (input) input.value = transaction[key];
        });
    } else {
        // Modo criação
        transactionForm.reset();
        delete transactionForm.dataset.id;
    }
    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');
    transactionForm.reset();
}

// Manipular envio do formulário
async function handleTransactionSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(transactionForm);
    const data = Object.fromEntries(formData.entries());
    
    try {
        if (transactionForm.dataset.id) {
            // Atualizar transação existente
            await Transaction.update(data, {
                where: { id: transactionForm.dataset.id }
            });
        } else {
            // Criar nova transação
            await Transaction.create(data);
        }
        
        closeModal();
        loadTransactions();
    } catch (error) {
        console.error('Erro ao salvar transação:', error);
        alert('Erro ao salvar transação. Tente novamente.');
    }
}

// Funções auxiliares
function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

function formatAmount(amount) {
    return Number(amount).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Funções de paginação
function updatePagination() {
    const pageInfo = document.getElementById('pageInfo');
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');

    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;

    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            loadTransactions();
        }
    };

    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadTransactions();
        }
    };
}

// Funções de edição e exclusão
async function editTransaction(id) {
    try {
        const transaction = await Transaction.findByPk(id);
        if (transaction) {
            openModal(transaction);
        }
    } catch (error) {
        console.error('Erro ao carregar transação:', error);
        alert('Erro ao carregar transação. Tente novamente.');
    }
}

async function deleteTransaction(id) {
    if (confirm('Tem certeza que deseja excluir esta transação?')) {
        try {
            await Transaction.destroy({ where: { id } });
            loadTransactions();
        } catch (error) {
            console.error('Erro ao excluir transação:', error);
            alert('Erro ao excluir transação. Tente novamente.');
        }
    }
}
