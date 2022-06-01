from django.db import models

from scrapper.models.folder import Folder
from scrapper.models.utils.base import BaseModel
from scrapper.settings import APP_LABEL


class Website(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    url = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    is_ready = models.BooleanField(default=False)
    is_simplified = models.BooleanField(default=False)
    is_new_data_collected = models.BooleanField(default=False)
    is_valid_with_robots = models.BooleanField(default=True)
    folder = models.ForeignKey(to=Folder, on_delete=models.CASCADE, null=True)

    def update_is_new_data_collected(self, is_collected):
        self.is_new_data_collected = is_collected
        self.save()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.url}, is_ready={self.is_ready})"

    __repr__ = __str__
