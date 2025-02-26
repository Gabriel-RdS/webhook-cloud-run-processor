import uuid
import threading
import datetime
from app.utils.monitoring import Monitoring
from typing import Optional
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response
from app.config import Config
from app.storage.gcs_client import GoogleCloudStorage
from app.services.file_downloader import safe_download, get_file_extension
from app.utils.logging import logger
from app.utils.webhook_utils import save_request_to_gcs
from app.utils.constants import Segment

webhook_stream_bp = Blueprint('webhook_stream', __name__)
monitor = Monitoring()

@webhook_stream_bp.before_request
def restrict_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr
    if ip not in Config.ALLOWED_IPS:
        logger.error(f"IP não autorizado: {ip}")
        abort(403, description="Acesso negado")

@webhook_stream_bp.route("/webhook_stream/<segment>", methods=["POST"])
def handle_webhook_stream_route(segment: str):
    if not Segment.is_valid(segment):
        logger.error(f"Segmento não autorizado: {segment}")
        abort(400, description="Segmento não autorizado")

    payload = request.get_json(silent=True) or {}
    if not payload.get("url"):
        logger.error("Requisição sem URL válida")
        abort(400, description="Parâmetro URL ausente")

    try:
        logger.info(f"Requisição recebida para processamento no webhook_stream para {segment}.")
        
        file_uuid = uuid.uuid4().hex
        save_request_to_gcs(payload, file_uuid, segment)
        
        response = jsonify({"status": "Processamento iniciado em segundo plano"})
        response.status_code = 202
        
        threading.Thread(target=process_file, args=(payload, file_uuid, segment)).start()
        
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

def process_file(payload, file_uuid, segment):
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
        
        base_path = Segment.get_base_path(segment)
        arquivo_nome = f"{base_path}/{now.year}/{now.month:02}/{now.day:02}/secured_export_{file_uuid}.{extension}"
        
        logger.info(f"Iniciando upload para o GCS em chunks em {arquivo_nome}")
        stream = get_stream(response, content_type, total_size)
        storage_client.upload_stream(stream, arquivo_nome)
        logger.info("Upload concluído com sucesso.")
        monitor.send_success_message(file_uuid, arquivo_nome)
    
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}", exc_info=True)
        monitor.send_failure_message(file_uuid, "N/D", str(e))