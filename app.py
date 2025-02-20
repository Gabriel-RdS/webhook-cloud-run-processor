from flask import Flask, Response
from app.config import Config
from app.routes import webhook, webhook_chunked
from app.utils.logging import logger

def create_app() -> Flask:
    """Factory principal para criação da aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registra Blueprints
    app.register_blueprint(webhook.webhook_bp)
    app.register_blueprint(webhook_chunked.webhook_chunked_bp)
    
    # Configuração adicional para Cloud Run
    @app.route("/healthcheck")
    def health_check():
        return "OK", 200

    return app

# Inicializa aplicação Flask
app = create_app()

def handle_webhook(request):
    """Entry point para Cloud Functions/Cloud Run"""
    logger.info("Requisição recebida no entrypoint do Cloud Run")
    return Response.from_app(app, request.environ)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=(Config.ENVIRONMENT == "development")
    )
