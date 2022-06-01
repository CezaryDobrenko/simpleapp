from django.db import models

from scrapper.models.user import User
from scrapper.models.utils.base import BaseModel
from scrapper.models.utils.intervals import Interval
from scrapper.settings import APP_LABEL


class Folder(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    name = models.CharField(max_length=200)
    is_ready = models.BooleanField(default=False)
    scraping_interval = models.CharField(
        max_length=20, choices=Interval.Options.choices, default=Interval.Options.HOUR1
    )
    last_scraping = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def update_last_scraping(self, scrape_date):
        self.last_scraping = scrape_date
        self.save()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, is_ready={self.is_ready})"

    __repr__ = __str__
