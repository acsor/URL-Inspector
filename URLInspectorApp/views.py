from django.views.generic import TemplateView, DetailView, ListView

from .models import Extraction


global_context = {
    "length_url_max": 50,
    "length_url_min": 30,
}


class IndexView(ListView):
    template_name = "url_inspector/index.html"
    context_object_name = "extractions"

    def get_queryset(self):
        limit = 5

        return Extraction.objects.all().order_by("-start_date")[:limit]

    # TO-DO Remove definitions duplication of get_context_data() method in the classes below
    def get_context_data(self, **kwargs):
        super_context = super(IndexView, self).get_context_data(**kwargs)
        context = global_context.copy()

        context.update(super_context)

        return context


class InspectionView(DetailView):
    template_name = "url_inspector/inspection.html"
    context_object_name = "extraction"

    model = Extraction

    def get_context_data(self, **kwargs):
        super_context = super(InspectionView, self).get_context_data(**kwargs)
        context = global_context.copy()

        context.update(super_context)

        return context


class SavedInspectionsView(ListView):
    # TO-DO Add ordering by various fields, like date, name or number of scraped anchors
    template_name = "url_inspector/inspections_saved.html"
    context_object_name = "extractions"

    model = Extraction

    def get_context_data(self, **kwargs):
        super_context = super(SavedInspectionsView, self).get_context_data(**kwargs)
        context = global_context.copy()

        context.update(super_context)
        context["length_url_max"] = 100

        return context


class PreNewInspectionView(TemplateView):
    template_name = "url_inspector/pre_new_inspection.html"
