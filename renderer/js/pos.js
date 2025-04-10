document.addEventListener('DOMContentLoaded', () => {
    // Initialize POS
    initializePOS();
    
    // Set up event listeners
    setupEventListeners();
});

// Global variables
let cart = [];
let products = [];
let customers = [];
let selectedCustomer = null;

async function initializePOS() {
    try {
        // Load products
        await loadProducts();
        
        // Load customers
        await loadCustomers();
        
        // Update UI
        updateProductsGrid();
        updateCustomerSelect();
    } catch (error) {
        console.error('Error initializing POS:', error);
        showNotification('Erro ao inicializar o PDV', 'error');
    }
}

function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterProducts(e.target.value);
        });
    }
    
    // Category filter
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', (e) => {
            filterProductsByCategory(e.target.value);
        });
    }
    
    // Customer select
    const customerSelect = document.getElementById('customerSelect');
    if (customerSelect) {
        customerSelect.addEventListener('change', (e) => {
            const customerId = e.target.value;
            selectedCustomer = customers.find(c => c.id === parseInt(customerId)) || null;
            updateCartSummary();
        });
    }
    
    // Payment method
    const paymentMethod = document.getElementById('paymentMethod');
    if (paymentMethod) {
        paymentMethod.addEventListener('change', (e) => {
            // Update payment method in cart summary
            updateCartSummary();
        });
    }
    
    // Checkout button
    const checkoutBtn = document.getElementById('checkoutBtn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', processCheckout);
    }
}

async function loadProducts() {
    try {
        // In a real app, this would fetch products from the main process
        // For now, we'll use mock data
        products = await window.api.getProducts();
        
        // If no products were returned, use mock data
        if (!products || products.length === 0) {
            products = [
                { id: 1, nome: 'Notebook', preco: 3500.00, estoque: 10 },
                { id: 2, nome: 'Smartphone', preco: 1200.00, estoque: 15 },
                { id: 3, nome: 'Tablet', preco: 1800.00, estoque: 8 },
                { id: 4, nome: 'Monitor', preco: 800.00, estoque: 12 },
                { id: 5, nome: 'Teclado', preco: 150.00, estoque: 20 },
                { id: 6, nome: 'Mouse', preco: 80.00, estoque: 25 },
                { id: 7, nome: 'Headphone', preco: 200.00, estoque: 18 },
                { id: 8, nome: 'Webcam', preco: 120.00, estoque: 10 }
            ];
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Erro ao carregar produtos', 'error');
    }
}

async function loadCustomers() {
    try {
        // In a real app, this would fetch customers from the main process
        // For now, we'll use mock data
        customers = await window.api.getCustomers();
        
        // If no customers were returned, use mock data
        if (!customers || customers.length === 0) {
            customers = [
                { id: 1, nome: 'Cliente Padrão', contacto: 'N/A' },
                { id: 2, nome: 'João Silva', contacto: '(11) 98765-4321' },
                { id: 3, nome: 'Maria Oliveira', contacto: '(11) 91234-5678' }
            ];
        }
    } catch (error) {
        console.error('Error loading customers:', error);
        showNotification('Erro ao carregar clientes', 'error');
    }
}

function updateProductsGrid() {
    const productsGrid = document.getElementById('productsGrid');
    if (!productsGrid) return;
    
    productsGrid.innerHTML = '';
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.dataset.id = product.id;
        
        productCard.innerHTML = `
            <div class="product-name">${product.nome}</div>
            <div class="product-price">${formatCurrency(product.preco)}</div>
            <div class="product-stock">Estoque: ${product.estoque}</div>
        `;
        
        productCard.addEventListener('click', () => {
            addToCart(product);
        });
        
        productsGrid.appendChild(productCard);
    });
}

function updateCustomerSelect() {
    const customerSelect = document.getElementById('customerSelect');
    if (!customerSelect) return;
    
    customerSelect.innerHTML = '<option value="">Selecione um cliente</option>';
    
    customers.forEach(customer => {
        const option = document.createElement('option');
        option.value = customer.id;
        option.textContent = customer.nome;
        customerSelect.appendChild(option);
    });
}

