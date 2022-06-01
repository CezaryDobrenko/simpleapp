import json

from django import forms
from django.utils.translation import ugettext_lazy as _

from scrapper.models.selector_type import SelectorType
from scrapper.models.selectors import Selector
from scrapper.models.website import Website
from scrapper.views.basic_forms import BaseForm


class SelectorCreateForm(BaseForm):
    class Meta:
        model = Selector
        fields = ["value", "description", "selector_type"]
        labels = {
            "value": _("Nazwa selektora:"),
            "description": _("Opis:"),
            "selector_type": _("Typ selektora:"),
        }

    def save(self, commit=True):
        Selector.objects.get_or_create(
            value=self.cleaned_data["value"],
            description=self.cleaned_data["description"],
            website_id=self.cleaned_data["website_id"],
            selector_type_id=self.data["selector_type"],
        )


class SelectorCreateGUIForm(BaseForm):
    selectors = forms.CharField(
        label="Wybrane selektory", widget=forms.Textarea, required=False
    )
    paragraph = forms.BooleanField(
        label="Czy pobrać wszystkie dane paragrafów?", required=False
    )
    div = forms.BooleanField(
        label="Czy pobrać całą zawartość znaczników div?", required=False
    )
    section = forms.BooleanField(
        label="Czy pobrać wszystkie dane sekcji?", required=False
    )
    adress = forms.BooleanField(
        label="Czy pobrać wszystkie dane adresu?", required=False
    )
    article = forms.BooleanField(
        label="Czy pobrać wszystkie dane artykułów?", required=False
    )
    link = forms.BooleanField(
        label="Czy pobrać wszystkie dane odnośników?", required=False
    )
    img = forms.BooleanField(label="Czy pobrać wszystkie dane obrazów?", required=False)
    list = forms.BooleanField(label="Czy pobrać wszystkie dane list?", required=False)
    bold = forms.BooleanField(
        label="Czy pobrać wszystkie teksty pogrubione?", required=False
    )
    headline = forms.BooleanField(
        label="Czy pobrać wszystkie nagłówki?", required=False
    )
    table = forms.BooleanField(label="Czy pobrać wszystkie tabele?", required=False)

    class Meta:
        model = Selector
        fields = [
            "selectors",
            "paragraph",
            "div",
            "section",
            "adress",
            "article",
            "link",
            "list",
            "bold",
            "headline",
            "table",
        ]

    def save(self, commit=True):
        website_id = self.cleaned_data["website_id"]
        website = Website.objects.get(id=website_id)
        tag_type = SelectorType.objects.get(name="tag")
        class_type = SelectorType.objects.get(name="class")
        id_type = SelectorType.objects.get(name="id")

        if selectors := self.cleaned_data.get("selectors"):
            selectors_dict = json.loads(selectors)
            for selector in selectors_dict:
                key = self.get_first_key(selector)
                value = selector.get(key)
                if key == "class_name":
                    self.create_selector(
                        value,
                        "pobiera wartości wybranej grupy selektorów",
                        website.id,
                        class_type.id,
                    )
                if key == "id":
                    self.create_selector(
                        value,
                        "pobiera wartość wybranego selektoru",
                        website.id,
                        id_type.id,
                    )

        if self.cleaned_data.get("paragraph"):
            self.create_selector(
                "p", "pobiera całą zawartość paragrafów", website.id, tag_type.id
            )

        if self.cleaned_data.get("div"):
            self.create_selector(
                "div", "pobiera całą zawartość znaczników div", website.id, tag_type.id
            )

        if self.cleaned_data.get("section"):
            self.create_selector(
                "section", "pobiera wszystkie dane sekcji", website.id, tag_type.id
            )

        if self.cleaned_data.get("adress"):
            self.create_selector(
                "adress", "pobiera wszystkie dane adresu", website.id, tag_type.id
            )

        if self.cleaned_data.get("article"):
            self.create_selector(
                "article",
                "pobiera całą zawartość znaczników article",
                website.id,
                tag_type.id,
            )

        if self.cleaned_data.get("link"):
            self.create_selector(
                "a", "pobiera wszystkie dane odnośników", website.id, tag_type.id
            )

        if self.cleaned_data.get("list"):
            self.create_selector(
                "list", "pobiera wszystkie dane list", website.id, tag_type.id
            )

        if self.cleaned_data.get("bold"):
            self.create_selector(
                "b", "pobiera wszystkie teksty pogrubione", website.id, tag_type.id
            )

        if self.cleaned_data.get("headline"):
            self.create_selector(
                "headline", "pobiera wszystkie nagłówki", website.id, tag_type.id
            )

        if self.cleaned_data.get("table"):
            self.create_selector(
                "table", "pobiera wszystkie tabele", website.id, tag_type.id
            )

    def create_selector(self, value, description, website_id, type_id):
        Selector.objects.get_or_create(
            value=value,
            description=description,
            website_id=website_id,
            selector_type_id=type_id,
        )

    def get_first_key(self, dict):
        return list(dict.keys())[0]


class SelectorApproveForm(BaseForm):
    class Meta:
        model = Selector
        fields = []

    def save(self, commit=True):
        website_id = self.cleaned_data["website_id"]
        website = Website.objects.filter(id=website_id).first()
        website.is_ready = True
        website.save()


class SelectorClearForm(BaseForm):
    class Meta:
        model = Selector
        fields = []

    def save(self, commit=True):
        website_id = self.cleaned_data["website_id"]
        selectors = Selector.objects.filter(website_id=website_id)
        for selector in selectors:
            selector.delete()


class SelectorUpdateForm(BaseForm):
    class Meta:
        model = Selector
        fields = ["value", "description", "selector_type"]
        labels = {
            "value": _("Nazwa selektora:"),
            "description": _("Opis:"),
            "selector_type": _("Typ selektora:"),
        }
