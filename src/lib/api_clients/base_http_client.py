import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger("apps")


class BaseHttpClient:
    """
    A base HTTP client for external API requests.
    """

    def __init__(self, base_url: str, default_headers: dict = None, timeout: int = 10):
        """
        Initializes the BaseHttpClient with a base URL, default headers, and timeout.

        Args:
            base_url: The base URL for API requests.
            default_headers: Optional dictionary of default headers to include in requests.
            timeout: Optional timeout in seconds for requests.
        """
        self._base_url = base_url
        self._headers = {"Accept": "application/json", **(default_headers or {})}
        self._timeout = timeout

    def _request(self, method: str, path: str, **kwargs):
        """
        Internal method to make HTTP requests.

        Args:
            method: The HTTP method (e.g., "GET", "POST").
            path: The path to append to the base URL.
            **kwargs: Additional keyword arguments to pass to requests.request.

        Returns:
            The requests.Response object if the request is successful.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.
        """
        url = urljoin(self._base_url, path)  # Combine base_url and path
        try:
            response = requests.request(method, url, timeout=self._timeout, **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            logger.exception(f"API request failed: {e}")
            raise  # Re-raise

    def get(self, path: str, params: dict = None, **kwargs):
        """
        Sends a GET request.

        Args:
            path: The path to append to the base URL.
            params: Optional dictionary of query parameters.
            **kwargs: Additional keyword arguments to pass to _request.

        Returns:
            The requests.Response object.
        """
        return self._request(method="GET", path=path, params=params, **kwargs)

    def post(self, path: str, json: dict = None, data: dict = None, **kwargs):
        """
        Sends a POST request.

        Args:
            path: The path to append to the base URL.
            json: Optional dictionary to send as JSON body.
            data: Optional dictionary to send as form data.
            **kwargs: Additional keyword arguments to pass to _request.

        Returns:
            The requests.Response object.
        """
        return self._request(method="POST", path=path, json=json, data=data, **kwargs)
