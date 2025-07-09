from django.contrib.auth.models import User

from rest_framework import serializers,pagination

from .models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'	

class UserPagination(pagination.PageNumberPagination):
    page_size = 20
    