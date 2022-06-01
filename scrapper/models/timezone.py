from django.db import models

from scrapper.models.utils.base import BaseModel
from scrapper.settings import APP_LABEL


class Timezone(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    name = models.CharField(max_length=200)
    value = models.FloatField()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, value={self.value})"

    __repr__ = __str__
