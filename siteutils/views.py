'''
Views function utils
'''

from django.http import JsonResponse

from .exceptions import JsonBadRequest


def json_response(payload: dict = None) -> JsonResponse:
    payload = {} if payload is None else payload
    assert 'state' not in payload, 'duplicate key `state` in payload'
    payload.update({'state': 'ok'})
    return JsonResponse(payload)


def _check(keys, payload, pred, msg):
    for k in keys:
        if not pred(k, payload):
            raise JsonBadRequest(msg.format(k=k))


def _required(k, payload):
    return k in payload


def check_required(keys: list, payload: dict):
    return _check(keys, payload, _required, 'field `{k}` not found')


def _nonempty(k, payload):
    return len(payload.get(k, [])) != 0


def check_nonempty(keys: list, payload: dict):
    return _check(keys, payload, _nonempty, 'field `{k}` should not be empty')


def check_type(typ: type, keys: list, payload: dict):
    return _check(keys, payload, lambda x, d: isinstance(d[x], typ),
                  'field `{k}` type error')
