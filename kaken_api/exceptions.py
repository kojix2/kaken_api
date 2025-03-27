"""
Exceptions for the KAKEN API client.
"""


class KakenApiError(Exception):
    """Base exception for all KAKEN API errors."""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class KakenApiRequestError(KakenApiError):
    """Exception raised when there is an error with the request."""

    pass


class KakenApiResponseError(KakenApiError):
    """Exception raised when there is an error with the response."""

    pass


class KakenApiAuthError(KakenApiError):
    """Exception raised when there is an authentication error."""

    pass


class KakenApiRateLimitError(KakenApiError):
    """Exception raised when the API rate limit is exceeded."""

    pass


class KakenApiNotFoundError(KakenApiError):
    """Exception raised when a resource is not found."""

    pass
