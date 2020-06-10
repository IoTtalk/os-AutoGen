import logging
import traceback

from six import StringIO

log = logging.getLogger('autogen.exception')
log.setLevel(logging.DEBUG)


class CompilationError(Exception):
    pass

def raise_compilation_error():
    exc_output = StringIO()
    traceback.print_exc(file=exc_output)
    log.debug('User defined function exception:\n %s',
              exc_output.getvalue())
    raise CompilationError(exc_output.getvalue())
