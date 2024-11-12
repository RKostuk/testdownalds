from django.urls import path

from apps.service.views import UploadFileAPIView
from apps.users.views import UserRegisterAPIView

app_name = 'users_section'

urlpatterns = [
    path('create/', UserRegisterAPIView.as_view(), name='user_create'),
]
