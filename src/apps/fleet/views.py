import logging

from rest_framework.permissions import AllowAny
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from .helpers.viewmixin import MultiSerializerViewSetMixin
from .serializers import CarSerializer, DriverSerializer, DefaultPagination, DriverOperationsSerializer, DriverLocationSerializer
from .models import Car, Driver

from apps.fleet.services.country_data_service import CountryDataService
from apps.fleet.clients.countries_now_client import CountriesNowClient

logger = logging.getLogger(__name__)


@extend_schema(tags=["Admin Car"])
class CarModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Car instances.
    """

    queryset = Car.objects.all()
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination
    serializer_class = CarSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


@extend_schema(tags=["Admin Driver"])
class DriverModelViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing Driver instances.
    """

    queryset = Driver.objects.all()
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    serializers = {
        "default": DriverOperationsSerializer,
        "list": DriverSerializer,
        "retrieve": DriverSerializer,
    }


@extend_schema(tags=["Driver"])
class DriverCityLocationRetrieveAPIView(generics.RetrieveAPIView):
    """
    ViewSet for check the city location of a driver
    """

    queryset = Driver.objects.all()
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    serializer_class = DriverLocationSerializer

    def get_serializer_context(self):
        """
        Extends the default serializer context to include an instance of CountryDataService.
        This allows the `DriverLocationSerializer` to access the service for fetching city data.
        """
        #! implementation only for testing and showcase purposes
        context = super().get_serializer_context()
        country_service = CountryDataService(countries_api_client=CountriesNowClient())
        context["country_data_service"] = country_service
        return context

    def get_object(self):
        """
        Retrieves the Driver object based on the URL lookup field.

        Raises:
            NotFound: If the driver with the given ID is not found, with a custom error message.

        Returns:
            The Driver object.
        """
        try:
            obj = super().get_object()
        except NotFound:
            raise NotFound(detail="The requested driver with this ID was not found in our system. Please verify the ID and try again.")
        return obj
