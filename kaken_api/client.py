"""
Main client for the KAKEN API.
"""

import logging
from typing import Optional

import requests

from .api.projects import ProjectsAPI
from .api.researchers import ResearchersAPI
from .exceptions import KakenApiError


logger = logging.getLogger(__name__)


class KakenApiClient:
    """
    Client for the KAKEN API.

    This client provides access to the KAKEN API, which allows searching for
    research projects and researchers funded by KAKEN (Grants-in-Aid for Scientific Research).

    Example:
        >>> from kaken_api import KakenApiClient
        >>> client = KakenApiClient(app_id="your_app_id")
        >>> projects = client.projects.search(keyword="人工知能")
        >>> for project in projects.projects:
        ...     print(project.title)
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        session: Optional[requests.Session] = None,
    ):
        """
        Initialize the KAKEN API client.

        Args:
            app_id: The application ID for the KAKEN API.
            timeout: The timeout for API requests in seconds.
            max_retries: The maximum number of retries for API requests.
            session: The requests session to use. If not provided, a new session will be created.
        """
        self.app_id = app_id
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = session or self._create_session()

        # Initialize API clients
        self.projects = ProjectsAPI(self.session, self.app_id)
        self.researchers = ResearchersAPI(self.session, self.app_id)

    def _create_session(self) -> requests.Session:
        """
        Create a new requests session.

        Returns:
            The requests session.
        """
        session = requests.Session()
        
        # Set default timeout
        session.request = lambda method, url, **kwargs: super(  # type: ignore
            requests.Session, session
        ).request(
            method=method, url=url, timeout=self.timeout, **kwargs
        )
        
        # Set retry strategy
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def close(self) -> None:
        """
        Close the client session.
        """
        if self.session:
            self.session.close()

    def __enter__(self):
        """
        Enter context manager.

        Returns:
            The client instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager.

        Args:
            exc_type: The exception type.
            exc_val: The exception value.
            exc_tb: The exception traceback.
        """
        self.close()
