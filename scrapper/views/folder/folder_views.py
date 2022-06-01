from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView, ListView, UpdateView

from scrapper.models.folder import Folder
from scrapper.models.user import User
from scrapper.models.utils.intervals import Interval
from scrapper.models.website import Website
from scrapper.translations.language_pl import Translator

from .folder_forms import FolderCreateForm, FolderUpdateForm


class FoldersList(LoginRequiredMixin, ListView):
    model = Folder
    template_name = "scrapper/folder/folders_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        folders = []
        user = User.objects.get(id=self.request.user.id)
        for folder in Folder.objects.filter(user_id=self.request.user.id):
            last_date = folder.last_scraping
            next_date = Interval.find_next_scraping_date(
                folder.last_scraping, folder.scraping_interval
            )
            if folder.last_scraping:
                timezone_value = user.timezone.value
                last_date = last_date + timedelta(hours=timezone_value)
                next_date = next_date + timedelta(hours=timezone_value)
            folder.sites = Website.objects.filter(folder_id=folder.id).count()
            folder.is_ready = Translator.is_ready_to_pl(folder.is_ready)
            folder.scraping_interval = Translator.interval_to_pl(
                folder.scraping_interval
            )
            folder.last_scraping = Translator.scraping_date_to_pl(last_date)
            folder.next_scraping = Translator.scraping_date_to_pl(next_date)
            folders.append(folder)
        return folders


class FoldersDelete(LoginRequiredMixin, DeleteView):
    model = Folder
    template_name = "scrapper/folder/folders_delete.html"
    success_url = reverse_lazy("folders")


class FolderCreate(LoginRequiredMixin, FormView):
    form_class = FolderCreateForm
    template_name = "scrapper/folder/folders_add.html"
    success_url = reverse_lazy("folders")

    def form_valid(self, form):
        form.cleaned_data["user_id"] = self.request.user.id
        form.save()
        return super().form_valid(form)


class FolderUpdate(LoginRequiredMixin, UpdateView):
    model = Folder
    form_class = FolderUpdateForm
    template_name = "scrapper/folder/folders_update.html"
    success_url = reverse_lazy("folders")

    def form_valid(self, form):
        folder_id = self.request.resolver_match.kwargs.get("pk")
        form.cleaned_data["user_id"] = self.request.user.id
        form.cleaned_data["folder_id"] = folder_id
        form.save()
        return super().form_valid(form)
