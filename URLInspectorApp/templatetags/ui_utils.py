from http import HTTPStatus

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter("http_code_phrase")
@stringfilter
def http_code_phrase(code):
    if code.isdigit():
        try:
            return HTTPStatus(int(code)).phrase
        except ValueError:
            pass

    return ""


@register.filter("http_code_desc")
@stringfilter
def http_code_description(code):
    if code.isdigit():
        try:
            return HTTPStatus(int(code)).description
        except ValueError:
            pass

    return ""
