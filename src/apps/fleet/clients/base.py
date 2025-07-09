from abc import abstractmethod, ABC
from typing import List


class CountriesApiClientABC(ABC):
    """
    Abstract class for a client interacting with a Countries API.
    """

    @abstractmethod
    def get_cities_of_country_states(self, country: str, state: str) -> List[str]:
        """
        Abstract method to get a list of cities for a given country and state.

        Args:
            country: The name of the country.
            state: The name of the state.

        Returns:
            A list of city names.
        """
        pass
