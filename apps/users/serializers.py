
from rest_framework import serializers


from apps.users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'email', 'email', 'password',
        extra_kwargs = {"password": {"write_only": True}}
