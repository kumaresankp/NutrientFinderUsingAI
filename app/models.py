from django.db import models
from django.contrib.auth.models import User

class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Store creation timestamp

    def __str__(self):
        return self.key[:10]


class UploadedFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add a ForeignKey to User
    image = models.ImageField(upload_to='uploads/')
    content = models.TextField(blank=True, null=True)  # To store AI response
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Food Image {self.id} - Uploaded on {self.uploaded_at}"