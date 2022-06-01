from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from scrapper.models.collected_data import CollectedData
from scrapper.models.folder import Folder
from scrapper.models.selectors import Selector
from scrapper.models.user import User
from scrapper.models.website import Website


class DashboardView(TemplateView):
    template_name = "scrapper/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folders_count = 0
        websites_count = 0
        data_count = 0
        for folder in Folder.objects.all().all():
            folders_count += 1
            for website in Website.objects.filter(folder_id=folder.id).all():
                websites_count += 1
                for selector in Selector.objects.filter(website_id=website.id).all():
                    data_count += CollectedData.objects.filter(
                        selector_id=selector.id
                    ).count()

        context["folders_count"] = folders_count
        context["websites_count"] = websites_count
        context["data_count"] = data_count
        return context


class ProcessView(TemplateView):
    template_name = "scrapper/how_it_works.html"


class AnnouncementsView(TemplateView):
    template_name = "scrapper/announcements.html"


class MissionView(TemplateView):
    template_name = "scrapper/mission.html"


class SuccessView(TemplateView):
    template_name = "scrapper/success.html"


class PrivateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "scrapper/private_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        folders_count = 0
        websites_count = 0
        data_count = 0
        for folder in Folder.objects.filter(user_id=user_id).all():
            folders_count += 1
            for website in Website.objects.filter(folder_id=folder.id).all():
                websites_count += 1
                for selector in Selector.objects.filter(website_id=website.id).all():
                    data_count += CollectedData.objects.filter(
                        selector_id=selector.id
                    ).count()

        context["user"] = user
        context["join_date"] = user.date_joined.strftime("%d.%m.%Y")
        context["folders_count"] = folders_count
        context["websites_count"] = websites_count
        context["data_count"] = data_count
        context["timezone"] = user.timezone
        return context
