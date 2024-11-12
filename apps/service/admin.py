from django.contrib import admin

from apps.service.models import UploadedFile, AdData, LogsError


# Register your models here.
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'user', 'uploaded_at', 'status']


@admin.register(AdData)
class AdDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertiser', 'brand', 'impressions', 'start', 'end')


@admin.register(LogsError)
class LogsErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'created_at')