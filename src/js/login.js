const mysql = require('mysql2/promise');
const bcrypt = require('bcrypt');

// Database connection configuration
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: '', // XAMPP default
    database: 'FinGestPro'
};

// Create database connection pool
const pool = mysql.createPool(dbConfig);

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const windowsAuthCheckbox = document.getElementById('windowsAuth');
    
    // Show/Hide password functionality
    const togglePassword = document.querySelector('.toggle-password');
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = this.querySelector('i');
        icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    });

    // Input validation and feedback
    const validateInput = (input, minLength = 3) => {
        const value = input.value.trim();
        const isValid = value.length >= minLength;
        
        input.style.borderColor = isValid ? 'var(--input-border)' : 'var(--error-color)';
        return isValid;
    };

    // Real-time validation
    usernameInput.addEventListener('input', () => validateInput(usernameInput));
    passwordInput.addEventListener('input', () => validateInput(passwordInput, 6));

    // Windows Authentication handler
    windowsAuthCheckbox.addEventListener('change', function() {
        if (this.checked) {
            usernameInput.value = process.env.USERNAME || '';
            usernameInput.disabled = true;
        } else {
            usernameInput.disabled = false;
        }
    });

    // Form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validate inputs
        const isUsernameValid = validateInput(usernameInput);
        const isPasswordValid = validateInput(passwordInput, 6);
        
        if (!isUsernameValid || !isPasswordValid) {
            errorMessage.textContent = 'Por favor, preencha todos os campos corretamente';
            errorMessage.style.opacity = '1';
            return;
        }

        // Show loading state
        const submitBtn = loginForm.querySelector('.btn-confirmar');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Entrando...';
        submitBtn.disabled = true;
        
        try {
            const connection = await pool.getConnection();
            
            try {
                const [rows] = await connection.execute(
                    'SELECT * FROM usuarios WHERE username = ?',
                    [usernameInput.value]
                );
                
                if (rows.length === 0) {
                    throw new Error('Usuário não encontrado');
                }
                
                const user = rows[0];
                const match = await bcrypt.compare(passwordInput.value, user.password);
                
                if (!match) {
                    throw new Error('Senha incorreta');
                }
                
                // Success animation
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Sucesso!';
                submitBtn.style.backgroundColor = 'var(--success-color)';
                
                // Clear any error messages
                errorMessage.textContent = '';
                errorMessage.style.opacity = '0';
                
                // Redirect after success animation
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
                
            } finally {
                connection.release();
            }
            
        } catch (error) {
            console.error('Login error:', error);
            
            // Reset button
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            // Show error with animation
            errorMessage.textContent = error.message || 'Erro ao conectar com o banco de dados';
            errorMessage.style.opacity = '0';
            requestAnimationFrame(() => {
                errorMessage.style.opacity = '1';
            });
        }
    });
    
    // Cancel button handler with animation
    document.querySelector('.btn-cancelar').addEventListener('click', () => {
        // Animate form reset
        loginForm.style.opacity = '0.5';
        
        setTimeout(() => {
            usernameInput.value = '';
            passwordInput.value = '';
            windowsAuthCheckbox.checked = false;
            usernameInput.disabled = false;
            errorMessage.textContent = '';
            
            // Reset validation styles
            usernameInput.style.borderColor = 'var(--input-border)';
            passwordInput.style.borderColor = 'var(--input-border)';
            
            // Restore form opacity
            loginForm.style.opacity = '1';
        }, 200);
    });

    // Focus first input on load
    usernameInput.focus();
});

