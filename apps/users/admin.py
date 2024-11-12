
from apps.users.models import User
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'email']
    search_fields = ['email', 'full_name']
