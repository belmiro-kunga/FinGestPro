document.addEventListener('DOMContentLoaded', () => {
    // Load customers on page load
    loadCustomers();
    
    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Add customer button
    const addCustomerBtn = document.getElementById('addCustomerBtn');
    if (addCustomerBtn) {
        addCustomerBtn.addEventListener('click', () => {
            openCustomerModal();
        });
    }
    
    // Customer form
    const customerForm = document.getElementById('customerForm');
    if (customerForm) {
        customerForm.addEventListener('submit', handleCustomerSubmit);
    }
    
    // Search input
    const searchInput = document.getElementById('customerSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterCustomers(e.target.value);
        });
    }
}

async function loadCustomers() {
    try {
        const customers = await window.api.getCustomers();
        updateCustomersTable(customers);
    } catch (error) {
        console.error('Error loading customers:', error);
        showNotification('Erro ao carregar clientes', 'error');
    }
}

function updateCustomersTable(customers) {
    const tableBody = document.querySelector('#customersTable tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    customers.forEach(customer => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${customer.id}</td>
            <td>${customer.nome}</td>
            <td>${customer.contacto || '-'}</td>
            <td>
                <button class="edit-btn" data-id="${customer.id}">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="delete-btn" data-id="${customer.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        // Add event listeners to buttons
        const editBtn = row.querySelector('.edit-btn');
        const deleteBtn = row.querySelector('.delete-btn');
        
        editBtn.addEventListener('click', () => {
            openCustomerModal(customer);
        });
        
        deleteBtn.addEventListener('click', () => {
            if (confirm('Tem certeza que deseja excluir este cliente?')) {
                deleteCustomer(customer.id);
            }
        });
        
        tableBody.appendChild(row);
    });
}

function filterCustomers(searchTerm) {
    const rows = document.querySelectorAll('#customersTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const match = text.includes(searchTerm.toLowerCase());
        row.style.display = match ? '' : 'none';
    });
}

function openCustomerModal(customer = null) {
    const modal = document.getElementById('customerModal');
    const form = document.getElementById('customerForm');
    
    if (!modal || !form) return;
    
    // Reset form
    form.reset();
    
    // Set form values if editing
    if (customer) {
        form.dataset.id = customer.id;
        form.elements.nome.value = customer.nome;
        form.elements.contacto.value = customer.contacto || '';
    } else {
        delete form.dataset.id;
    }
    
    // Show modal
    modal.classList.add('active');
}

async function handleCustomerSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const isEditing = form.dataset.id;
    
    const customerData = {
        nome: form.elements.nome.value,
        contacto: form.elements.contacto.value
    };
    
    try {
        if (isEditing) {
            // Update existing customer
            await window.api.updateCustomer(parseInt(form.dataset.id), customerData);
            showNotification('Cliente atualizado com sucesso!', 'success');
        } else {
            // Create new customer
            await window.api.createCustomer(customerData);
            showNotification('Cliente criado com sucesso!', 'success');
        }
        
        // Close modal and reload customers
        closeCustomerModal();
        loadCustomers();
    } catch (error) {
        console.error('Error saving customer:', error);
        showNotification('Erro ao salvar cliente', 'error');
    }
}

async function deleteCustomer(id) {
    try {
        await window.api.deleteCustomer(id);
        showNotification('Cliente excluído com sucesso!', 'success');
        loadCustomers();
    } catch (error) {
        console.error('Error deleting customer:', error);
        showNotification('Erro ao excluir cliente', 'error');
    }
}

function closeCustomerModal() {
    const modal = document.getElementById('customerModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function showNotification(message, type = 'info') {
    // In a real app, this would show a notification
    console.log(`${type.toUpperCase()}: ${message}`);
} 