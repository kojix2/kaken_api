"""
Tests for utility functions.
"""

from kaken_api.utils import build_url, ensure_list, clean_text, parse_boolean, join_values


def test_build_url():
    """Test the build_url function."""
    # Test with parameters
    base_url = "https://example.com"
    params = {"key1": "value1", "key2": "value2"}
    url = build_url(base_url, params)
    assert "https://example.com?" in url
    assert "key1=value1" in url
    assert "key2=value2" in url
    
    # Test with None parameters (should be filtered out)
    params = {"key1": "value1", "key2": None}
    url = build_url(base_url, params)
    assert "https://example.com?" in url
    assert "key1=value1" in url
    assert "key2" not in url
    
    # Test with empty parameters
    url = build_url(base_url, {})
    assert url == "https://example.com"


def test_ensure_list():
    """Test the ensure_list function."""
    # Test with None
    assert ensure_list(None) == []
    
    # Test with list
    assert ensure_list([1, 2, 3]) == [1, 2, 3]
    
    # Test with single value
    assert ensure_list("test") == ["test"]
    assert ensure_list(123) == [123]


def test_clean_text():
    """Test the clean_text function."""
    # Test with None
    assert clean_text(None) is None
    
    # Test with empty string
    assert clean_text("") == ""
    
    # Test with whitespace
    assert clean_text("  test  ") == "test"
    
    # Test with multiple whitespace
    assert clean_text("test  test") == "test test"
    
    # Test with newlines
    assert clean_text("test\ntest") == "test test"
    assert clean_text("test\n\ntest") == "test test"


def test_parse_boolean():
    """Test the parse_boolean function."""
    # Test with None
    assert parse_boolean(None) is None
    
    # Test with boolean values
    assert parse_boolean(True) is True
    assert parse_boolean(False) is False
    
    # Test with string values
    assert parse_boolean("true") is True
    assert parse_boolean("True") is True
    assert parse_boolean("TRUE") is True
    assert parse_boolean("t") is True
    assert parse_boolean("yes") is True
    assert parse_boolean("y") is True
    assert parse_boolean("1") is True
    
    assert parse_boolean("false") is False
    assert parse_boolean("False") is False
    assert parse_boolean("FALSE") is False
    assert parse_boolean("f") is False
    assert parse_boolean("no") is False
    assert parse_boolean("n") is False
    assert parse_boolean("0") is False
    
    # Test with other values
    assert parse_boolean(1) is True
    assert parse_boolean(0) is False


def test_join_values():
    """Test the join_values function."""
    # Test with None
    assert join_values(None) is None
    
    # Test with empty list
    assert join_values([]) is None
    
    # Test with single value
    assert join_values(["test"]) == "test"
    
    # Test with multiple values
    assert join_values(["a", "b", "c"]) == "a,b,c"
    
    # Test with custom separator
    assert join_values(["a", "b", "c"], separator="|") == "a|b|c"
    
    # Test with None values in list
    assert join_values(["a", None, "c"]) == "a,c"
