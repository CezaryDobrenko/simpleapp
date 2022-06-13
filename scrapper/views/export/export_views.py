import codecs
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView

from scrapper.export import Export
from scrapper.models.folder import Folder


class ExportList(LoginRequiredMixin, ListView):
    model = Folder
    template_name = "scrapper/export/export_list.html"
    paginate_by = 10
    ordering = ["pk"]

    def get_queryset(self):
        folders = []
        for folder in Folder.objects.filter(user_id=self.request.user.id):
            folders.append(folder)
        return folders


class ExportJSON(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        export = Export(pk)
        data = export.export_as_json()
        parsed_json_data = json.loads(data)
        response = JsonResponse(parsed_json_data)
        response["Content-Type"] = "text/html; charset=utf-8"
        response["Content-Disposition"] = 'attachment; filename="expoted_data.json"'
        return response


class ExportTXT(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        export = Export(pk)
        data = export.export_as_txt()
        response = HttpResponse(data)
        response["Content-Type"] = "text/html; charset=utf-8"
        response["Content-Disposition"] = 'attachment; filename="expoted_data.txt"'
        return response


class ExportXML(LoginRequiredMixin, View):
    def get(self, request, pk):
        export = Export(pk)
        data = export.export_as_xml()
        response = HttpResponse(data)
        response["Content-Type"] = "text/html; charset=utf-8"
        response["Content-Disposition"] = 'attachment; filename="expoted_data.xml"'
        return response


class ExportCSV(LoginRequiredMixin, View):
    def get(self, request, pk):
        export = Export(pk)
        data = export.export_as_csv()
        response = HttpResponse(data)
        response["Content-Type"] = "text/csv; charset=utf-8"
        response["Content-Disposition"] = 'attachment; filename="expoted_data.csv"'
        return response
