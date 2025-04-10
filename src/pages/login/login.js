document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // TODO: Implement authentication logic
    try {
        // For now, just redirect to main page
        window.location.href = '../main/main.html';
    } catch (error) {
        console.error('Login failed:', error);
        alert('Erro no login. Por favor, tente novamente.');
    }
});
