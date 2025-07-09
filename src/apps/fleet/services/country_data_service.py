import random
import logging
from typing import Optional

from requests.exceptions import HTTPError

from apps.fleet.clients.base import CountriesApiClientABC
from lib.email.utils import send_text_email

logger = logging.getLogger(__name__)


class CountryDataService:
    """
    Service to provide country and city-related data,
    """

    #! implementation only for testing and showcase purposes

    def __init__(self, countries_api_client: CountriesApiClientABC):
        """
        Initializes the CountryDataService with a CountriesApiClientABC instance.

        Args:
            countries_api_client: An instance of a class implementing CountriesApiClientABC.
        """
        self.countries_api_client = countries_api_client  # Dependency Injection

    def get_random_city_in_a_state(self, country_name: str, state: str) -> Optional[str]:
        """
        Retrieves a random city from the given country and state using the configured API client.

        Args:
            country_name: The name of the country.
            state: The name of the state.

        Returns:
            A random city name as a string, or None if an error occurs or no cities are found.

        Raises:
            Exception: Propagates exceptions from the underlying API client or if no cities are returned.
        """
        try:
            cities = self.countries_api_client.get_cities_of_country_states(country=country_name, state=state)
            if not cities:
                logger.warning(f"No cities found for {state}, {country_name}")
                return None
            city = random.choice(cities)
            return city
        except HTTPError as e:
            #! implementation only for testing and showcase purposes
            error_message = f"Failed to get cities for {state}, {country_name} from CountriesNow API. Error: {e}"
            logger.exception(error_message)
            send_text_email(subject="CountriesNow API Error", message=error_message, recipient_list=["foobar@outlook.com"])
            return None
        except Exception as e:
            logger.exception(f"Service error getting random city for {state}, {country_name}: {e}")
            return None
