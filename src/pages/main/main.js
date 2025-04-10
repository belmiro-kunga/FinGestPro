// Main page functionality
document.addEventListener('DOMContentLoaded', () => {
    // Menu navigation
    const menuItems = document.querySelectorAll('.menu li');
    const pages = document.querySelectorAll('.page');

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all menu items
            menuItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            item.classList.add('active');

            // Show corresponding page
            const pageName = item.getAttribute('data-page');
            pages.forEach(page => {
                if (page.id === pageName) {
                    page.classList.add('active');
                } else {
                    page.classList.remove('active');
                }
            });
        });
    });

    // Sync button functionality
    const syncButton = document.getElementById('syncButton');
    syncButton.addEventListener('click', async () => {
        try {
            // TODO: Implement sync logic between SQLite and MySQL
            alert('Sincronização iniciada...');
        } catch (error) {
            console.error('Erro na sincronização:', error);
            alert('Erro na sincronização. Tente novamente.');
        }
    });

    // Logout functionality
    const logoutButton = document.getElementById('logoutButton');
    logoutButton.addEventListener('click', () => {
        // TODO: Implement proper logout logic
        window.location.href = '../login/login.html';
    });

    // Connection status check
    function updateConnectionStatus() {
        const statusIcon = document.querySelector('.connection-status i');
        const statusText = document.getElementById('connectionStatus');
        
        if (navigator.onLine) {
            statusIcon.className = 'fas fa-wifi';
            statusText.textContent = 'Online';
            statusIcon.style.color = '#2ecc71';
        } else {
            statusIcon.className = 'fas fa-wifi-slash';
            statusText.textContent = 'Offline';
            statusIcon.style.color = '#e74c3c';
        }
    }

    window.addEventListener('online', updateConnectionStatus);
    window.addEventListener('offline', updateConnectionStatus);
    updateConnectionStatus();
});
