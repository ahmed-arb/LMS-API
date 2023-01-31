"""Core config of LMS"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """This class defines core app configs"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        """Sets up imports and pre-requisites for this app"""
        import core.signals
