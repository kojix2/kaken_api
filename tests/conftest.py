"""
Pytest configuration file.
"""

import os
import pytest
from kaken_api import KakenApiClient


@pytest.fixture
def app_id():
    """
    Fixture that provides the application ID for the KAKEN API.
    
    The application ID is read from the KAKEN_APP_ID environment variable.
    If the environment variable is not set, the test will be skipped.
    """
    app_id = os.environ.get("KAKEN_APP_ID")
    if not app_id:
        pytest.skip("KAKEN_APP_ID environment variable is not set")
    return app_id


@pytest.fixture
def client(app_id):
    """
    Fixture that provides a KakenApiClient instance.
    
    The client is initialized with the application ID from the app_id fixture.
    The client is automatically closed after the test.
    """
    client = KakenApiClient(app_id=app_id)
    yield client
    client.close()
