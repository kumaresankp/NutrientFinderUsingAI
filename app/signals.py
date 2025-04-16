# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UploadedFood
import json 
@receiver(post_save, sender=User)
def create_default_uploaded_food(sender, instance, created, **kwargs):
    if created:
        # Create a default record in UploadedFood for the new user
        UploadedFood.objects.create(
            user=instance,  # Link the uploaded food record to the new user
            image="uploads/lightgreenice.jpg",  # Default image path (ensure this image exists)
            content=json.dumps({
            "food_name": "Mint Ice Cream", 
            "fat": "10", 
            "protein": "2", 
            "carbohydrates": "20", 
            "calories": "180", 
            "additional_notes": "It contains mint extract or fresh mint leaves. The color is likely achieved through natural ingredients or food coloring."
        }), # Example nutritional info as JSON
        )
