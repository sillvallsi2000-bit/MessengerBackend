from django.apps import AppConfig


class MessagesConfig(AppConfig):
    name = "apps.messages"

    def ready(self):
        import apps.messages.signals
