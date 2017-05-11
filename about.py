"""About page - sysinfo function.
"""
import os
import platform
import shutil
import socket
import sys
from pip.operations import freeze

def sysinfo(newline=None): #----------------------------------------------<<<
    """Return system information.

    newline = delimiter for returned list of key/value pairs; if not
              specified, a dictionary of key/value pairs is returned

    Since this information is typically used for diagnostic printing or
    displaying of values, all vaues are returned as strings.
    """
    sys_info = dict()
    sys_info['PY_VERSION'] = sys.version.strip().split(' ')[0] + \
        (' (64-bit)' if '64 bit' in sys.version else ' (32-bit)')
    sys_info['PY_LOCATION'] = sys.prefix
    sys_info['PY_PACKAGES'] = ','.join([_ for _ in freeze.freeze()])
    sys_info['PY_PATH'] = ','.join(sys.path)
    sys_info['OS_VERSION'] = platform.platform()
    sys_info['HOST_NAME'] = socket.gethostname()
    sys_info['HOST_PROC'] = \
        os.environ['PROCESSOR_ARCHITECTURE'] + ', ' + \
        os.environ['PROCESSOR_IDENTIFIER'].split(' ')[0] + ', ' + \
        os.environ['NUMBER_OF_PROCESSORS'] + ' cores'
    sys_info['HOST_IPADDR'] = socket.gethostbyname(socket.gethostname())
    sys_info['DIRECTORY'] = os.getcwd()
    size, used, free = shutil.disk_usage('/')
    sys_info['DISK_SIZE'] = '{:,}'.format(size)
    sys_info['DISK_USED'] = '{:,}'.format(used)
    sys_info['DISK_FREE'] = '{:,}'.format(free)

    if newline:
        return newline.join([key + ': ' + sys_info[key] for key in sorted(sys_info)])
    return sys_info
