from http import HTTPStatus
from math import floor, ceil

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def http_code_phrase(code):
    """
    :param code: an HTTP status code (e.g. 200, 403, 404, ...).
    :return: a short name for an HTTP status code, or an empty string if no such code exists.
    """
    if code.isdigit():
        try:
            return HTTPStatus(int(code)).phrase
        except ValueError:
            pass

    return ""


@register.filter("http_code_desc")
@stringfilter
def http_code_description(code):
    """
    :param code: an HTTP status code (e.g. 200, 403, 404, ...).
    :return: a short description for an HTTP status code, or an empty string if no such code exists.
    """
    if code.isdigit():
        try:
            return HTTPStatus(int(code)).description
        except ValueError:
            pass

    return ""


@register.filter()
@stringfilter
def truncate_chars_middle(text, limit, sep="..."):
    """
    Truncates a given string **text** in the middle, so that **text** has length **limit** if it exceeds the number of
    characters, or else **len(text)** if it doesn't.
    Since this is a template filter, no exceptions are raised when they would normally do.

    :param text: the text to truncate.
    :param limit: the maximum length of **text**.
    :param sep: the separator to display in place of the (**len(text) - limit**) truncated characters.
    :return: a truncated version of **text**.
    """
    if not text or limit < 0:
        return ""

    length = len(text)

    if length < limit:
        return text
    else:
        first_half = ceil(limit / 2)
        second_half = length - floor(limit / 2)

        return text[:first_half] + sep + text[second_half:]
