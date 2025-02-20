from typing import Optional
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import abort
from app.config import Config
from app.storage.gcs_client import GoogleCloudStorage
from app.services.file_downloader import safe_download, LoggingStreamWrapper, get_file_extension
from app.utils.logging import logger
import uuid
import datetime

webhook_chunked_bp = Blueprint('webhook_chunked', __name__)

@webhook_chunked_bp.before_request
def restrict_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr
    if ip not in Config.ALLOWED_IPS:
        logger.error(f"IP não autorizado: {ip}")
        abort(403, description="Acesso negado")

@webhook_chunked_bp.route("/webhook_chunked", methods=["POST"])
def handle_webhook_chunked_route():
    payload = request.get_json(silent=True) or {}
    if not payload.get("url"):
        logger.error("Requisição sem URL válida")
        abort(400, description="Parâmetro URL ausente")

    try:
        logger.info("Iniciando processamento do webhook em chunks.")
        storage_client = GoogleCloudStorage()
        url = payload["url"]

        logger.info(f"Iniciando download do arquivo em chunks: {url}")
        response = safe_download(url)

        content_type = response.headers.get("Content-Type")
        total_size = response.headers.get("Content-Length")
        total_size = int(total_size) if total_size else None

        if not total_size:
            logger.info("Content-Length não informado; monitoramento limitado do progresso.")

        extension = get_file_extension(content_type)
        arquivo_nome = f"staging/insider/{datetime.datetime.now().year}/{datetime.datetime.now().month:02}/{datetime.datetime.now().day:02}/secured_export_{uuid.uuid4().hex}.{extension}"
        chunk_size = 256 * 1024 * 1024  # 256MB

        logger.info(f"Iniciando upload para o GCS em chunks em {arquivo_nome}")
        stream = LoggingStreamWrapper(response.raw, total_size, logger)
        storage_client.upload_parquet_chunks(stream, arquivo_nome, chunk_size)
        logger.info("Upload em chunks concluído com sucesso.")

        return jsonify({"status": "Processamento concluído (chunks)"}), 200

    except Exception as e:
        logger.error(f"Erro interno: {e}", exc_info=True)
        abort(500, description="Erro interno do servidor")