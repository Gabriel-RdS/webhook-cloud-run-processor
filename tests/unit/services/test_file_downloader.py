import pytest
from unittest.mock import Mock, patch
from app.services.file_downloader import safe_download, get_file_extension

class TestFileDownloader:
    def test_get_file_extension(self):
        assert get_file_extension('application/parquet') == 'parquet'
        assert get_file_extension('text/csv') == 'csv'
        
    @patch('requests.get')
    def test_safe_download_success(self, mock_get):
        mock_response = Mock()
        mock_response.headers = {'Content-Type': 'application/parquet'}
        mock_get.return_value = mock_response
        
        response = safe_download('http://test.com/file.parquet')
        assert response == mock_response