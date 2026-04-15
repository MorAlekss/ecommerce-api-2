import sys
sys.path.insert(0, '.')
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.utils.http import get, post, put, patch as http_patch, delete
from src.utils.middleware import authenticated_get, authenticated_post


def _build_mock_client():
    """Create a mock AsyncClient context manager with a mock response."""
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    mock_client.put.return_value = mock_response
    mock_client.patch.return_value = mock_response
    mock_client.delete.return_value = mock_response
    return mock_client, mock_response


@pytest.mark.asyncio
async def test_get():
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client, mock_response = _build_mock_client()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response.json.return_value = {"data": "value"}
        result = await get("https://api.example.com/test")
        assert result["data"] == "value"


@pytest.mark.asyncio
async def test_post():
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client, mock_response = _build_mock_client()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response.json.return_value = {"id": "123"}
        result = await post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"


@pytest.mark.asyncio
async def test_authenticated_get():
    with patch('src.utils.middleware.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "secure"}
        mock_response.raise_for_status.return_value = None
        mock_client.get.return_value = mock_response
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"
