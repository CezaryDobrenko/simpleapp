from django import forms

from scrapper.translations.language_pl import Translator


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_to_translate = [
            "FolderUpdateForm",
            "FolderCreateForm",
            "ApiKeyCreateForm",
            "ApiKeyUpdateForm",
        ]
        form_name = self.__class__.__name__
        for visible in self.visible_fields():
            field_type = visible.field.widget.__class__.__name__
            if field_type == "Select" and form_name in form_to_translate:
                visible.field.choices = self.__select_translator_hander(visible.field)
                visible.field.widget.attrs["class"] = "form-control"
            if field_type == "SelectDateWidget" and form_name in form_to_translate:
                visible.field.widget.months = self.__select_date_translator_hander(
                    visible.field
                )
                visible.field.widget.attrs["class"] = "form-control"
            elif field_type == "CheckboxInput":
                visible.field.widget.attrs["class"] = "form-control-checkbox"
            else:
                visible.field.widget.attrs["class"] = "form-control"

    def __select_translator_hander(self, field):
        parsed_choices = []
        for item in field.choices:
            key, _ = item
            parsed_choices.append((key, Translator.interval_to_pl(key)))
        return parsed_choices

    def __select_date_translator_hander(self, field):
        parsed_months = {}
        for index in field.widget.months:
            month = field.widget.months.get(index)
            parsed_months[index] = Translator.month_to_pl(month)
        return parsed_months
