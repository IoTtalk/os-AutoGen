"""Django View for Autogen Subsystem."""
import json
import requests

from uuid import uuid4

# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


import ccmapi.v0 as api

from ccmapi.exceptions import CCMAPIError

from .config import ccm_api_args, ccm_api_url
from .device import devicehandler
from .models import Device
from .utils import rgetattr

api.config.api_url = ccm_api_url


def index(request):
    """Index page, useless."""
    return HttpResponse("404")


@csrf_exempt
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
    if request.method != 'POST':
        return HttpResponseNotFound()

    code = request.POST.get("code")
    version = request.POST.get("version", 2)

    if not code:
        return HttpResponse("code not found", status=400)

    token = str(uuid4())
    device = Device(code=code, token=token, version=version)
    device.save()

    return HttpResponse(devicehandler.create_device(device))


@csrf_exempt
def delete_device(request):
    """
    Stop a existing AutoGen device.

    :post.data token: The token of the device to be stopped.
                      It is given by create API.
    """
    if request.method != 'POST':
        return HttpResponseNotFound()

    token = request.POST.get("token")
    if not token:
        return HttpResponse('token is required', status=400)

    try:
        device = Device.objects.get(token=token)
    except Device.DoesNotExist:
        return HttpResponse('device not found', status=400)

    token = devicehandler.delete_device(device)
    device.delete()

    return HttpResponse(token)


@csrf_exempt
def ccm_api(request):
    """
    CCM API.

    :post.data api_name: IoTtalk v1/v2 CCM API name.
    :post.data payload:  IoTtalk v1/v2 CCM API payload.
    :post.data username: Optional, IoTtalk v2 username.
    :post.data password: Optional, IoTtalk v2 password.
    TODO: username/password should use access token instead
    """
    if request.method != 'POST':
        return HttpResponseNotFound()

    api_name = request.POST.get('api_name')
    payload = json.loads(request.POST.get('payload', '{}'))
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    session_id = request.POST.get('session_id', None)

    if api_name not in ccm_api_args:
        return HttpResponse('api_name is not found', status=400)

    # extract args from payload
    try:
        args = [payload.pop(k) for k in ccm_api_args.get(api_name, [])]
    except KeyError as e:
        return HttpResponse('{} in the payload is required.'.format(e))

    # get api function from library ccmapi
    f = rgetattr(api, api_name)

    # login user for v2
    s = requests.Session()
    if username and password:
        u_id, cookie = api.account.login(username, password, session=s)
    elif session_id:
        s.cookies.update({'session_id': session_id})

    # assign logined session to invoke api
    payload.update({'session': s})

    try:
        result = f(*args, session=s)
    except CCMAPIError as e:
        result = e

    return HttpResponse(json.dumps(result))
