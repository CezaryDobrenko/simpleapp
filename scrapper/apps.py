from django.apps import AppConfig


class scrapperConfig(AppConfig):
    name = "scrapper"

    def ready(self):
        import scrapper.signals  # noqa
