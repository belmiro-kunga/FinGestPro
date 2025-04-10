const { ipcRenderer } = require('electron');
const { Product, Customer, Sale } = require('../../models');
const { Op } = require('sequelize');

// Estado da venda atual
let currentSale = {
    items: [],
    customer: null,
    subtotal: 0,
    discount: 0,
    tax: 0,
    total: 0
};

// Elementos DOM
const productsGrid = document.getElementById('productsGrid');
const productSearch = document.getElementById('productSearch');
const saleItemsList = document.getElementById('saleItemsList');
const customerName = document.getElementById('customerName');
const subtotalElement = document.getElementById('subtotal');
const discountElement = document.getElementById('discount');
const taxElement = document.getElementById('tax');
const totalElement = document.getElementById('total');
const paymentModal = document.getElementById('paymentModal');
const amountReceived = document.getElementById('amountReceived');
const changeElement = document.getElementById('change');

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    await loadProducts();
    setupEventListeners();
    initializeSale();
});

// Carregar produtos
async function loadProducts(searchTerm = '') {
    try {
        const where = searchTerm ? {
            [Op.or]: [
                { name: { [Op.like]: `%${searchTerm}%` } },
                { code: { [Op.like]: `%${searchTerm}%` } },
                { barcode: { [Op.like]: `%${searchTerm}%` } }
            ]
        } : {};

        const products = await Product.findAll({
            where,
            order: [['name', 'ASC']]
        });

        renderProducts(products);
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        alert('Erro ao carregar produtos. Tente novamente.');
    }
}

// Renderizar produtos na grade
function renderProducts(products) {
    productsGrid.innerHTML = products.map(product => `
        <div class="product-card" onclick="addProductToSale(${product.id})">
            <img src="../../../assets/images/products/${product.id}.jpg" 
                 onerror="this.src='../../../assets/images/no-image.png'"
                 alt="${product.name}">
            <div class="product-name">${product.name}</div>
            <div class="product-price">${formatCurrency(product.price)}</div>
        </div>
    `).join('');
}

// Adicionar produto à venda
async function addProductToSale(productId) {
    try {
        const product = await Product.findByPk(productId);
        if (!product) return;

        const existingItem = currentSale.items.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity++;
            existingItem.total = existingItem.quantity * existingItem.price;
        } else {
            currentSale.items.push({
                productId: product.id,
                code: product.code,
                name: product.name,
                price: product.price,
                quantity: 1,
                total: product.price,
                taxRate: product.taxRate
            });
        }

        updateSaleDisplay();
    } catch (error) {
        console.error('Erro ao adicionar produto:', error);
    }
}

// Atualizar exibição da venda
function updateSaleDisplay() {
    // Atualizar lista de itens
    saleItemsList.innerHTML = currentSale.items.map((item, index) => `
        <tr>
            <td>${item.code}</td>
            <td>${item.name}</td>
            <td>
                <input type="number" value="${item.quantity}" 
                       onchange="updateItemQuantity(${index}, this.value)"
                       min="1" step="1">
            </td>
            <td>${formatCurrency(item.price)}</td>
            <td>
                <input type="number" value="0" 
                       onchange="updateItemDiscount(${index}, this.value)"
                       min="0" step="0.01">
            </td>
            <td>${formatCurrency(item.total)}</td>
            <td>
                <button onclick="removeItem(${index})" class="btn-icon">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');

    // Calcular totais
    calculateTotals();
}

// Calcular totais
function calculateTotals() {
    currentSale.subtotal = currentSale.items.reduce((sum, item) => sum + item.total, 0);
    currentSale.tax = currentSale.items.reduce((sum, item) => {
        return sum + (item.total * (item.taxRate / 100));
    }, 0);
    currentSale.total = currentSale.subtotal + currentSale.tax - currentSale.discount;

    // Atualizar display
    subtotalElement.textContent = formatCurrency(currentSale.subtotal);
    taxElement.textContent = formatCurrency(currentSale.tax);
    discountElement.textContent = formatCurrency(currentSale.discount);
    totalElement.textContent = formatCurrency(currentSale.total);
}

// Atualizar quantidade de item
function updateItemQuantity(index, quantity) {
    const item = currentSale.items[index];
    item.quantity = parseInt(quantity);
    item.total = item.quantity * item.price;
    updateSaleDisplay();
}

// Atualizar desconto de item
function updateItemDiscount(index, discount) {
    const item = currentSale.items[index];
    item.discount = parseFloat(discount);
    item.total = (item.quantity * item.price) - item.discount;
    updateSaleDisplay();
}

// Remover item
function removeItem(index) {
    currentSale.items.splice(index, 1);
    updateSaleDisplay();
}

// Configurar event listeners
function setupEventListeners() {
    // Pesquisa de produtos
    productSearch.addEventListener('input', debounce((e) => {
        loadProducts(e.target.value);
    }, 300));

    // Leitor de código de barras
    document.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter' && document.activeElement === productSearch) {
            const barcode = productSearch.value;
            const product = await Product.findOne({ where: { barcode } });
            if (product) {
                addProductToSale(product.id);
                productSearch.value = '';
            }
        }
    });

    // Botão de pagamento
    document.getElementById('checkoutBtn').addEventListener('click', () => {
        if (currentSale.items.length === 0) {
            alert('Adicione itens à venda antes de finalizar.');
            return;
        }
        openPaymentModal();
    });

    // Cálculo de troco
    amountReceived.addEventListener('input', () => {
        const received = parseFloat(amountReceived.value) || 0;
        const change = received - currentSale.total;
        changeElement.value = formatCurrency(change >= 0 ? change : 0);
    });

    // Métodos de pagamento
    document.querySelectorAll('.payment-method').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelector('.payment-method.active').classList.remove('active');
            button.classList.add('active');
        });
    });

    // Confirmar pagamento
    document.getElementById('confirmPaymentBtn').addEventListener('click', finalizeSale);
}

// Abrir modal de pagamento
function openPaymentModal() {
    document.getElementById('paymentTotal').textContent = formatCurrency(currentSale.total);
    paymentModal.classList.add('active');
    amountReceived.value = currentSale.total;
    amountReceived.focus();
}

// Fechar modal de pagamento
function closePaymentModal() {
    paymentModal.classList.remove('active');
}

// Finalizar venda
async function finalizeSale() {
    try {
        const paymentMethod = document.querySelector('.payment-method.active').dataset.method;
        const received = parseFloat(amountReceived.value);

        if (received < currentSale.total) {
            alert('Valor recebido é menor que o total da venda.');
            return;
        }

        const sale = await Sale.create({
            customerId: currentSale.customer?.id,
            subtotal: currentSale.subtotal,
            tax: currentSale.tax,
            discount: currentSale.discount,
            total: currentSale.total,
            paymentMethod,
            paymentStatus: 'paid',
            status: 'completed'
        });

        // TODO: Criar itens da venda e atualizar estoque

        closePaymentModal();
        initializeSale();
        alert('Venda finalizada com sucesso!');
    } catch (error) {
        console.error('Erro ao finalizar venda:', error);
        alert('Erro ao finalizar venda. Tente novamente.');
    }
}

// Inicializar nova venda
function initializeSale() {
    currentSale = {
        items: [],
        customer: null,
        subtotal: 0,
        discount: 0,
        tax: 0,
        total: 0
    };
    updateSaleDisplay();
}

// Funções auxiliares
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-AO', {
        style: 'currency',
        currency: 'AOA'
    }).format(value);
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
