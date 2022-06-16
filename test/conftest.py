import subprocess
import os

from .common import *


def prepare_env():
    if INFO.os == Constants.windows:
        export_path = PATH.test/'env/windows/export'
        origin_path = os.environ['PATH']
        os.environ['PATH'] = export_path.str+';'+origin_path
    elif INFO.os == Constants.linux:
        raise NotImplementedError
    else:
        raise NotImplementedError

def pytest_runtest_setup(item):
    prepare_env()

