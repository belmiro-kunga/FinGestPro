const { contextBridge, ipcRenderer } = require('electron');

// Configuração do Content Security Policy
const meta = document.createElement('meta');
meta.httpEquiv = 'Content-Security-Policy';
meta.content = `
  default-src 'self' 'unsafe-inline' 'unsafe-eval' data:;
  script-src 'self' 'unsafe-inline' 'unsafe-eval';
  style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
  style-src-elem 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
  img-src 'self' data: https:;
  font-src 'self' data: https://cdnjs.cloudflare.com;
  connect-src 'self' http://localhost:3000;
  frame-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
`;
document.head.appendChild(meta);

// Expondo APIs seguras para o renderer
contextBridge.exposeInMainWorld('electron', {
    // Exemplo de API segura
    sendMessage: (channel, data) => {
        ipcRenderer.send(channel, data);
    },
    receiveMessage: (channel, func) => {
        ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
});
