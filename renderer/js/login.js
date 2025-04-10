document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('errorMessage');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = emailInput.value.trim();
            const password = passwordInput.value;
            
            if (!email || !password) {
                showError('Por favor, preencha todos os campos');
                return;
            }
            
            try {
                // In a real app, this would call the main process to authenticate
                // For now, we'll simulate a successful login
                const success = await window.api.login(email, password);
                
                if (success) {
                    // Redirect to dashboard on successful login
                    window.location.href = 'index.html';
                } else {
                    showError('Email ou senha incorretos');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('Erro ao fazer login. Tente novamente.');
            }
        });
    }

    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        }
    }
}); 