import logging
import re

from .exceptions import KernelExecError

log = logging.getLogger('siteutils.funcutils')


def remove_ansi_esc(s: str):
    '''
    https://stackoverflow.com/a/14693789
    '''
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', s)


def output_catcher():
    '''
    output catcher for IPython kernel
    '''
    def capture_output(context):  # https://tinyurl.com/y5y7fudy
        msg_type = context.get('msg_type')
        content = context.get('content', {})

        if msg_type == 'stream':  # https://tinyurl.com/y5868jpy
            capture_output.msg += content.get('text', '')

        elif msg_type == 'error':  # https://tinyurl.com/y6oeeeq6
            tb = content.get('traceback', [])
            capture_output.msg += remove_ansi_esc('\n'.join(tb))
            raise KernelExecError()

        elif msg_type == 'display_data':  # https://tinyurl.com/y5kmwswt
            data = content.get('data', {})
            for mime, val in data.items():
                if mime.startswith('image'):
                    capture_output.msg += f'<img src="data:{mime};base64,{val}">\n'
                elif mime.startswith('text'):
                    pass
                else:
                    log.warning(f'unsupported format {mime}: {val}')

    capture_output.msg = ''

    return capture_output
