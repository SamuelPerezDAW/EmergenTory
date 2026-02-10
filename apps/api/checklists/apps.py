from django.apps import AppConfig


class ChecklistsConfig(AppConfig):
    name = 'checklists'

    def ready(self):
        from . import signals  # noqa
