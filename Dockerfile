# Use uma imagem base Python oficial
FROM python:3.11-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG=True
ENV SECRET_KEY=insecure-development-key
ENV ALLOWED_HOSTS=localhost,127.0.0.1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Cria diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles

# Expõe a porta 8000
EXPOSE 8000

# Comando para executar o Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fingest_pro.wsgi:application"]
