import uuid
from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from apps.fleet.models import Driver, Car
from apps.fleet.helpers import faker


# Fixture to create a Driver instance
@pytest.fixture(scope="function")
def driver_instance(db):
    """
    Pytest fixture to create and return a Driver instance with an associated Car.
    The 'db' fixture ensures database access.
    """
    car_obj = Car.objects.create(**faker.fake_car())
    return Driver.objects.create(**faker.fake_driver(car=car_obj))


@pytest.fixture(scope="session")
def api_client():
    """
    Pytest fixture to provide an APIClient instance for making HTTP requests in tests.
    """
    return APIClient()


@pytest.mark.django_db
class TestDriverCityLocationRetrieveAPIView:
    """
    Test suite for the DriverCityLocationRetrieveAPIView.
    Ensures the API endpoint correctly retrieves driver city locations.
    """
    @patch("apps.fleet.services.country_data_service.CountryDataService.get_random_city_in_a_state")
    def test_successful_response(self, mock_get_random_city, api_client, driver_instance):
        """
        Tests that the API returns a successful response with the correct city location.
        Mocks the external country data service to control the returned city.
        """
        mock_get_random_city.return_value = "Bogota"
        url = reverse("fleet:driver_detail_with_location", kwargs={"pk": driver_instance.id})

        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data.get("city_location") == "Bogota"
        mock_get_random_city.assert_called_once_with(country_name='Colombia', state='Cundinamarca Department')

    @patch("apps.fleet.services.country_data_service.CountryDataService.get_random_city_in_a_state")
    def test_external_api_error_returns_none(self, mock_get_random_city, api_client, driver_instance):
        """
        Tests that if the external API returns None (e.g., due to an error or no data),
        the city_location field in the response is also None.
        """
        mock_get_random_city.return_value = None
        url = reverse("fleet:driver_detail_with_location", kwargs={"pk": driver_instance.id})

        response = api_client.get(url)

        assert response.data.get("city_location") == None

        mock_get_random_city.assert_called_once_with(country_name='Colombia', state='Cundinamarca Department')

    @patch("apps.fleet.services.country_data_service.CountryDataService.get_random_city_in_a_state")
    def test_error_404_response(self, mock_get_random_city, api_client, driver_instance):
        """
        Tests that requesting a non-existent driver ID returns a 404 Not Found response
        with a custom error message, and the external API is not called.
        """
        mock_get_random_city.return_value = None
        url = reverse("fleet:driver_detail_with_location", kwargs={"pk": uuid.uuid4()})

        response = api_client.get(url)

        assert response.status_code == 404
        assert response.data.get("detail") == "The requested driver with this ID was not found in our system. Please verify the ID and try again."

        mock_get_random_city.assert_not_called()
