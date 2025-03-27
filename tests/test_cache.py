"""
Tests for the ResponseCache class.
"""

import os
import tempfile
import shutil
from pathlib import Path

import pytest
from kaken_api.cache import ResponseCache


@pytest.fixture
def temp_cache_dir():
    """
    Fixture that provides a temporary directory for cache files.
    
    The directory is automatically deleted after the test.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_cache_initialization():
    """Test cache initialization."""
    # Default initialization
    cache = ResponseCache()
    assert cache.enabled is True
    assert cache.cache_dir.exists()
    
    # Disabled cache
    cache = ResponseCache(enabled=False)
    assert cache.enabled is False


def test_cache_get_set(temp_cache_dir):
    """Test cache get and set."""
    cache = ResponseCache(cache_dir=temp_cache_dir)
    
    # Set a cache entry
    url = "https://example.com/api"
    content = b"Test content"
    cache.set(url, content)
    
    # Get the cache entry
    cached_content = cache.get(url)
    assert cached_content == content
    
    # Get a non-existent cache entry
    cached_content = cache.get("https://example.com/nonexistent")
    assert cached_content is None


def test_cache_clear(temp_cache_dir):
    """Test cache clear."""
    cache = ResponseCache(cache_dir=temp_cache_dir)
    
    # Set some cache entries
    cache.set("https://example.com/api1", b"Test content 1")
    cache.set("https://example.com/api2", b"Test content 2")
    
    # Verify that the cache entries exist
    assert cache.get("https://example.com/api1") is not None
    assert cache.get("https://example.com/api2") is not None
    
    # Clear the cache
    cache.clear()
    
    # Verify that the cache entries are gone
    assert cache.get("https://example.com/api1") is None
    assert cache.get("https://example.com/api2") is None


def test_cache_disabled(temp_cache_dir):
    """Test disabled cache."""
    cache = ResponseCache(cache_dir=temp_cache_dir, enabled=False)
    
    # Set a cache entry
    url = "https://example.com/api"
    content = b"Test content"
    cache.set(url, content)
    
    # Get the cache entry (should be None)
    cached_content = cache.get(url)
    assert cached_content is None
