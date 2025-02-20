from typing import Optional
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response
from app.config import Config
from app.storage.gcs_client import GoogleCloudStorage
from app.services.file_downloader import safe_download, get_file_extension
from app.utils.logging import logger
import uuid

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
        logger.info("Iniciando processamento do webhook.")
        storage_client = GoogleCloudStorage()
        url = payload["url"]
        
        logger.info(f"Iniciando download do arquivo: {url}")
        response = safe_download(url)

        content_type = response.headers.get("Content-Type")
        total_size = response.headers.get("Content-Length")
        total_size = int(total_size) if total_size else None
        
        if not total_size:
            logger.info("Content-Length não informado; monitoramento limitado do progresso.")

        stream = get_stream(response, content_type, total_size)
        extension = get_file_extension(content_type)
        arquivo_nome = f"staging/insider/secured_export_{uuid.uuid4().hex}.{extension}"
        
        logger.info(f"Iniciando upload para o GCS em {arquivo_nome}")
        storage_client.upload_stream(stream, arquivo_nome)
        logger.info("Upload concluído com sucesso.")

        return jsonify({"status": "Processamento concluído"}), 200

    except Exception as e:
        logger.error(f"Erro interno: {e}", exc_info=True)
        abort(500, description="Erro interno do servidor")

def get_stream(response, content_type: str, total_size: Optional[int]):
    """Centraliza a criação do stream com tratamento adequado"""
    if content_type not in ["application/zip", "application/gzip", "application/x-gzip"]:
        response.raw.decode_content = True

    if total_size:
        from app.services.file_downloader import LoggingStreamWrapper
        return LoggingStreamWrapper(response.raw, total_size, logger)
    return response.raw