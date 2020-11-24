from django.http import JsonResponse


class JsonBadRequest(Exception):
    status = 400

    def __init__(self, reason: str, payload: dict = None):
        payload = {} if payload is None else payload
        assert 'state' not in payload, 'duplicate key `state` in payload'
        payload.update({
            'state': 'error',
            'reason': reason
        })
        self.payload = payload

    @property
    def response(self):
        return JsonResponse(self.payload, status=self.status)


class KernelExecError(Exception):
    '''
    the execution exception caused by the custom code in Jupyter
    '''
    ...


class FileNotFound(Exception):
    ...
