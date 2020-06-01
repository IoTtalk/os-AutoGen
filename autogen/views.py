"""Django View for Autogen Subsystem."""
import json

from uuid import uuid4

from ccmapi.exceptions import CCMAPIError
# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


from .models import Device
from .device import devicehandler
from .ccmapi import ccmapihandler


def index(request):
    """Index page, useless."""
    return HttpResponse("404")


@csrf_exempt
def create_device(request):
    """
    Create a new AutoGen device or update an existing device.

    :post.data code: The SA code for IoTtalk.
                     AutoGen will run this code as your device.
    :post.data token: Optional. If you want to update your device with new
                      SA code, you can assign the token of the device. AutoGen
                      will stop the previous device and run the new device.
    :post.data version: Optional: 1 or 2, default: 2. This value is used to run
                        different iottalk dan libraries. Depends on the device
                        the user wants to create.

    :response token: The token of the device has been created.
                     Used to update or delete this device.
    """
    if request.method != 'POST':
        return HttpResponseNotFound()

    code = request.POST.get("code")
    token = request.POST.get("token")
    version = request.POST.get("version", 2)

    if not code:
        return HttpResponse("code not found", status=400)

    if token:
        try:
            device = Device.objects.get(token=token)
        except Device.DoesNotExist:
            return HttpResponse('device not found', status=400)
    else:
        token = str(uuid4())
        device = Device(code=code, token=token, version=version)
        device.save()

    devicehandler.create_device(device)

    return HttpResponse(device.token)


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

    devicehandler.delete_device(device)

    return HttpResponse(device.token)


@csrf_exempt
def ccm_api(request):
    """CCM API."""
    if request.method != 'POST':
        return HttpResponseNotFound()

    api_name = request.POST.get('api_name')
    payload = json.loads(request.POST.get('payload', '{}'))

    if not api_name:
        return HttpResponse('api_name is required', status=400)
    if not payload:
        return HttpResponse('payload is required', status=400)

    try:
        result = ccmapihandler.request(api_name, payload)
        print(result)
    except CCMAPIError as e:
        print(str(e))
        return HttpResponse('CCMAPIError', status=400)

    # TODO ?
    return HttpResponse(result)
