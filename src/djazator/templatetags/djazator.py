from django import template
from django.utils.safestring import mark_safe
from ..utils import tokenize

register = template.Library()

@register.simple_tag(takes_context=True)
def djazator_token(context):
    user = context['user']
    try:
        return tokenize(user)
    except:
        return False
