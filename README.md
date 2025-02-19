# 🚀 Integração de Webhook com Cloud Run

**Processamento seguro de arquivos em tempo real com integração GCP**

[![Python 3.11](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![GCP Compatible](https://img.shields.io/badge/GCP-Cloud_Run%20%7C%20Secret_Manager%20%7C%20GCS-orange.svg)](https://cloud.google.com)

## ✨ Funcionalidades Principais
- **Processamento Seguro de Webhooks**
  - Validação de IPs permitidos via lista configurável
  - Autenticação via token da API Insider (armazenado no Secret Manager)
- **Upload Automático para GCS**
  - Detecção automática de tipo MIME
  - Nomenclatura única para arquivos com UUID
- **Monitoramento em Tempo Real**
  - Logging detalhado com dual output (console/arquivo)
  - Trackeamento de progresso de uploads grandes
- **Configuração Flexível**
  - Variáveis de ambiente para múltiplos ambientes
  - Healthcheck endpoint para monitoramento

## 🛠 Tecnologias Utilizadas
- **Core**: Python 3.11, Flask 2.x
- **GCP**: Cloud Run, Secret Manager, Cloud Storage
- **Segurança**: Validação de IP, Content-Type restrictions
- **DevOps**: Docker (implícito no Cloud Run), GitHub Actions

## 📦 Estrutura do Projeto
```
.
├── app/
│   ├── routes/          # Definicoes de endpoints
│   ├── services/        # Lógica de negócios
│   ├── storage/         # Integrações com GCS
│   ├── utils/           # Helpers e utilities
│   ├── config.py        # Configurações dinâmicas
│   └── __init__.py
├── credentials/         # Service accounts (local dev)
├── tests/              # Testes unitários/integração
├── app.py              # Entry point principal
├── requirements.txt    # Dependências
└── README.md           # Este arquivo
```

## ⚙️ Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```
# Configurações obrigatórias
BUCKET_NAME="seu-bucket-gcs"
PROJECT_ID="projeto-gcp"
ALLOWED_IPS="127.0.0.1,34.122.0.0/20"  # IPs autorizados

# Secrets (gerados via Secret Manager)
INSIDER_API_TOKEN_SECRET="nome-do-secret"

# Ambiente (development|production)
ENVIRONMENT="development"
```

### Instalação Local
```
# 1. Clone o repositório
git clone https://github.com/seu-usuario/webhook-processor.git
cd webhook-processor

# 2. Configure ambiente virtual
python -m venv venv
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute (modo desenvolvimento)
ENVIRONMENT=development python app.py
```

## 🌐 Deployment no Cloud Run
```
# Build e deploy via gcloud CLI
gcloud run deploy webhook-processor \
  --source . \
  --region southamerica-east1 \
  --allow-unauthenticated \
  --set-env-vars "ENVIRONMENT=production"
```

**Endpoints:**
- `POST /`: Processamento principal de webhooks
- `GET /healthcheck`: Status do serviço (200 OK)

## 🧪 Testando a API
```
# Exemplo de requisição
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com/arquivo.parquet"}'
```

## 🤝 Como Contribuir
1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença
Distribuído sob licença Apache 2.0. Veja `LICENSE` para mais informações.

## 🚨 Troubleshooting
Problemas comuns e soluções:
- **Erro 403 (Acesso negado)**: Verifique ALLOWED_IPS e X-Forwarded-For
- **Falha no upload**: Valide permissões do service account no GCS
- **Logs incompletos**: Configure ENVIRONMENT=development para logging em arquivo

> [!TIP]
> Use `make local-env` para subir ambiente com Docker Compose (exemplo no Makefile)