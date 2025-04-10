const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { store, getWindowBounds, setWindowBounds } = require('./src/config/electron');
const { testConnections } = require('./src/config/database');
const { User, Transaction, Account } = require('./src/models');

let mainWindow;

async function createWindow() {
    const bounds = getWindowBounds();

    mainWindow = new BrowserWindow({
        ...bounds,
        minWidth: 1024,
        minHeight: 768,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        icon: path.join(__dirname, 'assets/images/icon.png')
    });

    // Test database connections
    await testConnections();

    // Load the login page
    mainWindow.loadFile('src/pages/login/login.html');

    // Save window size and position when closing
    mainWindow.on('close', () => {
        setWindowBounds(mainWindow.getBounds());
    });

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
}

// IPC Communication handlers
ipcMain.handle('auth:login', async (event, credentials) => {
    try {
        const user = await User.findOne({ where: { username: credentials.username } });
        if (user && await user.validatePassword(credentials.password)) {
            return { success: true, user: { id: user.id, name: user.name, username: user.username } };
        }
        return { success: false, error: 'Credenciais inválidas' };
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, error: 'Erro no servidor' };
    }
});

ipcMain.handle('data:sync', async () => {
    try {
        // TODO: Implement sync logic between SQLite and MySQL
        return { success: true };
    } catch (error) {
        console.error('Sync error:', error);
        return { success: false, error: error.message };
    }
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Handle any uncaught exceptions
process.on('uncaughtException', (error) => {
    console.error('Uncaught exception:', error);
});

process.on('unhandledRejection', (error) => {
    console.error('Unhandled rejection:', error);
});
