// Módulos do sistema
const modules = {
    pdv: {
        name: 'PDV',
        icon: 'fas fa-cash-register',
        permissions: ['sales', 'cashier'],
        routes: [
            { path: '/pdv', component: 'pdv/index.html' },
            { path: '/pdv/sales', component: 'pdv/sales.html' }
        ]
    },
    inventory: {
        name: 'Estoque',
        icon: 'fas fa-boxes',
        permissions: ['inventory.view', 'inventory.edit'],
        routes: [
            { path: '/inventory', component: 'inventory/index.html' },
            { path: '/inventory/products', component: 'inventory/products.html' },
            { path: '/inventory/categories', component: 'inventory/categories.html' }
        ]
    },
    hr: {
        name: 'Recursos Humanos',
        icon: 'fas fa-users',
        permissions: ['hr.view', 'hr.edit'],
        routes: [
            { path: '/hr', component: 'hr/index.html' },
            { path: '/hr/employees', component: 'hr/employees.html' },
            { path: '/hr/payroll', component: 'hr/payroll.html' }
        ]
    },
    accounting: {
        name: 'Contabilidade',
        icon: 'fas fa-calculator',
        permissions: ['accounting.view', 'accounting.edit'],
        routes: [
            { path: '/accounting', component: 'accounting/index.html' },
            { path: '/accounting/ledger', component: 'accounting/ledger.html' },
            { path: '/accounting/reports', component: 'accounting/reports.html' }
        ]
    },
    billing: {
        name: 'Faturamento',
        icon: 'fas fa-file-invoice',
        permissions: ['billing.view', 'billing.edit'],
        routes: [
            { path: '/billing', component: 'billing/index.html' },
            { path: '/billing/invoices', component: 'billing/invoices.html' },
            { path: '/billing/customers', component: 'billing/customers.html' }
        ]
    },
    management: {
        name: 'Gestão',
        icon: 'fas fa-chart-line',
        permissions: ['management.view', 'management.edit'],
        routes: [
            { path: '/management', component: 'management/index.html' },
            { path: '/management/dashboard', component: 'management/dashboard.html' },
            { path: '/management/reports', component: 'management/reports.html' }
        ]
    }
};

module.exports = modules;
