"""Bot application"""

from django.apps import AppConfig  # type: ignore


class BotConfig(AppConfig):  # type: ignore
    """Bot application"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
