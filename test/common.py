import sys
import logging
import platform
from dataclasses import dataclass
from enum import Enum, auto
from cbutil import Path
__all__ = ['Path', 'PATH', 'logger', 'INFO', 'Constants']

logger = logging

def find_proj_root():
    from cbutil import Path
    path = Path(__file__)
    
    while True:
        prnt_path = path.prnt
        if prnt_path == path:
            return
        path = prnt_path
        if (path/'project_info.json').exists():
            return path

proj_root = find_proj_root()
if proj_root is None:
    raise RuntimeError('Cannot find project root')
sys.path.insert(0, str(proj_root/'info'))
from program_info import *


@dataclass
class Constants(Enum):
    windows = auto()
    linux = auto()


@dataclass
class InfoClass:
    os = dict(
        windows = Constants.windows,
        linux = Constants.linux
    )[platform.system().lower()]


INFO = InfoClass()

