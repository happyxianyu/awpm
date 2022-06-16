import logging
import platform
from dataclasses import dataclass
from enum import Enum, auto
from cbutil import Path, DictObjectAdaptor

__all__ = ['Path', 'logger', 'DictObjectAdaptor', 'INFO', 'Constants']

logger = logging

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

