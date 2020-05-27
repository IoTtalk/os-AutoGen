"""Device Handler."""
import logging
import traceback

from multiprocessing import Process, get_context
from six import StringIO

from .exceptions import CompilationError

log = logging.getLogger('autogen.device')
log.setLevel(logging.DEBUG)


class _DeviceHandler():
    def __init__(self):
        self._device_processes = {}

    def create_device(self, device):
        # Check if the device prcess exists
        # If it exists, return the token directly
        if self._device_processes.get(device.token):
            return device.token

        # If it does not exist, create a device process
        # TODO

        ctx = get_context('forkserver')
        target = getattr(self, f'_create_v{device.version}_device')

        proc = ctx.Process(target=target, args=(device.code, device.token))
        proc.daemon = False
        proc.start()

        self._device_processes[device.token] = proc

        return device.token

    def delete_device(self, device):
        # Check if the device prcess exists
        proc = self._device_processes.get(device.token)
        if proc and proc.is_alive():
            proc.terminate()
            proc.join(2)

        return device.token

    @staticmethod
    def _create_v1_device(code, token):
        # TODO
        pass

    @staticmethod
    def _create_v2_device(code, token):
        # TODO
        filename = '<UserSA:{}>'.format(token)
        context = {}
        try:
            code = compile(code, filename, mode='exec')
            exec(code, context)
        except Exception:
            exc_output = StringIO()
            traceback.print_exc(file=exc_output)
            log.debug('User defined function exception:\n %s',
                      exc_output.getvalue())
            raise CompilationError(exc_output.getvalue())

devicehandler = _DeviceHandler()
