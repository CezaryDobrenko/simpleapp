from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from scrapper.models.api_key import ApiKey
from scrapper.translations.language_pl import Translator

from .api_forms import ApiKeyClearForm, ApiKeyCreateForm, ApiKeyUpdateForm


class ApiKeyList(LoginRequiredMixin, ListView):
    model = ApiKey
    template_name = "scrapper/api_keys/api_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        result = []
        for api_key in ApiKey.objects.filter(user_id=self.request.user.id):
            api_key.is_active = Translator.is_ready_to_pl(api_key.is_active)
            api_key.expired_at = Translator.expired_date_to_pl(api_key.expired_at)
            result.append(api_key)
        return result


class ApiKeyDelete(LoginRequiredMixin, DeleteView):
    model = ApiKey
    template_name = "scrapper/api_keys/api_delete.html"
    success_url = reverse_lazy("api-key-list")


class ApiKeyClear(LoginRequiredMixin, FormView):
    form_class = ApiKeyClearForm
    template_name = "scrapper/api_keys/api_clear.html"
    success_url = reverse_lazy("api-key-list")

    def form_valid(self, form):
        form.cleaned_data["user_id"] = self.request.user.id
        form.save()
        return super().form_valid(form)


class ApiKeyCreate(LoginRequiredMixin, FormView):
    form_class = ApiKeyCreateForm
    template_name = "scrapper/api_keys/api_add.html"
    success_url = reverse_lazy("api-key-list")

    def form_valid(self, form):
        form.cleaned_data["user_id"] = self.request.user.id
        form.save()
        return super().form_valid(form)


class ApiKeyUpdate(LoginRequiredMixin, UpdateView):
    model = ApiKey
    form_class = ApiKeyUpdateForm
    template_name = "scrapper/api_keys/api_update.html"
    success_url = reverse_lazy("api-key-list")

    def form_valid(self, form):
        key_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["key_id"] = key_id
        form.save()
        return super().form_valid(form)
