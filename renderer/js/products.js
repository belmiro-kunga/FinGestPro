document.addEventListener('DOMContentLoaded', () => {
    // Load products on page load
    loadProducts();
    
    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Add product button
    const addProductBtn = document.getElementById('addProductBtn');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', () => {
            openProductModal();
        });
    }
    
    // Product form
    const productForm = document.getElementById('productForm');
    if (productForm) {
        productForm.addEventListener('submit', handleProductSubmit);
    }
    
    // Search input
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterProducts(e.target.value);
        });
    }
}

async function loadProducts() {
    try {
        const products = await window.api.getProducts();
        updateProductsTable(products);
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Erro ao carregar produtos', 'error');
    }
}

function updateProductsTable(products) {
    const tableBody = document.querySelector('#productsTable tbody');
    if (!tableBody) return;
    
    tableBody.innerHTML = '';
    
    products.forEach(product => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.nome}</td>
            <td>${formatCurrency(product.preco)}</td>
            <td>${product.estoque}</td>
            <td>
                <button class="edit-btn" data-id="${product.id}">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="delete-btn" data-id="${product.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        // Add event listeners to buttons
        const editBtn = row.querySelector('.edit-btn');
        const deleteBtn = row.querySelector('.delete-btn');
        
        editBtn.addEventListener('click', () => {
            openProductModal(product);
        });
        
        deleteBtn.addEventListener('click', () => {
            if (confirm('Tem certeza que deseja excluir este produto?')) {
                deleteProduct(product.id);
            }
        });
        
        tableBody.appendChild(row);
    });
}

function filterProducts(searchTerm) {
    const rows = document.querySelectorAll('#productsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const match = text.includes(searchTerm.toLowerCase());
        row.style.display = match ? '' : 'none';
    });
}

function openProductModal(product = null) {
    const modal = document.getElementById('productModal');
    const form = document.getElementById('productForm');
    
    if (!modal || !form) return;
    
    // Reset form
    form.reset();
    
    // Set form values if editing
    if (product) {
        form.dataset.id = product.id;
        form.elements.nome.value = product.nome;
        form.elements.preco.value = product.preco;
        form.elements.estoque.value = product.estoque;
    } else {
        delete form.dataset.id;
    }
    
    // Show modal
    modal.classList.add('active');
}

async function handleProductSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const isEditing = form.dataset.id;
    
    const productData = {
        nome: form.elements.nome.value,
        preco: parseFloat(form.elements.preco.value),
        estoque: parseInt(form.elements.estoque.value)
    };
    
    try {
        if (isEditing) {
            // Update existing product
            await window.api.updateProduct(parseInt(form.dataset.id), productData);
            showNotification('Produto atualizado com sucesso!', 'success');
        } else {
            // Create new product
            await window.api.createProduct(productData);
            showNotification('Produto criado com sucesso!', 'success');
        }
        
        // Close modal and reload products
        closeProductModal();
        loadProducts();
    } catch (error) {
        console.error('Error saving product:', error);
        showNotification('Erro ao salvar produto', 'error');
    }
}

async function deleteProduct(id) {
    try {
        await window.api.deleteProduct(id);
        showNotification('Produto excluído com sucesso!', 'success');
        loadProducts();
    } catch (error) {
        console.error('Error deleting product:', error);
        showNotification('Erro ao excluir produto', 'error');
    }
}

function closeProductModal() {
    const modal = document.getElementById('productModal');
    if (modal) {
        modal.classList.remove('active');
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