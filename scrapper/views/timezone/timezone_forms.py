from django.http import HttpResponseRedirect
from django.urls import reverse

from scrapper.models.timezone import Timezone
from scrapper.models.user import User
from scrapper.views.basic_forms import BaseForm


class ChangeTimezoneForm(BaseForm):
    class Meta:
        model = Timezone
        fields = []

    def save(self, id, commit=True):
        user = User.objects.get(id=id)
        user.timezone_id = self.data["timezone"]
        user.save()
        return HttpResponseRedirect(reverse("private_dashboard"))
