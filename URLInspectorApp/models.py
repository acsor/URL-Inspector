import http
from urllib.parse import urlparse

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

    def __str__(self):
        return urlparse(self.url).netloc

    @staticmethod
    def urlitems_occurrences(items):
        o = dict()

        for i in items:
            o[i.status_code] = 1 + o.get(i.status_code, 0)

        return o


class URLItem(models.Model):
    status_codes = [
        (c.value, c.phrase) for c in http.HTTPStatus
    ]
    str_max_length = 50

    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    url = models.URLField()
    absolute_url = models.URLField()
    # TO-DO Handle missing HTTP status codes
    status_code = models.PositiveSmallIntegerField(choices=status_codes)

    def __str__(self):
        result = "%d %s" % (self.status_code, self.absolute_url)
        placeholder = " [...]" if len(result) > self.str_max_length else ""

        return result[:self.str_max_length] + placeholder
