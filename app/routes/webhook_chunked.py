import uuid
import datetime
import threading
from typing import Optional
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import abort
from app.config import Config
from app.utils.logging import logger
from app.storage.gcs_client import GoogleCloudStorage
from app.services.file_downloader import safe_download, LoggingStreamWrapper, get_file_extension
from app.utils.webhook_utils import save_request_to_gcs
from app.utils.monitoring import Monitoring

webhook_chunked_bp = Blueprint('webhook_chunked', __name__)
monitor = Monitoring()

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
        logger.info("Requisição recebida para processamento em chunks.")

        # Gerar UUID para rastreamento
        file_uuid = uuid.uuid4().hex

        # Salvar a requisição no GCS
        save_request_to_gcs(payload, file_uuid)

        # Retornar a resposta "202 Accepted"
        response = jsonify({"status": "Processamento iniciado em segundo plano"})
        response.status_code = 202

        # Iniciar o processamento em segundo plano
        threading.Thread(target=process_file, args=(payload, file_uuid)).start()

        return response

    except Exception as e:
        logger.error(f"Erro ao receber requisição: {e}", exc_info=True)
        abort(500, description="Erro ao receber requisição")

def process_file(payload, file_uuid):
    """Função para processar o arquivo em segundo plano."""
    try:
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
        now = datetime.datetime.now()
        arquivo_nome = f"staging/insider/{now.year}/{now.month:02}/{now.day:02}/secured_export_{file_uuid}.{extension}"
        chunk_size = 256 * 1024 * 1024  # 256MB

        logger.info(f"Iniciando upload para o GCS em chunks em {arquivo_nome}")
        stream = LoggingStreamWrapper(response.raw, total_size, logger)
        storage_client.upload_parquet_chunks(stream, arquivo_nome, chunk_size)
        logger.info("Upload em chunks concluído com sucesso.")

        logger.info(f"Arquivo {arquivo_nome} processado com sucesso.")
        monitor.send_success_message(file_uuid, arquivo_nome)

    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}", exc_info=True)
        logger.error("Erro ao processar arquivo.")
        monitor.send_failure_message(file_uuid, "N/D", str(e))