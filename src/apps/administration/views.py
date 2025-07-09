import logging

from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer, UserPagination
from .models import User

logger = logging.getLogger(__name__)


@extend_schema(tags=["User Administration"])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [AllowAny]
    ordering = ["-date_joined"]
