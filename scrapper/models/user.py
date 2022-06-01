from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from scrapper.models.timezone import Timezone
from scrapper.models.utils.graphql_mixin import GrapheneMixin
from scrapper.settings import APP_LABEL


class User(AbstractUser, GrapheneMixin):
    class Meta:
        app_label = APP_LABEL
        ordering = ("pk",)

    username = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True, blank=True)
    is_active = models.BooleanField(default=False)
    verification_pin = models.CharField(max_length=6)
    timezone = models.ForeignKey(
        to=Timezone, on_delete=models.SET_DEFAULT, default=3, null=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.email})"

    __repr__ = __str__
