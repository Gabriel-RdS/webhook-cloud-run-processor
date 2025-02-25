import pytest
from unittest.mock import patch
from flask import Flask

class TestWebhookStream:
    def test_webhook_stream_without_url(self, client):
        response = client.post('/webhook_stream', json={})
        assert response.status_code == 400
        
    def test_webhook_stream_success(self, client):
        with patch('app.routes.webhook_stream.save_request_to_gcs'), \
             patch('app.routes.webhook_stream.process_file'):
            response = client.post('/webhook_stream', 
                                 json={'url': 'http://test.com'})
            assert response.status_code == 202