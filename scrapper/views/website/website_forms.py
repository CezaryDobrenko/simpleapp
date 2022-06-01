import urllib.robotparser

import validators
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from scrapper.models.website import Website
from scrapper.views.basic_forms import BaseForm


def robots_validator(url):
    parsed_url = urllib.parse.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except:
        return True
    return rp.can_fetch("*", url)


class WebsiteCreateForm(BaseForm):
    class Meta:
        model = Website
        fields = ["url", "description", "is_ready", "is_simplified"]
        labels = {
            "url": _("Adres WWW strony:"),
            "description": _("Opis:"),
            "is_ready": _("Czy aktywnya"),
            "is_simplified": _(
                "Czy pobrane dane przetwarzać do formatu JSON (tryb zaawansowany)?"
            ),
        }

    def clean(self):
        errors = []
        if validators.url(self.data["url"]) is not True:
            errors.append("Wprowadzony adres www został zweryfikowany jako błędny")
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        website = Website(
            url=self.cleaned_data["url"],
            description=self.cleaned_data["description"],
            is_ready=self.cleaned_data["is_ready"],
            folder_id=self.cleaned_data["folder_id"],
            is_valid_with_robots=robots_validator(self.data["url"]),
        )
        website.save()


class WebsiteClearForm(BaseForm):
    class Meta:
        model = Website
        fields = []

    def save(self, commit=True):
        folder_id = self.cleaned_data["folder_id"]
        websites = Website.objects.filter(folder_id=folder_id)
        for website in websites:
            website.delete()


class WebsiteUpdateForm(BaseForm):
    class Meta:
        model = Website
        fields = ["url", "description", "is_ready", "is_simplified"]
        labels = {
            "url": _("Adres WWW strony:"),
            "description": _("Opis:"),
            "is_ready": _("Czy aktywna?"),
            "is_simplified": _(
                "Czy pobrane dane przetwarzać do formatu JSON (tryb zaawansowany)?"
            ),
        }

    def clean(self):
        errors = []
        if validators.url(self.data["url"]) is not True:
            errors.append("Wprowadzony adres www został zweryfikowany jako błędny")
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        website_id = self.test
        website = Website.objects.get(id=website_id)
        update_data = {}
        if "url" in self.data.keys():
            update_data["url"] = self.data["url"]
            update_data["is_valid_with_robots"] = robots_validator(self.data["url"])
        if "description" in self.data.keys():
            update_data["description"] = self.data["description"]
        if "is_ready" in self.data.keys():
            if self.data["is_ready"] == "on":
                update_data["is_ready"] = True
        else:
            update_data["is_ready"] = False
        if "is_simplified" in self.data.keys():
            if self.data["is_simplified"] == "on":
                update_data["is_simplified"] = True
        else:
            update_data["is_simplified"] = False
        website.update(**update_data)
        return HttpResponseRedirect(
            reverse("websites-settings", kwargs={"pk": website.folder.id})
        )
