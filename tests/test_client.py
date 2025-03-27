"""
Tests for the KakenApiClient class.
"""

import pytest
from kaken_api import KakenApiClient


def test_client_initialization(app_id):
    """Test client initialization with app_id."""
    client = KakenApiClient(app_id=app_id)
    assert client is not None
    assert client.app_id == app_id
    assert client.projects is not None
    assert client.researchers is not None
    client.close()


def test_client_initialization_without_app_id():
    """Test client initialization without app_id."""
    client = KakenApiClient()
    assert client is not None
    assert client.app_id is None
    assert client.projects is not None
    assert client.researchers is not None
    client.close()


def test_client_context_manager(app_id):
    """Test client as a context manager."""
    with KakenApiClient(app_id=app_id) as client:
        assert client is not None
        assert client.app_id == app_id
        assert client.projects is not None
        assert client.researchers is not None
    # Context manager should close the client automatically


def test_client_timeout_and_retries():
    """Test client initialization with custom timeout and retries."""
    client = KakenApiClient(timeout=60, max_retries=5)
    assert client is not None
    assert client.timeout == 60
    assert client.max_retries == 5
    client.close()
