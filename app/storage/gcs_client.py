from google.cloud import storage
from app.config import Config
from app.utils.logging import logger

class GoogleCloudStorage:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(Config.BUCKET_NAME)

    def upload_stream(self, stream, filename: str) -> storage.Blob:
        """Faz upload de um stream de dados para o GCS com tipo MIME apropriado"""
        blob = self.bucket.blob(filename)
        
        content_type_mapping = {
            "parquet": "application/parquet",
            "csv": "text/csv",
            "json": "application/json"
        }
        
        extension = filename.split(".")[-1]
        content_type = content_type_mapping.get(extension, "application/octet-stream")
        
        blob.content_type = content_type
        blob.cache_control = "no-cache, no-store, must-revalidate"
        blob.upload_from_file(stream, content_type=content_type)
        
        logger.info(f"Arquivo {filename} enviado com sucesso.")
        return blob
    
    def upload_parquet_chunks(self, stream, filename: str, chunk_size: int = 1024*1024) -> storage.Blob:
        """Faz upload de um stream de dados Parquet para o GCS em chunks."""
        blob = self.bucket.blob(filename)
        blob.content_type = "application/parquet"
        blob.cache_control = "no-cache, no-store, must-revalidate"

        with blob.open("wb", chunk_size=chunk_size) as f:
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        logger.info(f"Arquivo {filename} enviado em chunks com sucesso.")
        return blob
