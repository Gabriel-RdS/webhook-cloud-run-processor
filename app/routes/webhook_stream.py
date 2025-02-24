import uuid
import threading
import json
import datetime
from typing import Optional
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response
from app.config import Config
from app.storage.gcs_client import GoogleCloudStorage
from app.services.file_downloader import safe_download, get_file_extension
from app.utils.logging import logger
from app.utils.webhook_utils import save_request_to_gcs

webhook_stream_bp = Blueprint('webhook_stream', __name__)

@webhook_stream_bp.before_request
def restrict_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr
    if ip not in Config.ALLOWED_IPS:
        logger.error(f"IP não autorizado: {ip}")
        abort(403, description="Acesso negado")

@webhook_stream_bp.route("/webhook_stream", methods=["POST"])
def handle_webhook_stream_route():
    payload = request.get_json(silent=True) or {}
    if not payload.get("url"):
        logger.error("Requisição sem URL válida")
        abort(400, description="Parâmetro URL ausente")

    try:
        logger.info("Requisição recebida para processamento no webhook_stream.")
  
        # Gerar UUID para rastreamento
        file_uuid = uuid.uuid4().hex
  
        # Salvar a requisição no GCS (função similar à do webhook_chunked)
        save_request_to_gcs(payload, file_uuid)
  
        # Retornar a resposta "202 Accepted" imediatamente
        response = jsonify({"status": "Processamento iniciado em segundo plano"})
        response.status_code = 202
  
        # Iniciar o processamento em segundo plano
        threading.Thread(target=process_file, args=(payload, file_uuid)).start()
  
        return response
  
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {e}", exc_info=True)
        abort(500, description="Erro interno do servidor")

def get_stream(response, content_type: str, total_size: Optional[int]):
    """Centraliza a criação do stream com tratamento adequado"""
    if content_type not in ["application/zip", "application/gzip", "application/x-gzip"]:
        response.raw.decode_content = True

    if total_size:
        from app.services.file_downloader import LoggingStreamWrapper
        return LoggingStreamWrapper(response.raw, total_size, logger)
    return response.raw

def process_file(payload, file_uuid):
    try:
        storage_client = GoogleCloudStorage()
        url = payload["url"]
  
        logger.info(f"Iniciando download do arquivo: {url}")
        response = safe_download(url)
  
        content_type = response.headers.get("Content-Type")
        total_size = response.headers.get("Content-Length")
        total_size = int(total_size) if total_size else None
  
        if not total_size:
            logger.info("Content-Length não informado; monitoramento limitado do progresso.")
  
        extension = get_file_extension(content_type)
        now = datetime.datetime.now()
        arquivo_nome = f"staging/insider/{now.year}/{now.month:02}/{now.day:02}/secured_export_{file_uuid}.{extension}"
        # Defina um chunk size apropriado, se necessário
        chunk_size = 256 * 1024 * 1024  # ex: 256MB
  
        logger.info(f"Iniciando upload para o GCS em chunks em {arquivo_nome}")
  
        # Se a sua aplicação faz upload em chunks via um método específico (como upload_parquet_chunks), use-o
        # Caso contrário, pode ser um upload normal
        stream = get_stream(response, content_type, total_size)
        storage_client.upload_stream(stream, arquivo_nome)
        logger.info("Upload concluído com sucesso.")
  
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}", exc_info=True)