import pytest
from unittest.mock import patch
from flask import Flask

class TestWebhookChunked:
    def test_webhook_chunked_without_url(self, client):
        response = client.post('/webhook_chunked', json={})
        assert response.status_code == 400
        
    def test_webhook_chunked_success(self, client):
        with patch('app.routes.webhook_chunked.save_request_to_gcs'), \
             patch('app.routes.webhook_chunked.process_file'):
            response = client.post('/webhook_chunked', 
                                 json={'url': 'http://test.com'})
            assert response.status_code == 202