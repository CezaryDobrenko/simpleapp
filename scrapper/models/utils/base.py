import re

from django.db import models
from django.utils import timezone

from scrapper.models.utils.graphql_mixin import GrapheneMixin


def camel_to_snake(name: str) -> str:
    first_cap_re = re.compile("(.)([A-Z][a-z]+)")
    all_cap_re = re.compile("([a-z0-9])([A-Z])")
    s1 = first_cap_re.sub(r"\1_\2", name)
    return all_cap_re.sub(r"\1_\2", s1).lower()


class BaseModel(models.Model, GrapheneMixin):
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    __str__ = __repr__

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, camel_to_snake(key)):
                setattr(self, camel_to_snake(key), value)
        self.save()
