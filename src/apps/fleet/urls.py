from django.urls import path
from django.conf.urls import include

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"car", views.CarModelViewSet, basename="car")
router.register(r"driver", views.DriverModelViewSet, basename="driver")

app_name = "fleet"

urlpatterns = [
    path("admin/", include(router.urls)),
    path("driver/<uuid:pk>/location", views.DriverCityLocationRetrieveAPIView.as_view(), name="driver_detail_with_location"),
]
