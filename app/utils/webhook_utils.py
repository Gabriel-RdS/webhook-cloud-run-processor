import json
import datetime
from app.storage.gcs_client import GoogleCloudStorage
from app.utils.logging import logger
from app.utils.constants import Segment

def save_request_to_gcs(payload, file_uuid, segment):
    """
    Salva os detalhes da requisição no GCS em uma estrutura organizada por data.
    """
    try:
        storage_client = GoogleCloudStorage()
        now = datetime.datetime.now()
        base_path = Segment.get_base_path(segment)
        request_filename = f"{base_path}/requests/{now.year}/{now.month:02}/{now.day:02}/request_{file_uuid}.json"
  
        # Converter o payload para JSON com formatação amigável
        request_data = json.dumps(payload, indent=2)
  
        # Fazer upload do JSON para o GCS
        storage_client.upload_string(request_data, request_filename, content_type='application/json')
        logger.info(f"Requisição salva em {request_filename}")
  
    except Exception as e:
        logger.error(f"Erro ao salvar requisição no GCS: {e}", exc_info=True)