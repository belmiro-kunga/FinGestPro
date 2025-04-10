document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard data
    loadDashboardData();
    
    // Set up refresh button
    const refreshBtn = document.getElementById('refreshDashboard');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadDashboardData);
    }
});

async function loadDashboardData() {
    try {
        // In a real app, this would fetch data from the main process
        // For now, we'll use mock data
        const stats = await window.api.getDashboardStats();
        
        // Update stats cards
        updateStatsCards(stats);
        
        // Load charts
        loadCharts(stats);
        
        // Load recent activity
        loadRecentActivity();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showNotification('Erro ao carregar dados do dashboard', 'error');
    }
}

function updateStatsCards(stats) {
    // Update total sales
    const totalSalesElement = document.getElementById('totalSales');
    if (totalSalesElement && stats.totalSales !== undefined) {
        totalSalesElement.textContent = formatCurrency(stats.totalSales);
    }
    
    // Update total products
    const totalProductsElement = document.getElementById('totalProducts');
    if (totalProductsElement && stats.totalProducts !== undefined) {
        totalProductsElement.textContent = stats.totalProducts;
    }
    
    // Update total customers
    const totalCustomersElement = document.getElementById('totalCustomers');
    if (totalCustomersElement && stats.totalCustomers !== undefined) {
        totalCustomersElement.textContent = stats.totalCustomers;
    }
    
    // Update today's sales
    const todaySalesElement = document.getElementById('todaySales');
    if (todaySalesElement && stats.todaySales !== undefined) {
        todaySalesElement.textContent = formatCurrency(stats.todaySales);
    }
}

function loadCharts(stats) {
    // In a real app, this would use a charting library
    // For now, we'll just log that charts would be loaded
    console.log('Loading charts with data:', stats);
}

function loadRecentActivity() {
    try {
        // In a real app, this would fetch recent activity from the main process
        // For now, we'll use mock data
        const activities = [
            { type: 'sale', description: 'Venda #1234 - R$ 150,00', time: '5 minutos atrás' },
            { type: 'product', description: 'Produto "Notebook" atualizado', time: '15 minutos atrás' },
            { type: 'customer', description: 'Novo cliente cadastrado', time: '1 hora atrás' },
            { type: 'sale', description: 'Venda #1233 - R$ 75,50', time: '2 horas atrás' }
        ];
        
        const activityList = document.getElementById('activityList');
        if (activityList) {
            activityList.innerHTML = '';
            
            activities.forEach(activity => {
                const activityItem = document.createElement('div');
                activityItem.className = 'activity-item';
                
                let icon = '';
                switch (activity.type) {
                    case 'sale':
                        icon = '<i class="fas fa-shopping-cart"></i>';
                        break;
                    case 'product':
                        icon = '<i class="fas fa-box"></i>';
                        break;
                    case 'customer':
                        icon = '<i class="fas fa-user"></i>';
                        break;
                    default:
                        icon = '<i class="fas fa-info-circle"></i>';
                }
                
                activityItem.innerHTML = `
                    <div class="activity-icon">${icon}</div>
                    <div class="activity-details">
                        <div class="activity-description">${activity.description}</div>
                        <div class="activity-time">${activity.time}</div>
                    </div>
                `;
                
                activityList.appendChild(activityItem);
            });
        }
    } catch (error) {
        console.error('Error loading recent activity:', error);
    }
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