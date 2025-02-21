# Imagem base oficial Python
FROM python:3.11-slim

# Variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Usuário não root para segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Porta que a aplicação escuta
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["python", "app.py"]