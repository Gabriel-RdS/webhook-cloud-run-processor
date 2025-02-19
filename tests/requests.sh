#Local

# ----| Arquivo pequeno para teste
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.filesampleshub.com/download/code/parquet/sample3.parquet"}' 


# ----| Arquivo de 7.18gb
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.kaggle.com/api/v1/datasets/download/amandamartin62/simulated-transactions-parquet-format"}'