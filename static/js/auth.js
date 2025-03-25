async function login(username, password) {
    try {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Armazena os tokens no localStorage
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            localStorage.setItem('user', JSON.stringify(data.user));

            // Redireciona para a URL fornecida pelo servidor
            window.location.href = data.redirect_url;
        } else {
            throw new Error(data.error || 'Erro ao fazer login');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert(error.message);
    }
}

// Função para fazer logout
async function logout() {
    try {
        const refreshToken = localStorage.getItem('refreshToken');
        
        if (refreshToken) {
            await fetch('/api/auth/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                },
                body: JSON.stringify({ refresh: refreshToken })
            });
        }
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
    } finally {
        // Limpa o localStorage e redireciona para a página inicial
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        window.location.href = '/';
    }
}

// Função para atualizar o token de acesso
async function refreshToken() {
    try {
        const refreshToken = localStorage.getItem('refreshToken');
        
        if (!refreshToken) {
            throw new Error('Refresh token não encontrado');
        }

        const response = await fetch('/api/auth/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('accessToken', data.access);
            return data.access;
        } else {
            throw new Error('Não foi possível atualizar o token');
        }
    } catch (error) {
        console.error('Erro ao atualizar token:', error);
        logout();
    }
}
