import logging
from app.config import Config

def configure_logging() -> logging.Logger:
    """Configura o sistema de logging para aplicação com handlers duplos"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler padrão para stdout
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Handler adicional para arquivo em desenvolvimento
    if Config.ENVIRONMENT == "development":
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = configure_logging()
