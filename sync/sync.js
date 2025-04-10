const { ipcRenderer } = require('electron');
const Store = require('electron-store');
const store = new Store();

class SyncManager {
  constructor() {
    this.syncInterval = null;
    this.isOnline = navigator.onLine;
    this.syncInProgress = false;
    this.syncServerUrl = store.get('syncServerUrl', 'https://sync.example.com');
    this.syncIntervalMinutes = store.get('syncIntervalMinutes', 5);
    
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // Listen for online/offline events
    window.addEventListener('online', () => this.handleOnlineStatus(true));
    window.addEventListener('offline', () => this.handleOnlineStatus(false));

    // Listen for sync settings changes
    document.getElementById('network-settings-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.updateSyncSettings();
    });
  }

  handleOnlineStatus(isOnline) {
    this.isOnline = isOnline;
    this.updateSyncStatus();
    
    if (isOnline) {
      this.sync();
    }
  }

  updateSyncStatus() {
    const statusElement = document.getElementById('sync-status');
    if (statusElement) {
      statusElement.textContent = this.isOnline ? 'Online' : 'Offline';
      statusElement.className = this.isOnline ? 'status-online' : 'status-offline';
    }
  }

  updateSyncSettings() {
    const intervalInput = document.getElementById('sync-interval');
    const serverInput = document.getElementById('sync-server');
    const autoSyncInput = document.getElementById('auto-sync');

    if (intervalInput && serverInput && autoSyncInput) {
      this.syncIntervalMinutes = parseInt(intervalInput.value) || 5;
      this.syncServerUrl = serverInput.value || 'https://sync.example.com';
      const autoSync = autoSyncInput.checked;

      store.set('syncIntervalMinutes', this.syncIntervalMinutes);
      store.set('syncServerUrl', this.syncServerUrl);
      store.set('autoSync', autoSync);

      this.updateSyncInterval();
    }
  }

  updateSyncInterval() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }

    if (store.get('autoSync', true)) {
      this.syncInterval = setInterval(() => {
        if (this.isOnline && !this.syncInProgress) {
          this.sync();
        }
      }, this.syncIntervalMinutes * 60 * 1000);
    }
  }

  async sync() {
    if (this.syncInProgress || !this.isOnline) {
      return;
    }

    this.syncInProgress = true;
    this.updateSyncStatus('Syncing...');

    try {
      // 1. Check server connection
      const serverAvailable = await this.checkServerConnection();
      if (!serverAvailable) {
        throw new Error('Server not available');
      }

      // 2. Send local records
      const unsyncedRecords = await this.getUnsyncedRecords();
      if (unsyncedRecords.length > 0) {
        await this.sendRecordsToServer(unsyncedRecords);
      }

      // 3. Get server updates
      const serverUpdates = await this.getServerUpdates();
      if (serverUpdates.length > 0) {
        await this.saveServerUpdates(serverUpdates);
      }

      this.updateLastSyncTime();
      this.logSyncSuccess();
    } catch (error) {
      this.logSyncError(error);
    } finally {
      this.syncInProgress = false;
      this.updateSyncStatus();
    }
  }

  async checkServerConnection() {
    try {
      const response = await fetch(`${this.syncServerUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Server connection check failed:', error);
      return false;
    }
  }

  async getUnsyncedRecords() {
    // Get records from local database where sincronizado = 0
    return await ipcRenderer.invoke('get-unsynced-records');
  }

  async sendRecordsToServer(records) {
    try {
      const response = await fetch(`${this.syncServerUrl}/sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ records }),
      });

      if (!response.ok) {
        throw new Error('Failed to send records to server');
      }

      const result = await response.json();
      
      // Mark records as synced in local database
      if (result.success) {
        await ipcRenderer.invoke('mark-records-synced', result.syncedIds);
      }

      return result;
    } catch (error) {
      console.error('Failed to send records:', error);
      throw error;
    }
  }

  async getServerUpdates() {
    try {
      const lastSync = store.get('lastSyncTime', 0);
      const response = await fetch(`${this.syncServerUrl}/updates?since=${lastSync}`);
      
      if (!response.ok) {
        throw new Error('Failed to get server updates');
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to get server updates:', error);
      throw error;
    }
  }

  async saveServerUpdates(updates) {
    return await ipcRenderer.invoke('save-server-updates', updates);
  }

  updateLastSyncTime() {
    store.set('lastSyncTime', Date.now());
    const lastSyncElement = document.getElementById('last-sync');
    if (lastSyncElement) {
      lastSyncElement.textContent = new Date().toLocaleString();
    }
  }

  logSyncSuccess() {
    this.addSyncLog('Sync completed successfully', 'success');
  }

  logSyncError(error) {
    this.addSyncLog(`Sync failed: ${error.message}`, 'error');
  }

  addSyncLog(message, type = 'info') {
    const logsContainer = document.getElementById('sync-logs');
    if (logsContainer) {
      const logEntry = document.createElement('div');
      logEntry.className = `log-entry log-${type}`;
      logEntry.innerHTML = `
        <span class="log-time">${new Date().toLocaleTimeString()}</span>
        <span class="log-message">${message}</span>
      `;
      logsContainer.insertBefore(logEntry, logsContainer.firstChild);
    }
  }
}

// Initialize sync manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
  window.syncManager = new SyncManager();
  
  // Initial sync if online
  if (navigator.onLine) {
    window.syncManager.sync();
  }
}); 