from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"user", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
