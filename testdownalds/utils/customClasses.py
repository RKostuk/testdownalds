# mypy: disable-error-code="union-attr, return-value, no-untyped-def, operator, arg-type, comparison-overlap"
from typing import Any, Optional, Union

from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from dynamic_preferences.registries import global_preferences_registry

from apps.users.models import User


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request: Optional[HttpRequest], **kwargs) -> Optional[User]:
        user: User | None = None
        full_name: str | None = kwargs.get('full_name')
        password: str | None = kwargs.get('password')
        if full_name and password:
            if '@' in full_name:
                try:
                    user = User.objects.get(email=full_name)
                except User.DoesNotExist:
                    ...
            else:
                try:
                    user = User.objects.get(full_name=full_name)
                except User.DoesNotExist:
                    ...

            if user is not None and user.check_password(password):
                return user

        return None

    def get_user(self, user_id: int) -> Union[User, Any]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


