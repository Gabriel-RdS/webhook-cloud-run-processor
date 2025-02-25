import pytest
from flask import Flask
from app.routes.webhook_chunked import webhook_chunked_bp
from app.routes.webhook_stream import webhook_stream_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(webhook_chunked_bp)
    app.register_blueprint(webhook_stream_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()