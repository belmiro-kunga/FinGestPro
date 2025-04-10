const { app, BrowserWindow } = require('electron');
const path = require('path');
const express = require('express');
const compression = require('compression');
const cors = require('cors');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

// Create Express server for serving static files
const server = express();
server.use(compression());
server.use(cors());

// Serve static files from src directory
server.use(express.static(path.join(__dirname), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    }
  }
}));

// Serve node_modules for Font Awesome
server.use('/node_modules', express.static(path.join(__dirname, '..', 'node_modules')));

// Start the server
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Static file server running on port ${PORT}`);
});

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: true
    },
    autoHideMenuBar: true
  });

  // Set CSP headers
  mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self' http://localhost:3000;",
          "style-src 'self' 'unsafe-inline' http://localhost:3000 https://cdnjs.cloudflare.com;",
          "font-src 'self' https://cdnjs.cloudflare.com;",
          "img-src 'self' data: http://localhost:3000;"
        ].join(' ')
      }
    });
  });

  // Wait for server to be ready
  const waitForServer = () => {
    return new Promise((resolve) => {
      const testConnection = () => {
        const req = require('http').get('http://localhost:3000', (res) => {
          if (res.statusCode === 200) {
            resolve();
          } else {
            setTimeout(testConnection, 100);
          }
        });
        req.on('error', () => setTimeout(testConnection, 100));
      };
      testConnection();
    });
  };

  // Load the index.html file after server is ready
  waitForServer().then(() => {
    mainWindow.loadURL('http://localhost:3000/index.html');
  });

  // Open DevTools (for development)
  mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();

  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.
