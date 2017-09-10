import http

from django.db import models
from django.utils import timezone


class Extraction(models.Model):
    STARTED = "started"
    TERMINATED = "terminated"
    CANCELLED = "cancelled"

    choices_status = (
        (STARTED, "Started"),
        (TERMINATED, "Terminated"),
        (CANCELLED, "Cancelled"),
    )

    url = models.URLField()
    start_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=16,
        choices=choices_status,
        default=STARTED
    )


class URLItem(models.Model):
    status_codes = [
        (c.value, c.phrase) for c in http.HTTPStatus
    ]

    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    url = models.URLField()
    full_url = models.URLField()
    status_code = models.PositiveSmallIntegerField(choices=status_codes)
