document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            // Aqui você pode adicionar a lógica de autenticação
            // Por exemplo, usando o IPC do Electron para comunicar com o processo principal
            window.electron.sendMessage('login-attempt', { username, password });
            
            // Exemplo de resposta do processo principal
            window.electron.receiveMessage('login-response', (response) => {
                if (response.success) {
                    // Redirecionar para a página principal
                    window.location.href = 'main.html';
                } else {
                    alert('Login falhou: ' + response.message);
                }
            });
        } catch (error) {
            console.error('Erro no login:', error);
            alert('Ocorreu um erro durante o login');
        }
    });
}); 