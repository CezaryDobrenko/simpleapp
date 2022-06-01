from django.utils.translation import ugettext_lazy as _

from scrapper.models.collected_data import CollectedData
from scrapper.views.basic_forms import BaseForm


class CollectedDataClearForm(BaseForm):
    class Meta:
        model = CollectedData
        fields = []

    def save(self, commit=True):
        selector_id = self.cleaned_data["selector_id"]
        data = CollectedData.objects.filter(selector_id=selector_id)
        for item in data:
            item.delete()


class CollectedDataUpdateForm(BaseForm):
    class Meta:
        model = CollectedData
        fields = ["value"]
        labels = {
            "value": _("Wartość:"),
        }
