"""Device Handler."""
import logging
import traceback

from six import StringIO

from iottalkpy.dai import module_to_sa

from .exceptions import CompilationError

log = logging.getLogger('autogen.device')
log.setLevel(logging.DEBUG)


# TODO load_module_from_str in dai
class App(object):
    def __init__(self, d):
        self.__dict__ = d


class _DeviceHandler():
    def __init__(self):
        self._device_processes = {}

    def create_device(self, device):
        # Check if the device prcess exists
        # If it exists, return the token directly
        if self._device_processes.get(device.token):
            return device.token

        try:  # TODO, currently V2 only
            # compile SA code
            context = {}
            exec(device.code, context)

            # run device via DAI
            dai = module_to_sa(App(context))
            dai.start()
        except Exception:
            exc_output = StringIO()
            traceback.print_exc(file=exc_output)
            log.debug('User defined function exception:\n %s',
                      exc_output.getvalue())
            raise CompilationError(exc_output.getvalue())

        self._device_processes[device.token] = dai

        return device.token

    def delete_device(self, device):
        # Check if the device prcess exists
        dai = self._device_processes.get(device.token)
        if dai:
            dai.terminate()

        return device.token

devicehandler = _DeviceHandler()
