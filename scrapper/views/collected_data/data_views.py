from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from scrapper.models.collected_data import CollectedData
from scrapper.models.selectors import Selector
from scrapper.models.user import User
from scrapper.translations.language_pl import Translator

from .data_forms import CollectedDataClearForm, CollectedDataUpdateForm


class CollectedDataList(LoginRequiredMixin, ListView):
    model = CollectedData
    template_name = "scrapper/collected_data/data_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        timezone_value = user.timezone.value
        selector_id = self.request.resolver_match.kwargs.get("pk")
        collected_data = []
        for element in CollectedData.objects.filter(selector_id=selector_id):
            element.created_date = Translator.scraping_date_to_pl(
                element.created_date + timedelta(hours=timezone_value)
            )
            collected_data.append(element)
        return collected_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selector_id = self.request.resolver_match.kwargs.get("pk")
        selector = Selector.objects.filter(id=selector_id).first()
        context["return_id"] = selector.website.id
        context["id"] = selector.id
        return context


class CollectedDataDelete(LoginRequiredMixin, DeleteView):
    model = CollectedData
    template_name = "scrapper/collected_data/data_delete.html"

    def get_success_url(self):
        data_id = self.kwargs["pk"]
        collected_data = CollectedData.objects.filter(id=data_id).first()
        return reverse("collected-data-list", kwargs={"pk": collected_data.selector.id})


class CollectedDataClear(LoginRequiredMixin, FormView):
    form_class = CollectedDataClearForm
    template_name = "scrapper/collected_data/data_clear.html"

    def form_valid(self, form):
        selector_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["selector_id"] = selector_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("collected-data-list", kwargs={"pk": self.kwargs["pk"]})


class CollectedDataUpdate(LoginRequiredMixin, UpdateView):
    model = CollectedData
    form_class = CollectedDataUpdateForm
    template_name = "scrapper/collected_data/data_update.html"

    def form_valid(self, form):
        selector_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["selector_id"] = selector_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        collected_data_id = self.kwargs["pk"]
        collected_data = CollectedData.objects.filter(id=collected_data_id).first()
        return reverse("collected-data-list", kwargs={"pk": collected_data.selector.id})
