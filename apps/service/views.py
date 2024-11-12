from datetime import datetime

import pandas as pd
from django.db.models import Sum
from django.db.models.functions import TruncYear
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from testdownalds.utils.default_responses import api_bad_request_400, api_created_201
from apps.service.models import AdData, UploadedFile, LogsError
from apps.service.serializers import AggregatedDataSerializer
from apps.users.models import User


# Create your views here.


class UploadFileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        file = request.FILES.get('file')

        if not file:
            return api_bad_request_400({'error': 'No file provided.'})

        if not file.name.endswith('.csv') and not file.name.endswith('.xlsx'):
            return api_bad_request_400({'error': 'Invalid file format. Only .csv and .xlsx files are allowed.'})

        upload_file = UploadedFile.objects.create(user=request.user, file=file, status=UploadedFile.StatusChoices.PROCESSING)

        status_data = handle_uploaded_file(upload_file, file)
        if status_data:
            return api_created_201({"upload_file": upload_file.pk, "message": "File uploaded and processed successfully."})

        return api_bad_request_400({"error": LogsError.objects.filter(file=upload_file).last().error})


def handle_uploaded_file(upload_file: UploadedFile, file: UploadedFile.file) -> bool:
    #TODO: the best solution would be to put it in a task so as not to load the endpoint with file processing

    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    except Exception as e:
        upload_file.status = UploadedFile.StatusChoices.FAILED
        upload_file.save()
        LogsError.objects.create(user=upload_file.user,
                                 file=upload_file,
                                 error=f"Помилка при обробці файла - {e}")
        return False

    required_columns = AdData().list_columns_in_file
    if not all(col in df.columns for col in required_columns):
        upload_file.status = UploadedFile.StatusChoices.FAILED
        upload_file.save()
        LogsError.objects.create(user=upload_file.user,
                                 file=upload_file,
                                 error="Invalid file format. Required columns are missing.")
        return False

    ad_data_objects = []

    for _, row in df.iterrows():
        try:
            try:
                start_date = row.get('Start')
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
                end_date = row.get('End')
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            except Exception as e:
                LogsError.objects.create(user=upload_file.user,
                                         file=upload_file,
                                         error=f"Помилка з датами у файлі")
                return False

            ad_data = AdData(
                uploaded_file=upload_file,
                advertiser=row.get('Advertiser'),
                brand=row.get('Brand'),
                start=start_date,
                end=end_date,
                format=row.get('Format'),
                platform=row.get('Platform'),
                impressions=row.get('Impr'),
            )
            ad_data_objects.append(ad_data)

        except Exception as e:
            LogsError.objects.create(user=upload_file.user,
                                     file=upload_file,
                                     error=f"Помилка при обробці строки - {_} помилка - {e}")
            continue

    if ad_data_objects:
        AdData.objects.bulk_create(ad_data_objects)

    upload_file.status = UploadedFile.StatusChoices.DONE
    upload_file.save()
    return True


class AggregatedDataListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AggregatedDataSerializer

    def get_queryset(self):
        file_id = self.kwargs['file_id']

        file = get_object_or_404(UploadedFile, pk=file_id)

        if file.user != self.request.user:
            return api_bad_request_400({'error': 'You do not have permission to view this data.'})

        queryset = AdData.objects.filter(uploaded_file=file) \
            .annotate(year=TruncYear('end')) \
            .values('year') \
            .annotate(total_impressions=Sum('impressions')) \
            .order_by('year')

        return queryset