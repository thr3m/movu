import logging
from typing import List

from django.conf import settings

from .base import CountriesApiClientABC
from lib.api_clients.base_http_client import BaseHttpClient

logger = logging.getLogger(__name__)


class CountriesNowClient(CountriesApiClientABC):
    """
    Concrete client for the CountriesNow.space API.
    """

    BASE_URL = settings.BASE_URL_COUNTRIES_NOW
    """The base URL for the CountriesNow.space API."""

    def __init__(self):
        """
        Initializes the CountriesNowClient with a BaseHttpClient instance.
        """
        self._http_client = BaseHttpClient(base_url=self.BASE_URL)

    def get_cities_of_country_states(self, country: str, state: str) -> List[str]:
        """
        Retrieves a list of cities for a given country and state.
        Endpoint: countries/state/cities/q

        Args:
            country: The name of the country.
            state: The name of the state.

        Returns:
            A list of city names.

        Raises:
            ValueError: If the API returns an error or no data.
            requests.exceptions.RequestException: If an error occurs during the HTTP request.
        """
        try:
            response = self._http_client.get("countries/state/cities/q", params={"country": country, "state": state})
            data = response.json()
            if data and data.get("error") is False and "data" in data:
                return data["data"]
            raise ValueError(f"API error or no data: {data}")
        except Exception as e:
            logger.exception(f"Error fetching cities for {state}, {country}: {e}")
            raise
