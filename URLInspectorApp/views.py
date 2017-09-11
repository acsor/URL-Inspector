from django.views.generic import TemplateView, DetailView, ListView

from .models import Extraction


class IndexView(ListView):
    template_name = "urlinspector/index.html"
    context_object_name = "extractions"

    def get_queryset(self):
        limit = 5

        return Extraction.objects.all().order_by("-start_date")[:limit]


class InspectionView(TemplateView):
    template_name = "urlinspector/inspection.html"
