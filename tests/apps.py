"""App configuration for test models."""

from django.apps import AppConfig


class TestsConfig(AppConfig):
    """App config for tests."""

    name = "tests"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """Register admin when the app is ready."""
        from . import admin  # noqa: F401
