"""Utils for Autogen Subsystem."""
import functools


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
