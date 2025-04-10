document.addEventListener('DOMContentLoaded', () => {
    // Load sales on page load
    loadSales();
    
    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('saleSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterSales(e.target.value);
        });
    }
    
    // Date filter
    const dateFilter = document.getElementById('dateFilter');
    if (dateFilter) {
        dateFilter.addEventListener('change', (e) => {
            filterSalesByDate(e.target.value);
        });
    }
}

async function loadSales() {
    try {
        const sales = await window.api.getSales();
        updateSalesTable(sales);
    } catch (error) {
        console.error('Error loading sales:', error);
        showNotification('Erro ao carregar vendas', 'error');
    }
}

function updateSalesTable(sales) {
    const tableBody = document.querySelector('#salesTable tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    sales.forEach(sale => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${sale.id_local}</td>
            <td>${formatDate(sale.data)}</td>
            <td>${formatCurrency(sale.total)}</td>
            <td>${sale.sincronizado ? 'Sim' : 'Não'}</td>
            <td>
                <button class="view-btn" data-id="${sale.id_local}">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="print-btn" data-id="${sale.id_local}">
                    <i class="fas fa-print"></i>
                </button>
            </td>
        `;
        
        // Add event listeners to buttons
        const viewBtn = row.querySelector('.view-btn');
        const printBtn = row.querySelector('.print-btn');
        
        viewBtn.addEventListener('click', () => {
            viewSaleDetails(sale.id_local);
        });
        
        printBtn.addEventListener('click', () => {
            printReceipt(sale.id_local);
        });
        
        tableBody.appendChild(row);
    });
}

function filterSales(searchTerm) {
    const rows = document.querySelectorAll('#salesTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const match = text.includes(searchTerm.toLowerCase());
        row.style.display = match ? '' : 'none';
    });
}

function filterSalesByDate(date) {
    if (!date) {
        loadSales();
        return;
    }
    
    const rows = document.querySelectorAll('#salesTable tbody tr');
    const selectedDate = new Date(date).toLocaleDateString();
    
    rows.forEach(row => {
        const saleDate = row.children[1].textContent;
        row.style.display = saleDate === selectedDate ? '' : 'none';
    });
}

async function viewSaleDetails(saleId) {
    try {
        const sale = await window.api.getSaleDetails(saleId);
        openSaleDetailsModal(sale);
    } catch (error) {
        console.error('Error loading sale details:', error);
        showNotification('Erro ao carregar detalhes da venda', 'error');
    }
}

function openSaleDetailsModal(sale) {
    const modal = document.getElementById('saleDetailsModal');
    const modalContent = document.getElementById('saleDetailsContent');
    
    if (!modal || !modalContent) return;
    
    modalContent.innerHTML = `
        <h3>Venda #${sale.id_local}</h3>
        <p><strong>Data:</strong> ${formatDate(sale.data)}</p>
        <p><strong>Cliente:</strong> ${sale.customer ? sale.customer.nome : 'N/A'}</p>
        <p><strong>Total:</strong> ${formatCurrency(sale.total)}</p>
        
        <h4>Itens</h4>
        <table class="items-table">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Preço Unit.</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                ${sale.items.map(item => `
                    <tr>
                        <td>${item.nome}</td>
                        <td>${item.quantity}</td>
                        <td>${formatCurrency(item.preco)}</td>
                        <td>${formatCurrency(item.preco * item.quantity)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    modal.classList.add('active');
}

async function printReceipt(saleId) {
    try {
        await window.api.printReceipt(saleId);
        showNotification('Recibo enviado para impressão', 'success');
    } catch (error) {
        console.error('Error printing receipt:', error);
        showNotification('Erro ao imprimir recibo', 'error');
    }
}

function formatDate(date) {
    return new Date(date).toLocaleString('pt-BR');
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function showNotification(message, type = 'info') {
    // In a real app, this would show a notification
    console.log(`${type.toUpperCase()}: ${message}`);
} 