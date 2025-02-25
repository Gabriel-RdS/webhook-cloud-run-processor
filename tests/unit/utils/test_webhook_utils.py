import pytest
from unittest.mock import patch
from app.utils.webhook_utils import save_request_to_gcs

class TestWebhookUtils:
    @patch('app.utils.webhook_utils.GoogleCloudStorage')
    def test_save_request_to_gcs(self, mock_storage):
        payload = {'url': 'http://test.com'}
        file_uuid = 'test-uuid'
        
        save_request_to_gcs(payload, file_uuid)
        
        mock_storage.return_value.upload_string.assert_called_once()