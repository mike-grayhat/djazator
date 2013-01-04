from django.conf import settings
from django.utils import importlib

def _dumb(user):
    return user.id or "''"

try:
    path = settings.DJAZATOR_TOKENIZER
    module_name, sep, func_name = path.rpartition('.')
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    tokenize = func if callable(func) else _dumb
except:
    tokenize = _dumb
