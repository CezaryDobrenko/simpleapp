from django.db import models

from scrapper.models.utils.base import BaseModel
from scrapper.settings import APP_LABEL


class SelectorType(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.name} ({self.description})"

    __repr__ = __str__
