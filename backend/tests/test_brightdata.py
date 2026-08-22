import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from main import app
from app.services.brightdata_service import (
    BrightDataService,
    BrightDataAuthError,
    CollectorNotFoundError,
    ScraperRunFailedError,
    ScraperEmptyResultError,
    ScraperInvalidOutputError,
    ScraperTimeoutError
)

client = TestClient(app)

def test_service_auth_error():
    service = BrightDataService()
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error: No API key found. Run 'brightdata login'"
        )
        with pytest.raises(BrightDataAuthError):
            service.run_collector("c_mock123")

def test_service_collector_not_found_error():
    service = BrightDataService()
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error: collector c_not_exist not found"
        )
        with pytest.raises(CollectorNotFoundError):
            service.run_collector("c_not_exist")

def test_service_empty_result_error():
    service = BrightDataService()
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(
            returncode=0,
            stdout="[]",
            stderr=""
        )
        with pytest.raises(ScraperEmptyResultError):
            service.run_collector("c_mock123")

def test_service_invalid_output_error():
    service = BrightDataService()
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(
            returncode=0,
            stdout="Not valid json string",
            stderr=""
        )
        with pytest.raises(ScraperInvalidOutputError):
            service.run_collector("c_mock123")

def test_service_successful_run():
    service = BrightDataService()
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(
            returncode=0,
            stdout='[{"title": "Test Title", "url": "https://supabase.com/changelog/test"}]',
            stderr=""
        )
        result = service.run_collector("c_mock123", "https://supabase.com/changelog")
        assert len(result) == 1
        assert result[0]["title"] == "Test Title"

@patch("app.api.sources.brightdata_service.run_collector")
@patch("app.api.sources.brightdata_settings")
def test_api_scrape_source_mocked(mock_settings, mock_run_collector):
    mock_settings.BRIGHT_DATA_COLLECTOR_ID = "c_m1mocked123"
    mock_run_collector.return_value = [
        {
            "title": "Read replicas moved to Project Settings",
            "published_date": "2026-08-21",
            "category": "Improvement",
            "description": "Read replica management updated",
            "url": "https://supabase.com/changelog/read-replicas"
        }
    ]

    response = client.post("/sources/supabase_changelog/scrape")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["records_found"] == 1
    assert data["validation"]["status"] == "passed"
    assert data["validation"]["score"] == 100.0
