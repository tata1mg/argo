
"""
This module provides a robust API client for making HTTP requests.

It includes retry functionality and configurable timeouts to handle
network instabilities and slow responses.
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



class APIClient:
    """
    A client for making API requests with built-in retry and timeout functionality.

    This class provides a wrapper around the requests library, adding automatic
    retries for failed requests and a configurable timeout. It uses a session
    object to allow for connection pooling and other performance optimizations.

    Attributes:
        timeout (int): The timeout in seconds for each request.
        max_retries (int): The maximum number of retries for failed requests.
        session (requests.Session): The session object used for making requests.

    Example:
        client = APIClient(timeout=10, max_retries=5)
        response = client.post('https://api.example.com/data', data={'key': 'value'})
    """

    def __init__(self, timeout: int = 5, max_retries: int = 3):
        self.timeout: int = timeout
        self.max_retries: int = max_retries
        self.session: requests.Session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(total=self.max_retries, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def post(self, url, data, headers: dict = None):
        return self.session.post(
            url, data=data, headers=headers, timeout=self.timeout
        )
