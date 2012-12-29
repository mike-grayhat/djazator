from django import template
from django.template import Context
from django.template.loader import get_template

from ..utils import unique_hash

register = template.Library()

@register.simple_tag(takes_context=True)
def realtime_token(context):
    request = context['request']
    try:
        return unique_hash(request.user)
    except:
        return ''
