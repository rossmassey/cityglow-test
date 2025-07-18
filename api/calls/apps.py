from django.apps import AppConfig


class CallsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.calls'

    def ready(self):
        """Initialize Firebase when Django app is ready."""
        try:
            from api.database import initialize_firebase
            initialize_firebase()
        except Exception as e:
            # Log the error but don't prevent Django from starting
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to initialize Firebase: {e}")
