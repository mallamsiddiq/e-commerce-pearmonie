from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    
    def ready(self):
        # Import the signals to make sure they're registered
        import authapp.signals
