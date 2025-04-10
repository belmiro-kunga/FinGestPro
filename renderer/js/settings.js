document.addEventListener('DOMContentLoaded', () => {
    // Load settings
    loadSettings();
    
    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Settings form
    const settingsForm = document.getElementById('settingsForm');
    if (settingsForm) {
        settingsForm.addEventListener('submit', handleSettingsSubmit);
    }
    
    // Test database connection button
    const testDbBtn = document.getElementById('testDbConnection');
    if (testDbBtn) {
        testDbBtn.addEventListener('click', testDatabaseConnection);
    }
    
    // Sync now button
    const syncNowBtn = document.getElementById('syncNow');
    if (syncNowBtn) {
        syncNowBtn.addEventListener('click', syncData);
    }
}

async function loadSettings() {
    try {
        const settings = await window.api.getSettings();
        populateSettingsForm(settings);
    } catch (error) {
        console.error('Error loading settings:', error);
        showNotification('Erro ao carregar configurações', 'error');
    }
}

function populateSettingsForm(settings) {
    const form = document.getElementById('settingsForm');
    if (!form) return;
    
    // Database settings
    form.elements.dbHost.value = settings.database.host || '';
    form.elements.dbPort.value = settings.database.port || '';
    form.elements.dbName.value = settings.database.name || '';
    form.elements.dbUser.value = settings.database.user || '';
    
    // Company info
    form.elements.companyName.value = settings.company.name || '';
    form.elements.companyAddress.value = settings.company.address || '';
    form.elements.companyPhone.value = settings.company.phone || '';
    form.elements.companyEmail.value = settings.company.email || '';
    
    // Receipt settings
    form.elements.receiptHeader.value = settings.receipt.header || '';
    form.elements.receiptFooter.value = settings.receipt.footer || '';
    
    // Sync settings
    form.elements.syncInterval.value = settings.sync.interval || '5';
    form.elements.syncEnabled.checked = settings.sync.enabled || false;
}

async function handleSettingsSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    
    const settings = {
        database: {
            host: form.elements.dbHost.value,
            port: form.elements.dbPort.value,
            name: form.elements.dbName.value,
            user: form.elements.dbUser.value,
            password: form.elements.dbPassword.value
        },
        company: {
            name: form.elements.companyName.value,
            address: form.elements.companyAddress.value,
            phone: form.elements.companyPhone.value,
            email: form.elements.companyEmail.value
        },
        receipt: {
            header: form.elements.receiptHeader.value,
            footer: form.elements.receiptFooter.value
        },
        sync: {
            interval: form.elements.syncInterval.value,
            enabled: form.elements.syncEnabled.checked
        }
    };
    
    try {
        await window.api.saveSettings(settings);
        showNotification('Configurações salvas com sucesso!', 'success');
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('Erro ao salvar configurações', 'error');
    }
}

async function testDatabaseConnection() {
    const form = document.getElementById('settingsForm');
    if (!form) return;
    
    const dbSettings = {
        host: form.elements.dbHost.value,
        port: form.elements.dbPort.value,
        name: form.elements.dbName.value,
        user: form.elements.dbUser.value,
        password: form.elements.dbPassword.value
    };
    
    try {
        const result = await window.api.testDatabaseConnection(dbSettings);
        
        if (result.success) {
            showNotification('Conexão com o banco de dados estabelecida com sucesso!', 'success');
        } else {
            showNotification('Erro ao conectar ao banco de dados: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error testing database connection:', error);
        showNotification('Erro ao testar conexão com o banco de dados', 'error');
    }
}

async function syncData() {
    try {
        const result = await window.api.syncData();
        
        if (result.success) {
            showNotification('Dados sincronizados com sucesso!', 'success');
            updateSyncStatus(result);
        } else {
            showNotification('Erro na sincronização: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error syncing data:', error);
        showNotification('Erro ao sincronizar dados', 'error');
    }
}

function updateSyncStatus(status) {
    const lastSyncTime = document.getElementById('lastSyncTime');
    const pendingSyncs = document.getElementById('pendingSyncs');
    
    if (lastSyncTime) {
        lastSyncTime.textContent = formatDate(status.lastSync);
    }
    
    if (pendingSyncs) {
        pendingSyncs.textContent = status.pending;
    }
}

function formatDate(date) {
    return new Date(date).toLocaleString('pt-BR');
}

function showNotification(message, type = 'info') {
    // In a real app, this would show a notification
    console.log(`${type.toUpperCase()}: ${message}`);
} 