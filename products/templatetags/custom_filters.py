from django import template
from urllib.parse import quote_plus

register = template.Library()


@register.filter(name="encode_query_param")
def encode_query_param(value):
    """
    Encode the value to be used as a query parameter.
    As a user search term may contain characters that are not
    allowed in a URL query parameter.
    Also it encodes hex color, e.g. #FFFFFF to %23FFFFFF
    """
    return quote_plus(value)
