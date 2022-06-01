import datetime
import uuid

from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from scrapper.models.api_key import ApiKey
from scrapper.views.basic_forms import BaseForm


class ApiKeyCreateForm(BaseForm):
    expired_time = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="Data wygaśnięcia:",
        initial=datetime.date.today,
    )

    class Meta:
        model = ApiKey
        fields = ["name"]
        labels = {
            "name": _("Nazwa:"),
        }

    def save(self, commit=True):
        key = ApiKey(
            name=self.cleaned_data["name"],
            key=uuid.uuid4().hex[:50],
            expired_at=self.cleaned_data["expired_time"],
            user_id=self.cleaned_data["user_id"],
        )
        key.save()


class ApiKeyClearForm(BaseForm):
    class Meta:
        model = ApiKey
        fields = []

    def save(self, commit=True):
        user_id = self.cleaned_data["user_id"]
        keys = ApiKey.objects.filter(user_id=user_id)
        for key in keys:
            key.delete()


class ApiKeyUpdateForm(BaseForm):
    expired_time = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="Data wygaśnięcia:",
        initial=datetime.date.today,
    )

    class Meta:
        model = ApiKey
        fields = ["name", "is_active"]
        labels = {
            "name": _("Nazwa"),
            "is_active": _("Czy aktywny?"),
        }

    def save(self, commit=True):
        key_id = self.cleaned_data["key_id"]
        expired_time = self.cleaned_data["expired_time"]
        key = ApiKey.objects.get(id=key_id)
        data = {}
        data["name"] = self.cleaned_data["name"]
        data["is_active"] = self.cleaned_data["is_active"]
        data["expired_at"] = expired_time
        key.update(**data)
        return HttpResponseRedirect(reverse("folders"))
