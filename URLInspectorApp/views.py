from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from scrapyd_api import ScrapydAPI

from .models import Extraction
from .settings import conf_scrapyd

global_context = {
    "length_url_max": 50,
    "length_url_min": 30,
    "inspection_refresh": 7,    # Seconds to wait before an incomplete inspection's page is refreshed
}


class IndexView(ListView):
    template_name = "url_inspector/index.html"
    context_object_name = "extractions"

    def get_queryset(self):
        limit = 5

        return Extraction.objects.all().order_by("-start_date")[:limit]

    # TO-DO Remove definition duplicates of the get_context_data() method in the classes below
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
        context["items"] = context["extraction"].urlitem_set.all()
        context["occurrences"] = Extraction.urlitems_occurrences(context["items"])

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

        return context


class PreNewInspectionView(TemplateView):
    template_name = "url_inspector/pre_new_inspection.html"


def inspection_new(request: HttpRequest):
    url, extraction = None, None
    form_url = "scraping_url"
    scrapyc = ScrapydAPI(
        conf_scrapyd["target"]
    )

    if form_url not in request.GET:
        # TO-DO Implement proper handling
        pass
    else:
        url = request.GET[form_url]
        extraction = Extraction(url=url)

        extraction.save()

        try:
            scrapyc.schedule(
                conf_scrapyd["project"],
                conf_scrapyd["spider"],
                urls=url,
                django_urls=(url,),
                django_ids=(extraction.id,)
            )
        # TO-DO Catch possible exceptions here
        finally:
            pass

    return HttpResponseRedirect(
        reverse("url_inspector:inspection", kwargs={"pk": extraction.id})
    )
