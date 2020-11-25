"""Utils for Autogen Subsystem."""
import functools

from .exceptions import JsonBadRequest


def get_client_ip(request):
    """
    Retrive client IP address from request.

    This function will retrive from HTTP_X_FORWARDED_FOR first,
    then REMOTE_ADDR.

    :param request: The Django request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def _check(keys, payload, pred, msg):
    for k in keys:
        if not pred(k, payload):
            raise JsonBadRequest(msg.format(k=k))


def _required(k, payload):
    return k in payload


def check_required(keys: list, payload: dict):
    return _check(keys, payload, _required, 'field `{k}` not found')


def check_nonempty(keys: list, payload: dict):
    return _check(keys, payload, _nonempty, 'field `{k}` should not be empty')


def _nonempty(k, payload):
    return len(payload.get(k, [])) != 0


def check_type(typ: type, keys: list, payload: dict):
    return _check(keys, payload, lambda x, d: isinstance(d[x], typ),
                  'field `{k}` type error')
