"""
Utility functions for the KAKEN API client.
"""

import re
import urllib.parse
from typing import Dict, List, Optional, Union, Any


def build_url(base_url: str, params: Dict[str, Any]) -> str:
    """
    Build a URL with query parameters.

    Args:
        base_url: The base URL.
        params: The query parameters.

    Returns:
        The URL with query parameters.
    """
    # Filter out None values
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    # URL encode parameters
    encoded_params = urllib.parse.urlencode(filtered_params, doseq=True)
    
    # Combine base URL and parameters
    if encoded_params:
        return f"{base_url}?{encoded_params}"
    return base_url


def ensure_list(value: Union[List, Any]) -> List:
    """
    Ensure that a value is a list.

    Args:
        value: The value to ensure is a list.

    Returns:
        The value as a list.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean_text(text: Optional[str]) -> Optional[str]:
    """
    Clean text by removing extra whitespace.

    Args:
        text: The text to clean.

    Returns:
        The cleaned text.
    """
    if text is None:
        return None
    return re.sub(r'\s+', ' ', text).strip()


def parse_boolean(value: Union[str, bool, None]) -> Optional[bool]:
    """
    Parse a boolean value from a string.

    Args:
        value: The value to parse.

    Returns:
        The parsed boolean value.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', 't', 'yes', 'y', '1')
    return bool(value)


def join_values(values: List[str], separator: str = ",") -> Optional[str]:
    """
    Join a list of values into a string.

    Args:
        values: The values to join.
        separator: The separator to use.

    Returns:
        The joined string.
    """
    if not values:
        return None
    return separator.join(str(v) for v in values if v is not None)
