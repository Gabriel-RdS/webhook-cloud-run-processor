import pytest
from unittest.mock import Mock, patch
from app.storage.gcs_client import GoogleCloudStorage

class TestGCSClient:
    @pytest.fixture
    def storage_client(self):
        with patch('google.cloud.storage.Client'):
            return GoogleCloudStorage()

    def test_upload_stream(self, storage_client):
        mock_stream = Mock()
        mock_blob = Mock()
        storage_client.bucket.blob = Mock(return_value=mock_blob)
        
        result = storage_client.upload_stream(mock_stream, 'test.parquet')
        assert result == mock_blob