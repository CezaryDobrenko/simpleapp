from django.db import models

from scrapper.models.user import User
from scrapper.models.utils.base import BaseModel
from scrapper.settings import APP_LABEL


class ApiKey(BaseModel):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name}, key={self.key})"
        )

    __repr__ = __str__
