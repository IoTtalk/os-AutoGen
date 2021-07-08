"""Django View for Autogen Subsystem."""
import json
import requests

from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import ccmapi.v0 as api

from ccmapi.exceptions import CCMAPIError

from .device import devicehandler
from .exceptions import JsonBadRequest
from .models import Device
from .utils import rgetattr, check_required, check_nonempty, check_type


def json_response(payload: dict = None) -> JsonResponse:
    payload = {} if payload is None else payload
    assert 'state' not in payload, 'duplicate key `state` in payload'
    payload.update({'state': 'ok'})
    return JsonResponse(payload)


@csrf_exempt
@require_http_methods(['POST'])
def create_device(request):
    """
    Create a new AutoGen device or update an existing device.

    :post.data code: The SA code for IoTtalk.
                     AutoGen will run this code as your device.
    :post.data version: Optional: 1 or 2, default: 2. This value is used to run
                        different iottalk dan libraries. Depends on the device
                        the user wants to create.

    :response token: The token of the device has been created.
                     Used to delete this device.
    """
    payload = request.json
    payload.setdefault('version', 2)
    payload.setdefault('token', str(uuid4()))

    check_required(['code'], payload)
    check_nonempty(['code', 'token'], payload)
    check_type(int, ['version'], payload)

    dev = Device.objects.create(
        code=payload['code'],
        token=payload['token'],
        version=payload['version'])

    return json_response({
        'timestamp': datetime.now().timestamp(),
        'token': devicehandler.create_device(dev),
    })


@csrf_exempt
@require_http_methods(['POST'])
def delete_device(request):
    """
    Stop a existing AutoGen device.

    :post.data token: The token of the device to be stopped.
                      It is given by create API.
    """
    payload = request.json
    check_required(['token'], payload)
    token = payload.get('token', None)
    dev = get_object_or_404(Device, token=token)
    token = devicehandler.delete_device(dev)
    dev.delete()
    return json_response({
        'timestamp': datetime.now().timestamp(),
        'token': token,
    })


@csrf_exempt
@require_http_methods(['POST'])
def ccm_api(request):
    """
    CCM API.

    :post.data api_name: IoTtalk v1/v2 CCM API name.
    :post.data payload:  IoTtalk v1/v2 CCM API payload.
    :post.data username: Optional, IoTtalk v2 username.
    :post.data password: Optional, IoTtalk v2 password.
    TODO: username/password should use access token instead
    """
    payload = request.json
    check_required(['api_name', 'payload'], payload)
    username = payload.get('username', None)
    password = payload.get('password', None)
    session_id = payload.get('session_id', None)
    api_name = payload.get('api_name')

    api_args = settings.CCM_API_ARGS
    if api_name not in api_args:
        raise JsonBadRequest(f'api_name {api_name} not found')

    try:
        api_payload = payload.get('payload')
        # extract args from payload
        args = [api_payload.pop(k) for k in api_args.get(api_name, [])]

        # get api function from library ccmapi
        f = rgetattr(api, api_name)

        # login user for v2
        s = requests.Session()
        if username and password:
            u_id, cookie = api.account.login(username, password, session=s)
        elif session_id:
            s.cookies.update({'session_id': session_id})

        # assign logined session to invoke api
        api_payload.update({'session': s})

        result = f(*args, **api_payload)

    except AttributeError as e:
        raise JsonBadRequest(str(e))
    except KeyError as e:
        raise JsonBadRequest(f'{e} in the payload is required')
    except CCMAPIError as e:
        err = JsonBadRequest(json.dumps(e.msg))
        err.status = e.status_code
        raise err
    except requests.exceptions.ConnectionError:
        raise JsonBadRequest('Connection error, '
                              'please check that the IoTtalk Server ("api_url") '
                              'can be connected normally.')

    if 'account.login' == api_name:
        return json_response({'result': {'u_id': result[0]}})
    return json_response({'result': result})
