from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from scrapper.models.timezone import Timezone
from scrapper.models.user import User

from .timezone_forms import ChangeTimezoneForm


class ChangeTimezone(LoginRequiredMixin, FormView):
    form_class = ChangeTimezoneForm
    template_name = "scrapper/timezone/change_timezone.html"
    success_url = reverse_lazy("private_dashboard")

    def form_valid(self, form):
        id = self.request.resolver_match.kwargs.get("pk")
        form.save(id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        timezones = Timezone.objects.all()
        context["timezones"] = timezones
        context["current_timezone"] = user.timezone
        return context
