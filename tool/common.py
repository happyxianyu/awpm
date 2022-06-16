import sys
from cbutil import Path
__all__ = ['Path', 'PATH']

self_path = Path(__file__)
proj_root = self_path.prnt.prnt
sys.path.insert(0, str(proj_root/'info'))

from project_info import *


