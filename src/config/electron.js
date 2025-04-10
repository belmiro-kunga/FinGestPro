const Store = require('electron-store');

const store = new Store({
    defaults: {
        windowBounds: {
            width: 1200,
            height: 800
        },
        isDarkMode: false,
        autoSync: true,
        syncInterval: 30, // minutes
        lastSyncTime: null
    }
});

module.exports = {
    store,
    getWindowBounds: () => store.get('windowBounds'),
    setWindowBounds: (bounds) => store.set('windowBounds', bounds),
    isDarkMode: () => store.get('isDarkMode'),
    setDarkMode: (value) => store.set('isDarkMode', value),
    getAutoSync: () => store.get('autoSync'),
    setAutoSync: (value) => store.set('autoSync', value),
    getSyncInterval: () => store.get('syncInterval'),
    setSyncInterval: (minutes) => store.set('syncInterval', minutes),
    getLastSyncTime: () => store.get('lastSyncTime'),
    setLastSyncTime: (time) => store.set('lastSyncTime', time)
};
