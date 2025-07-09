from typing import Optional

from rest_framework import serializers, pagination

from apps.fleet.services.country_data_service import CountryDataService
from .models import Driver, Car

""" 
* Car Serializer
"""


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for the AddressDirectory model.
    """

    class Meta:
        """Meta class for CarSerializer."""

        model = Car
        fields = "__all__"


""" 
* Driver Serializer
"""


# * CREATE - UPDATE - DELETE
class DriverOperationsSerializer(serializers.ModelSerializer):
    """
    Serializer for Driver operations (CREATE, UPDATE, DELETE).
    """

    class Meta:
        """Meta class for DriverOperationsSerializer."""

        model = Driver
        fields = "__all__"


# * READ - LIST
class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for Driver read operations (READ, LIST).
    """

    car = CarSerializer()

    class Meta:
        """Meta class for DriverSerializer."""

        model = Driver
        fields = "__all__"


# * READ
class DriverLocationSerializer(DriverSerializer):
    """
    Serializer for Driver read operations (READ).
    """

    city_location = serializers.SerializerMethodField()  # Serializer method field to get the city location of the driver

    class Meta(DriverSerializer.Meta):
        """Meta class for DriverLocationSerializer."""

        fields = ["id", "car", "city_location", "name", "is_available"]

    def get_city_location(self, obj: Driver) -> Optional[str]:
        """
        Retrieves a random city for the driver's location.

        Args:
            obj: The Driver instance.

        Returns:
            A random city name as a string, or None if the service is not available or no city is found.
        """
        #! implementation only for testing and showcase purposes
        # * by default all drivers will be in Cundinamarca, Colombia.

        # Get the CountryDataService instance from the serializer context
        country_service: CountryDataService = self.context.get("country_data_service")

        if not country_service:
            print("Warning: CountryDataService not provided in serializer context.")
            return None

        city = country_service.get_random_city_in_a_state(country_name="Colombia", state="Cundinamarca Department")
        return city


class DefaultPagination(pagination.PageNumberPagination):
    """
    Default pagination class for listing resources.
    """

    page_size = 20
