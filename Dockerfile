# Usar imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Garantir que o script init.sh tenha permissão de execução
RUN chmod +x /app/init.sh

# Expor a porta usada pelo Django
EXPOSE 8000

# Expor a porta usada pelo Django
CMD ["/app/init.sh"]


