from django.db import models

from apps.users.models import User


# Create your models here.

class UploadedFile(models.Model):
    class StatusChoices(models.TextChoices):
        PROCESSING = 'Processing', 'Процес завантаження'
        DONE = 'Done', 'Успішно завантажено'
        FAILED = 'Failed', 'Помилка завантаження'

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='media/uploads/')
    status = models.CharField(max_length=255, choices=StatusChoices, default=StatusChoices.PROCESSING) # Choise add
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file.name}'

    class Meta:
        verbose_name = 'Завантажений файл'
        verbose_name_plural = 'Завантажені файли'


class AdData(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    advertiser = models.CharField(max_length=255, null=True, verbose_name='Рекламодавець')
    brand = models.CharField(max_length=100, null=True, verbose_name='Бренд')
    format = models.CharField(max_length=20, null=True, verbose_name='Формат')
    platform = models.CharField(max_length=50, null=True, verbose_name='Платформа')
    impressions = models.FloatField(null=True, verbose_name='Кількість показів')
    start = models.DateField(null=True, verbose_name='Дата початку')
    end = models.DateField(null=True, verbose_name='Дата закінчення')

    @property
    def list_columns_in_file(self):
        return ['Advertiser', 'Brand', 'Start', 'End', 'Format', 'Platform', 'Impr']

    def __str__(self):
        return f'{self.advertiser} - {self.brand}'

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламні дані'


class LogsError(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    error = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.error}'

    class Meta:
        verbose_name = 'Помилка'
        verbose_name_plural = 'Помилки'
