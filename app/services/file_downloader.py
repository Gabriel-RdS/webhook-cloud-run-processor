import requests
import logging
from typing import Optional
from app.config import Config
from app.utils.logging import logger
from werkzeug.exceptions import abort

class LoggingStreamWrapper:
    def __init__(self, stream, total: Optional[int], logger: logging.Logger):
        self.stream = stream
        self.total = total
        self.logger = logger
        self.bytes_read = 0

    def read(self, size: int = -1) -> bytes:
        data = self.stream.read(size)
        if data:
            self.bytes_read += len(data)
            if self.total:
                percent = (self.bytes_read / self.total) * 100
                self.logger.info(f"Lendo {self.bytes_read}/{self.total} bytes ({percent:.2f}%).")
            else:
                self.logger.info(f"Lendo {self.bytes_read} bytes.")
        return data

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def safe_download(file_url: str) -> requests.Response:
    headers = {
        "User-Agent": "InsiderSafeDownloader/1.0",
        "Authorization": f"Bearer {Config.INSIDER_API_TOKEN}"
    }
    try:
        response = requests.get(file_url, headers=headers, stream=True)
        response.raise_for_status()
        
        valid_content_types = [
            "application/octet-stream",
            "application/parquet",
            "text/csv",
            "application/json",
            "application/x-json",
            "application/zip",
            "application/x-zip-compressed",
            "application/gzip",
            "application/x-gzip"
        ]
        
        if response.headers.get("Content-Type") not in valid_content_types:
            logger.error("Tipo de arquivo inválido")
            abort(400, description="Tipo de arquivo não suportado")
            
        return response
    except requests.RequestException as e:
        logger.error(f"Erro no download: {str(e)}")
        abort(502, description="Erro ao processar arquivo remoto")

def get_file_extension(content_type: str) -> str:
    content_type_mapping = {
        "application/parquet": "parquet",
        "text/csv": "csv",
        "application/json": "json",
        "application/x-json": "json",
        "application/zip": "zip",
        "application/x-zip-compressed": "zip",
        "application/gzip": "gzip",
        "application/x-gzip": "gzip",
        "application/octet-stream": "parquet"
    }
    return content_type_mapping.get(content_type, "parquet")
