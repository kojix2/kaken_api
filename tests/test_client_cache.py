"""
Tests for the KakenApiClient cache functionality.
"""

import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

import pytest
import requests
from kaken_api import KakenApiClient


@pytest.fixture
def temp_cache_dir():
    """
    Fixture that provides a temporary directory for cache files.
    
    The directory is automatically deleted after the test.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_client_cache_initialization():
    """Test client cache initialization."""
    # Default initialization (cache enabled)
    client = KakenApiClient()
    assert client.cache.enabled is True
    
    # Disabled cache
    client = KakenApiClient(use_cache=False)
    assert client.cache.enabled is False
    
    # Custom cache directory
    with tempfile.TemporaryDirectory() as temp_dir:
        client = KakenApiClient(cache_dir=temp_dir)
        assert str(client.cache.cache_dir) == temp_dir


@patch('requests.Session.request')
def test_client_cache_hit(mock_request, temp_cache_dir):
    """Test client cache hit."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"test": "data"}'
    mock_request.return_value = mock_response
    
    # Create a client with a custom cache directory
    client = KakenApiClient(cache_dir=temp_cache_dir)
    
    # Make a request (this should cache the response)
    url = "https://example.com/api"
    client.session.get(url)
    
    # Make the same request again (this should use the cached response)
    client.session.get(url)
    
    # Verify that the request was only made once
    assert mock_request.call_count == 1


@patch('requests.Session.request')
def test_client_cache_miss(mock_request, temp_cache_dir):
    """Test client cache miss."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"test": "data"}'
    mock_request.return_value = mock_response
    
    # Create a client with a custom cache directory
    client = KakenApiClient(cache_dir=temp_cache_dir)
    
    # Make a request (this should cache the response)
    url1 = "https://example.com/api1"
    client.session.get(url1)
    
    # Make a different request (this should not use the cached response)
    url2 = "https://example.com/api2"
    client.session.get(url2)
    
    # Verify that the request was made twice
    assert mock_request.call_count == 2


@patch('requests.Session.request')
def test_client_cache_disabled(mock_request, temp_cache_dir):
    """Test client with disabled cache."""
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"test": "data"}'
    mock_request.return_value = mock_response
    
    # Create a client with disabled cache
    client = KakenApiClient(use_cache=False, cache_dir=temp_cache_dir)
    
    # Make a request (this should not cache the response)
    url = "https://example.com/api"
    client.session.get(url)
    
    # Make the same request again (this should not use the cached response)
    client.session.get(url)
    
    # Verify that the request was made twice
    assert mock_request.call_count == 2
