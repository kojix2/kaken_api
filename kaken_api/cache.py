"""
Cache module for the KAKEN API client.
"""

import os
import json
import hashlib
import logging
from typing import Dict, Any, Optional
from pathlib import Path


logger = logging.getLogger(__name__)


class ResponseCache:
    """Cache for API responses."""

    def __init__(self, cache_dir: Optional[str] = None, enabled: bool = True):
        """
        Initialize the response cache.

        Args:
            cache_dir: The directory to store cache files. If None, a default directory will be used.
            enabled: Whether the cache is enabled.
        """
        self.enabled = enabled
        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".kaken_api_cache")
        self.cache_dir = Path(cache_dir)
        
        # Create cache directory if it doesn't exist
        if self.enabled and not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created cache directory: {self.cache_dir}")

    def get(self, url: str) -> Optional[bytes]:
        """
        Get a cached response for the given URL.

        Args:
            url: The URL.

        Returns:
            The cached response, or None if not found.
        """
        if not self.enabled:
            return None
        
        cache_file = self._get_cache_file(url)
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, "rb") as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Failed to read cache file: {e}")
            return None

    def set(self, url: str, content: bytes) -> None:
        """
        Set a cached response for the given URL.

        Args:
            url: The URL.
            content: The response content.
        """
        if not self.enabled:
            return
        
        cache_file = self._get_cache_file(url)
        try:
            with open(cache_file, "wb") as f:
                f.write(content)
        except Exception as e:
            logger.warning(f"Failed to write cache file: {e}")

    def clear(self) -> None:
        """Clear the cache."""
        if not self.enabled or not self.cache_dir.exists():
            return
        
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
            logger.info(f"Cleared cache directory: {self.cache_dir}")
        except Exception as e:
            logger.warning(f"Failed to clear cache: {e}")

    def _get_cache_file(self, url: str) -> Path:
        """
        Get the cache file path for the given URL.

        Args:
            url: The URL.

        Returns:
            The cache file path.
        """
        # Create a hash of the URL to use as the filename
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.cache"
