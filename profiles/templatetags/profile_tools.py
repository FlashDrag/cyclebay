import json
from django import template

register = template.Library()


@register.filter(name="json_loads")
def json_loads(value):
    return json.loads(value)