function filterProducts(searchTerm) {
    const filteredProducts = products.filter(product => 
        product.nome.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    updateProductsGridWithFiltered(filteredProducts);
}

function filterProductsByCategory(categoryId) {
    if (!categoryId) {
        updateProductsGrid();
        return;
    }
    
    // In a real app, this would filter by category
    // For now, we'll just show all products
    updateProductsGrid();
}

function updateProductsGridWithFiltered(filteredProducts) {
    const productsGrid = document.getElementById('productsGrid');
    if (!productsGrid) return;
    
    productsGrid.innerHTML = '';
    
    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.dataset.id = product.id;
        
        productCard.innerHTML = `
            <div class="product-name">${product.nome}</div>
            <div class="product-price">${formatCurrency(product.preco)}</div>
            <div class="product-stock">Estoque: ${product.estoque}</div>
        `;
        
        productCard.addEventListener('click', () => {
            addToCart(product);
        });
        
        productsGrid.appendChild(productCard);
    });
}

function addToCart(product) {
    // Check if product is already in cart
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
        // Increment quantity
        existingItem.quantity++;
    } else {
        // Add new item
        cart.push({
            id: product.id,
            nome: product.nome,
            preco: product.preco,
            quantity: 1
        });
    }
    
    // Update cart UI
    updateCartItems();
    updateCartSummary();
}

function updateCartItems() {
    const cartItems = document.getElementById('cartItems');
    if (!cartItems) return;
    
    cartItems.innerHTML = '';
    
    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        
        cartItem.innerHTML = `
            <div class="cart-item-name">${item.nome}</div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" data-id="${item.id}" data-action="decrease">-</button>
                <span>${item.quantity}</span>
                <button class="quantity-btn" data-id="${item.id}" data-action="increase">+</button>
            </div>
            <div class="cart-item-price">${formatCurrency(item.preco * item.quantity)}</div>
            <button class="remove-item-btn" data-id="${item.id}">×</button>
        `;
        
        cartItems.appendChild(cartItem);
    });
    
    // Add event listeners to quantity buttons
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(e.target.dataset.id);
            const action = e.target.dataset.action;
            
            if (action === 'increase') {
                increaseQuantity(id);
            } else if (action === 'decrease') {
                decreaseQuantity(id);
            }
        });
    });
    
    // Add event listeners to remove buttons
    const removeBtns = document.querySelectorAll('.remove-item-btn');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(e.target.dataset.id);
            removeFromCart(id);
        });
    });
}

function updateCartSummary() {
    const subtotalElement = document.getElementById('cartSubtotal');
    const totalElement = document.getElementById('cartTotal');
    
    if (!subtotalElement || !totalElement) return;
    
    // Calculate subtotal
    const subtotal = cart.reduce((total, item) => total + (item.preco * item.quantity), 0);
    
    // Update subtotal
    subtotalElement.textContent = formatCurrency(subtotal);
    
    // Update total (in a real app, this might include tax, discounts, etc.)
    totalElement.textContent = formatCurrency(subtotal);
}

function increaseQuantity(productId) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity++;
        updateCartItems();
        updateCartSummary();
    }
}

function decreaseQuantity(productId) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        if (item.quantity > 1) {
            item.quantity--;
        } else {
            removeFromCart(productId);
        }
        updateCartItems();
        updateCartSummary();
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartItems();
    updateCartSummary();
}

async function processCheckout() {
    if (cart.length === 0) {
        showNotification('Adicione produtos ao carrinho', 'warning');
        return;
    }
    
    try {
        // Get payment method
        const paymentMethod = document.getElementById('paymentMethod');
        const paymentType = paymentMethod ? paymentMethod.value : 'cash';
        
        // Calculate total
        const total = cart.reduce((sum, item) => sum + (item.preco * item.quantity), 0);
        
        // Create sale object
        const sale = {
            items: cart,
            customer: selectedCustomer,
            total: total,
            paymentMethod: paymentType,
            date: new Date()
        };
        
        // In a real app, this would save the sale to the database
        const result = await window.api.saveSale(sale);
        
        if (result.success) {
            // Clear cart
            cart = [];
            updateCartItems();
            updateCartSummary();
            
            // Show success message
            showNotification('Venda realizada com sucesso!', 'success');
            
            // Open receipt modal
            openReceiptModal(sale, result.saleId);
        } else {
            showNotification('Erro ao processar venda', 'error');
        }
    } catch (error) {
        console.error('Error processing checkout:', error);
        showNotification('Erro ao processar venda', 'error');
    }
}

function openReceiptModal(sale, saleId) {
    // In a real app, this would open a modal with the receipt
    console.log('Receipt for sale #' + saleId, sale);
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