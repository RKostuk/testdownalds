from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from testdownalds.utils.default_responses import api_bad_request_400, api_created_201
from .models import User
from .serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        request_data = request.data
        password: str = request_data['password']
        email: str = request_data['email']
        full_name: str | None = request_data.get('full_name')

        user, created = User.objects.get_or_create(email=email.lower())

        if not created:
            return api_bad_request_400({"error": 'User with this email already exists'})
        user.set_password(password)

        if full_name:
            user.full_name = full_name

        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return api_created_201({"auth_token": token.key, "user": self.serializer_class(user).data})