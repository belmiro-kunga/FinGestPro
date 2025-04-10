const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let serverProcess;

function startServer() {
    return new Promise((resolve, reject) => {
        serverProcess = spawn('node', ['server.js'], {
            stdio: 'inherit',
            shell: true,
            env: {
                ...process.env,
                NODE_ENV: process.env.NODE_ENV || 'development'
            }
        });

        serverProcess.on('error', (err) => {
            console.error('Erro ao iniciar o servidor:', err);
            reject(err);
        });

        // Aguarda o servidor iniciar
        setTimeout(resolve, 2000);
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'src/preload.js'),
            webSecurity: true,
            allowRunningInsecureContent: false
        }
    });

    // Carrega a aplicação do servidor local
    mainWindow.loadURL('http://localhost:3000');

    // Abre o DevTools em desenvolvimento
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(async () => {
    try {
        await startServer();
        createWindow();
    } catch (error) {
        console.error('Falha ao iniciar o aplicativo:', error);
        app.quit();
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        if (serverProcess) {
            serverProcess.kill();
        }
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

// Manipulador de eventos para tentativas de login
ipcMain.on('login-attempt', (event, credentials) => {
    const { username, password } = credentials;
    
    // Simulação de autenticação
    if (username === 'admin' && password === 'admin') {
        event.reply('login-response', { success: true });
    } else {
        event.reply('login-response', { 
            success: false, 
            message: 'Usuário ou senha inválidos' 
        });
    }
});
