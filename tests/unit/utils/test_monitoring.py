import pytest
from unittest.mock import patch
from app.utils.monitoring import Monitoring

class TestMonitoring:
    @pytest.fixture
    def monitor(self):
        return Monitoring(
            success_webhook_url='http://success.com',
            failure_webhook_url='http://failure.com'
        )

    @patch('requests.post')
    def test_send_success_message(self, mock_post, monitor):
        monitor.send_success_message('test-uuid', 'test-file.parquet')
        mock_post.assert_called_once()