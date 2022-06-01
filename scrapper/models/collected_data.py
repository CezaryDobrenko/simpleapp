from django.db import models

from scrapper.models.selectors import Selector
from scrapper.models.utils.base import BaseModel
from scrapper.settings import APP_LABEL


class CollectedData(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    value = models.TextField()
    selector = models.ForeignKey(to=Selector, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, value={self.value})"

    __repr__ = __str__
