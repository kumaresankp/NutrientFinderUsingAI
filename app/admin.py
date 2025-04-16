from django.contrib import admin
from .models import APIKey,UploadedFood

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at')  # Add creation date to the list view
    search_fields = ('key',)
    list_filter = ('created_at',)  # Enable filtering by creation date

# Customize the admin panel for the UploadedFood model
class UploadedFoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'uploaded_at', 'content')  # Show these fields in the list view
    search_fields = ('user__username',)  # Allow searching by the user's username
    list_filter = ('uploaded_at',)  # Add filtering by upload date
    readonly_fields = ('uploaded_at',)  # Make uploaded_at field read-only
    ordering = ('-uploaded_at',)  # Order by most recent upload

admin.site.register(APIKey, APIKeyAdmin)

admin.site.register(UploadedFood, UploadedFoodAdmin)