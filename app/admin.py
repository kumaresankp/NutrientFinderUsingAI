from django.contrib import admin
from .models import APIKey

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at')  # Add creation date to the list view
    search_fields = ('key',)
    list_filter = ('created_at',)  # Enable filtering by creation date

admin.site.register(APIKey, APIKeyAdmin)

