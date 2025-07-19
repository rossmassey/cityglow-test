from django.apps import AppConfig


class CallsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.calls'

    def ready(self):
        """Initialize Firebase and Email service when Django app is ready."""
        try:
            from api.database import initialize_firebase
            initialize_firebase()
        except Exception as e:
            # Log the error but don't prevent Django from starting
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to initialize Firebase: {e}")
        
        try:
            from api.email_service import initialize_email
            initialize_email()
        except Exception as e:
            # Log the error but don't prevent Django from starting
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to initialize Email service: {e}")
