from django.db import models

from scrapper.models.selector_type import SelectorType
from scrapper.models.utils.base import BaseModel
from scrapper.models.website import Website
from scrapper.settings import APP_LABEL


class Selector(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    value = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    website = models.ForeignKey(to=Website, on_delete=models.CASCADE, null=True)
    selector_type = models.ForeignKey(
        to=SelectorType, on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, value={self.value}, description={self.description})"

    __repr__ = __str__
