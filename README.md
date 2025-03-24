# FinGest Pro

Sistema de Gestão Financeira desenvolvido com Django

## Requisitos

- Python 3.13+
- Django 5.1.7
- Virtualenv (recomendado)

## Instalação

1. Clone o repositório
```bash
git clone [url-do-repositório]
cd fingest_pro
```

2. Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/Scripts/activate  # No Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados
```bash
python manage.py migrate
```

5. Crie um superusuário (admin)
```bash
python manage.py createsuperuser
```

6. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

O sistema estará disponível em `http://localhost:8000`

## Funcionalidades

- [Em desenvolvimento]

## Estrutura do Projeto

- `fingest_pro/` - Configurações principais do projeto
- `manage.py` - Script de gerenciamento do Django 