from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from scrapper.models.folder import Folder
from scrapper.models.selectors import Selector
from scrapper.models.website import Website
from scrapper.translations.language_pl import Translator

from .website_forms import WebsiteClearForm, WebsiteCreateForm, WebsiteUpdateForm


class WebsitesList(LoginRequiredMixin, ListView):
    model = Website
    template_name = "scrapper/website/webistes_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        folder_id = self.request.resolver_match.kwargs.get("pk")
        websites = []
        for website in Website.objects.filter(folder_id=folder_id):
            website.is_ready = Translator.is_ready_to_pl(website.is_ready)
            website.is_simplified = Translator.is_ready_to_pl(website.is_simplified)
            website.selectors = Selector.objects.filter(website_id=website.id).count()
            websites.append(website)
        return websites

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["folder_id"] = self.request.resolver_match.kwargs.get("pk")
        return context


class AllWebsitesList(LoginRequiredMixin, ListView):
    model = Website
    template_name = "scrapper/website/all_webistes_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        folders = Folder.objects.filter(user_id=self.request.user.id)
        websites = []
        for folder in folders:
            folder_websites = Website.objects.filter(folder_id=folder.id)
            for website in folder_websites:
                websites.append(website)
        return websites


class WebsitesDelete(LoginRequiredMixin, DeleteView):
    model = Website
    template_name = "scrapper/website/websites_delete.html"

    def get_success_url(self):
        website_id = self.kwargs["pk"]
        website = Website.objects.filter(id=website_id).first()
        return reverse("websites-settings", kwargs={"pk": website.folder.id})


class WebsitesClear(LoginRequiredMixin, FormView):
    form_class = WebsiteClearForm
    template_name = "scrapper/website/websites_clear.html"

    def form_valid(self, form):
        folder_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["folder_id"] = folder_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("websites-settings", kwargs={"pk": self.kwargs["pk"]})


class WebsiteCreate(LoginRequiredMixin, FormView):
    form_class = WebsiteCreateForm
    template_name = "scrapper/website/websites_add.html"

    def form_valid(self, form):
        folder_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["folder_id"] = folder_id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("websites-settings", kwargs={"pk": self.kwargs["pk"]})


class WebsiteUpdate(LoginRequiredMixin, UpdateView):
    model = Website
    form_class = WebsiteUpdateForm
    template_name = "scrapper/website/websites_update.html"

    def form_valid(self, form):
        id = self.request.resolver_match.kwargs.get("pk")
        form.test = id
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        website_id = self.kwargs["pk"]
        website = Website.objects.filter(id=website_id).first()
        return reverse("websites-settings", kwargs={"pk": website.folder.id})
