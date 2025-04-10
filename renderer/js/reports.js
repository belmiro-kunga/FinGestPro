document.addEventListener('DOMContentLoaded', () => {
    // Load initial report data
    loadReportData();
    
    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Date range inputs
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    
    if (startDate && endDate) {
        startDate.addEventListener('change', loadReportData);
        endDate.addEventListener('change', loadReportData);
    }
    
    // Report type selector
    const reportType = document.getElementById('reportType');
    if (reportType) {
        reportType.addEventListener('change', loadReportData);
    }
    
    // Export buttons
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    const exportExcelBtn = document.getElementById('exportExcelBtn');
    
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', exportToPdf);
    }
    
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', exportToExcel);
    }
}

async function loadReportData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const reportType = document.getElementById('reportType').value;
    
    if (!startDate || !endDate) return;
    
    try {
        const data = await window.api.getReportData({
            startDate,
            endDate,
            type: reportType
        });
        
        updateReportView(data, reportType);
    } catch (error) {
        console.error('Error loading report data:', error);
        showNotification('Erro ao carregar dados do relatório', 'error');
    }
}

function updateReportView(data, reportType) {
    const reportContent = document.getElementById('reportContent');
    if (!reportContent) return;
    
    switch (reportType) {
        case 'sales':
            showSalesReport(data);
            break;
        case 'products':
            showProductsReport(data);
            break;
        case 'customers':
            showCustomersReport(data);
            break;
        default:
            showSalesReport(data);
    }
    
    // Update summary cards
    updateSummaryCards(data.summary);
}

function showSalesReport(data) {
    const reportContent = document.getElementById('reportContent');
    if (!reportContent) return;
    
    reportContent.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Venda #</th>
                    <th>Cliente</th>
                    <th>Total</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                ${data.sales.map(sale => `
                    <tr>
                        <td>${formatDate(sale.data)}</td>
                        <td>${sale.id_local}</td>
                        <td>${sale.customer ? sale.customer.nome : 'N/A'}</td>
                        <td>${formatCurrency(sale.total)}</td>
                        <td>${sale.sincronizado ? 'Sincronizado' : 'Pendente'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function showProductsReport(data) {
    const reportContent = document.getElementById('reportContent');
    if (!reportContent) return;
    
    reportContent.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Quantidade Vendida</th>
                    <th>Total Vendas</th>
                    <th>Estoque Atual</th>
                </tr>
            </thead>
            <tbody>
                ${data.products.map(product => `
                    <tr>
                        <td>${product.nome}</td>
                        <td>${product.quantidadeVendida}</td>
                        <td>${formatCurrency(product.totalVendas)}</td>
                        <td>${product.estoque}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function showCustomersReport(data) {
    const reportContent = document.getElementById('reportContent');
    if (!reportContent) return;
    
    reportContent.innerHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Cliente</th>
                    <th>Total Compras</th>
                    <th>Valor Total</th>
                    <th>Última Compra</th>
                </tr>
            </thead>
            <tbody>
                ${data.customers.map(customer => `
                    <tr>
                        <td>${customer.nome}</td>
                        <td>${customer.totalCompras}</td>
                        <td>${formatCurrency(customer.valorTotal)}</td>
                        <td>${formatDate(customer.ultimaCompra)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function updateSummaryCards(summary) {
    // Update total sales
    const totalSales = document.getElementById('totalSales');
    if (totalSales) {
        totalSales.textContent = formatCurrency(summary.totalSales);
    }
    
    // Update average ticket
    const averageTicket = document.getElementById('averageTicket');
    if (averageTicket) {
        averageTicket.textContent = formatCurrency(summary.averageTicket);
    }
    
    // Update total items
    const totalItems = document.getElementById('totalItems');
    if (totalItems) {
        totalItems.textContent = summary.totalItems;
    }
    
    // Update total customers
    const totalCustomers = document.getElementById('totalCustomers');
    if (totalCustomers) {
        totalCustomers.textContent = summary.totalCustomers;
    }
}

async function exportToPdf() {
    try {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const reportType = document.getElementById('reportType').value;
        
        await window.api.exportReportToPdf({
            startDate,
            endDate,
            type: reportType
        });
        
        showNotification('Relatório exportado com sucesso!', 'success');
    } catch (error) {
        console.error('Error exporting to PDF:', error);
        showNotification('Erro ao exportar relatório', 'error');
    }
}

async function exportToExcel() {
    try {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const reportType = document.getElementById('reportType').value;
        
        await window.api.exportReportToExcel({
            startDate,
            endDate,
            type: reportType
        });
        
        showNotification('Relatório exportado com sucesso!', 'success');
    } catch (error) {
        console.error('Error exporting to Excel:', error);
        showNotification('Erro ao exportar relatório', 'error');
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