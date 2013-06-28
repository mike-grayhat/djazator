from django.conf import settings
from django.core.signing import Signer
from django.utils import importlib

_signer = Signer(getattr(settings, 'DJAZATOR_SALT', 'djazator_salt'))


def _default_singer(user):
    return _signer.sign(user.id)

try:
    path = settings.DJAZATOR_TOKENIZER
    module_name, sep, func_name = path.rpartition('.')
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    tokenize = func if callable(func) else _default_singer
except:
    tokenize = _default_singer
