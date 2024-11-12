from django.urls import path

from apps.service.views import UploadFileAPIView, AggregatedDataListAPIView

app_name = 'service_section'

urlpatterns = [
    path('upload-file/', UploadFileAPIView.as_view(), name='upload_file'),
    path('aggregate/<str:file_id>/', AggregatedDataListAPIView.as_view(), name='aggregate'),
]
