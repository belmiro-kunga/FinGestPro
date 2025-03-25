# FinGest Pro - Sistema de Gestão Financeira

Sistema completo de gestão financeira desenvolvido com Django, PostgreSQL e Redis.

## Requisitos

- Docker
- Docker Compose
- Python 3.11+
- Django 5.1.7
- PostgreSQL 15
- Redis 7

## Configuração com Django (Desenvolvimento Local)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/FinGestPro.git
cd FinGestPro
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/Scripts/activate  # No Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (.env):
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=fingestpro
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/1
```

5. Configure o banco de dados:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Execute o servidor:
```bash
python manage.py runserver
```

O sistema estará disponível em:
- Interface Web: http://localhost:8000
- Painel Admin: http://localhost:8000/admin

## Configuração com Docker

### Serviços

O projeto utiliza três serviços Docker:

1. **Web (Django)**
   - Porta: 8000
   - Imagem: Python 3.11
   - Dependências: requirements.txt

2. **PostgreSQL**
   - Porta: 5432
   - Versão: 15
   - Banco de dados: fingestpro
   - Usuário: postgres

3. **Redis**
   - Porta: 6379
   - Versão: 7
   - Usado para cache

### Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/FinGestPro.git
cd FinGestPro
```

2. Inicie os containers:
```bash
docker-compose up -d
```

3. Acesse o sistema:
   - Interface Web: http://localhost:8000
   - Painel Admin: http://localhost:8000/admin
     - Usuário: admin
     - Senha: admin123

### Comandos Úteis

- Visualizar logs:
```bash
docker-compose logs -f
```

- Reiniciar serviços:
```bash
docker-compose restart
```

- Parar serviços:
```bash
docker-compose down
```

- Reconstruir containers:
```bash
docker-compose up -d --build
```

## Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - SECRET_KEY=your-secret-key
      - DB_NAME=fingestpro
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=fingestpro
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:

### Ambiente Docker

#### Configuração do Ambiente

1. **Instalação do Docker**
   - Windows: [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop)
   - Linux: 
     ```bash
     curl -fsSL https://get.docker.com | sh
     ```

2. **Instalação do Docker Compose**
   - Windows: Incluído no Docker Desktop
   - Linux:
     ```bash
     sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```

#### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Django
DEBUG=True
SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=fingestpro
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/1
```

#### Desenvolvimento com Docker

1. **Primeira Execução**
   ```bash
   # Clone o repositório
   git clone https://github.com/seu-usuario/FinGestPro.git
   cd FinGestPro

   # Crie o arquivo .env
   cp .env.example .env

   # Construa e inicie os containers
   docker-compose up -d --build

   # Execute as migrações
   docker-compose exec web python manage.py migrate

   # Crie um superusuário
   docker-compose exec web python manage.py createsuperuser
   ```

2. **Execuções Subsequentes**
   ```bash
   # Inicie os containers
   docker-compose up -d

   # Pare os containers
   docker-compose down
   ```

3. **Desenvolvimento**
   ```bash
   # Visualize os logs em tempo real
   docker-compose logs -f web

   # Execute comandos no container
   docker-compose exec web python manage.py shell

   # Instale novas dependências
   docker-compose exec web pip install nome-do-pacote
   docker-compose exec web pip freeze > requirements.txt
   ```

4. **Backup e Restauração**
   ```bash
   # Backup
   docker-compose exec db pg_dump -U postgres fingestpro > backup.sql

   # Restauração
   docker-compose exec -T db psql -U postgres fingestpro < backup.sql
   ```

#### Solução de Problemas

1. **Problemas de Permissão**
   ```bash
   # Linux/Mac: Ajuste as permissões
   sudo chown -R $USER:$USER .
   ```

2. **Containers não Iniciam**
   ```bash
   # Verifique os logs
   docker-compose logs

   # Reconstrua os containers
   docker-compose down -v
   docker-compose up -d --build
   ```

3. **Banco de Dados**
   ```bash
   # Resetar o banco de dados
   docker-compose down -v
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   ```

4. **Cache**
   ```bash
   # Limpar o cache do Redis
   docker-compose exec redis redis-cli FLUSHALL
   ```

### Comandos Docker

#### Construção e Inicialização
```bash
# Construir as imagens
docker-compose build

# Iniciar os serviços
docker-compose up -d

# Construir e iniciar (combinado)
docker-compose up -d --build
```

#### Gerenciamento de Containers
```bash
# Verificar status dos containers
docker-compose ps

# Verificar logs
docker-compose logs -f

# Acessar shell do container web
docker-compose exec web bash

# Parar os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

#### Comandos Django no Container
```bash
# Criar migrações
docker-compose exec web python manage.py makemigrations

# Aplicar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --no-input
```

#### Backup e Restauração
```bash
# Backup do banco de dados
docker-compose exec db pg_dump -U postgres fingestpro > backup.sql

# Restaurar banco de dados
docker-compose exec -T db psql -U postgres fingestpro < backup.sql
```

### Volumes Docker

O projeto utiliza os seguintes volumes:
- `postgres_data`: Armazena os dados do PostgreSQL
- `.:/app`: Mount do código fonte no container web

### Redes Docker

Os serviços estão conectados na mesma rede Docker, permitindo comunicação através dos seguintes hostnames:
- `web`: Aplicação Django
- `db`: Banco de dados PostgreSQL
- `redis`: Cache Redis

### Portas Expostas

- `8000`: Django web server
- `5432`: PostgreSQL
- `6379`: Redis

## Estrutura do Projeto

O projeto está organizado nos seguintes módulos:

- **assinaturas**: Gestão de assinaturas e planos
- **usuarios**: Autenticação e controle de usuários
- **clientes**: Cadastro e gestão de clientes
- **estoque_controle**: Controle de inventário
- **faturacao**: Sistema de faturamento
- **estoque**: Gestão de produtos
- **relatorios**: Geração de relatórios
- **reservas**: Sistema de reservas
- **rh**: Recursos Humanos
- **pos**: Ponto de Venda

## Configurações

As principais configurações estão definidas em `fingest_pro/settings.py`:

- Banco de dados: PostgreSQL
- Cache: Redis
- Idioma: Português (Brasil)
- Fuso horário: Africa/Luanda
- Debug: Ativo em desenvolvimento

## Segurança

O sistema inclui:
- Middleware de prevenção SQL Injection
- Middleware de permissões de usuário
- Middleware de atividade do usuário
- Proteção CSRF
- Autenticação JWT