from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from scrapper.gui_preview import GUIPreview
from scrapper.models.collected_data import CollectedData
from scrapper.models.selectors import Selector
from scrapper.models.website import Website

from .selectors_forms import (
    SelectorApproveForm,
    SelectorClearForm,
    SelectorCreateForm,
    SelectorCreateGUIForm,
    SelectorUpdateForm,
)


class SelectorsList(LoginRequiredMixin, ListView):
    model = Selector
    template_name = "scrapper/selector/selectors_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        website_id = self.request.resolver_match.kwargs.get("pk")
        selectors = []
        for selector in Selector.objects.filter(website_id=website_id):
            selector.type = selector.selector_type.name
            selector.data_count = CollectedData.objects.filter(
                selector_id=selector.id
            ).count()
            selectors.append(selector)
        return selectors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website_id = self.request.resolver_match.kwargs.get("pk")
        website = Website.objects.filter(id=website_id).first()
        context["return_id"] = website.folder.id
        context["website_id"] = website_id
        return context


class SelectorsApprove(LoginRequiredMixin, FormView):
    form_class = SelectorApproveForm
    template_name = "scrapper/selector/selectors_approve.html"

    def form_valid(self, form):
        website_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["website_id"] = website_id
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website_id = self.request.resolver_match.kwargs.get("pk")
        website = Website.objects.filter(id=website_id).first()
        selectors = Selector.objects.filter(website_id=website_id)
        website_data = {
            "id": website_id,
            "url": website.url,
            "description": website.description,
        }
        selectors_data = []
        for selector in selectors:
            selectors_data.append(
                {
                    "value": selector.value,
                    "desc": selector.description,
                    "type": selector.selector_type,
                }
            )
        context["website_data"] = website_data
        context["selectors_data"] = selectors_data
        return context

    def get_success_url(self):
        return reverse("folders")


class SelectorsDelete(LoginRequiredMixin, DeleteView):
    model = Selector
    template_name = "scrapper/selector/selectors_delete.html"

    def get_success_url(self):
        selector_id = self.kwargs["pk"]
        selector = Selector.objects.filter(id=selector_id).first()
        return reverse("selectors-list", kwargs={"pk": selector.website.id})


class SelectorsCreate(LoginRequiredMixin, FormView):
    form_class = SelectorCreateForm
    template_name = "scrapper/selector/selectors_add.html"

    def form_valid(self, form):
        website_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["website_id"] = website_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("selectors-list", kwargs={"pk": self.kwargs["pk"]})


class SelectorsCreateGUI(LoginRequiredMixin, FormView):
    form_class = SelectorCreateGUIForm
    template_name = "scrapper/selector/selectors_add_gui.html"

    def form_valid(self, form):
        website_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["website_id"] = website_id
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website_id = self.request.resolver_match.kwargs.get("pk")
        website = Website.objects.get(id=website_id)
        parsed_html = GUIPreview.get_preview(website.url)
        context["website_html"] = parsed_html
        return context

    def get_success_url(self):
        return reverse("selectors-list", kwargs={"pk": self.kwargs["pk"]})


class SelectorsClear(LoginRequiredMixin, FormView):
    form_class = SelectorClearForm
    template_name = "scrapper/selector/selectors_clear.html"

    def form_valid(self, form):
        website_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["website_id"] = website_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("selectors-list", kwargs={"pk": self.kwargs["pk"]})


class SelectorsUpdate(LoginRequiredMixin, UpdateView):
    model = Selector
    form_class = SelectorUpdateForm
    template_name = "scrapper/selector/selectors_update.html"

    def form_valid(self, form):
        website_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["website_id"] = website_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        selector_id = self.kwargs["pk"]
        selector = Selector.objects.filter(id=selector_id).first()
        return reverse("selectors-list", kwargs={"pk": selector.website.id})
