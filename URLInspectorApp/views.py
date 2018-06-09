from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView, DeleteView
from scrapyd_api import ScrapydAPI

from .models import Extraction
from .settings import conf_scrapyd

template_root = "url_inspector"


class IndexView(ListView):
    template_name = template_root + "/index.html"
    context_object_name = "extractions"

    def get_queryset(self):
        limit = 5

        return Extraction.objects.all().order_by("-start_date")[:limit]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["extractions_count"] = Extraction.objects.count()

        return context


class InspectionView(DetailView):
    template_name = template_root + "/inspection.html"
    context_object_name = "extraction"

    model = Extraction

    def get_context_data(self, **kwargs):
        super_context = super(InspectionView, self).get_context_data(**kwargs)
        super_context["items"] = super_context["extraction"].urlitem_set.all()
        super_context["occurrences"] = Extraction.urlitems_occurrences(super_context["items"])

        return super_context


class SavedInspectionsView(ListView):
    # TO-DO Add ordering by various fields, like date, name or number of scraped anchors
    template_name = template_root + "/inspections_saved.html"
    context_object_name = "extractions"

    model = Extraction


class PreNewInspectionView(TemplateView):
    template_name = template_root + "/pre_new_inspection.html"


def inspection_new(request: HttpRequest):
    # TO-DO Use Django's form validation
    url, extraction = None, None
    form_url = "scraping_url"
    scrapyc = ScrapydAPI(
        conf_scrapyd["target"]
    )

    if form_url not in request.GET:
        return HttpResponseRedirect(
            reverse("url_inspector:error_new_inspection")
        )
    else:
        url = request.GET[form_url]

        try:
            URLValidator()(url)
        except ValidationError:
            return HttpResponseRedirect(
                reverse("url_inspector:error_new_inspection")
            )

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
        except Exception as e:
            return HttpResponseRedirect(
                reverse("url_inspector:error_new_inspection")
            )

    return HttpResponseRedirect(
        reverse("url_inspector:inspection", kwargs={"pk": extraction.id})
    )


class ErrorNewInspection(TemplateView):
    template_name = template_root + "/error_new_inspection.html"


class InspectionDelete(DeleteView):
    model = Extraction
    context_object_name = "extraction"
    template_name = template_root + "/inspection_confirm_delete.html"

    success_url = reverse_lazy("url_inspector:inspections_saved")


