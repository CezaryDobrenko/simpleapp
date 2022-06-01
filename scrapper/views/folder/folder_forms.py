from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from scrapper.models.folder import Folder
from scrapper.views.basic_forms import BaseForm


class FolderCreateForm(BaseForm):
    class Meta:
        model = Folder
        fields = ["name", "is_ready", "scraping_interval"]
        labels = {
            "name": _("Nazwa folderu:"),
            "is_ready": _("Czy aktywny?"),
            "scraping_interval": _("Okresy pobierania danych"),
        }

    def save(self, commit=True):
        folder = Folder(
            name=self.cleaned_data["name"],
            is_ready=self.cleaned_data["is_ready"],
            scraping_interval=self.cleaned_data["scraping_interval"],
            user_id=self.cleaned_data["user_id"],
        )
        folder.save()


class FolderUpdateForm(BaseForm):
    class Meta:
        model = Folder
        fields = ["name", "is_ready", "scraping_interval"]
        labels = {
            "name": _("Nazwa folderu:"),
            "is_ready": _("Czy aktywny?"),
            "scraping_interval": _("Okresy pobierania danych"),
        }

    def save(self, commit=True):
        folder_id = self.cleaned_data.get("folder_id")
        folder = Folder.objects.filter(id=folder_id).first()
        for changed_field in self.changed_data:
            if changed_field in ["is_ready", "scraping_interval"]:
                self.cleaned_data["last_scraping"] = None
        folder.update(**self.cleaned_data)
        folder.save()
        return HttpResponseRedirect(reverse("folders"))
