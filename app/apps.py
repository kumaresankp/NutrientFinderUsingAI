# apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'app'  # Replace with your app's name

    def ready(self):
        import app.signals  # Make sure this points to your signals.py file
