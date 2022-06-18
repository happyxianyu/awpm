from dataclasses import dataclass
from cbutil import Path

__all__ = ['PATH']

self_path = Path(__file__)
proj_root = self_path.prnt.prnt

@dataclass
class PathInfo:
    root:Path = proj_root
    info:Path = root/'info'
    assets:Path = root/'assets'
    data:Path = root/'data'
    cache:Path = root/'cache'
    tmp:Path = root/'tmp'
    other:Path = root/'other'

    src:Path = root/'src'
    module:Path = root/'module'
    export:Path = root/'export'
    test:Path = root/'test'
    project:Path = root/'project'
    tool:Path = root/'tool'
    doc:Path = root/'doc'

    vscode:Path = root/'.vscode'

    journal:Path = data/'journal'
    log:Path = other/'log'
    module_gen:Path = module/'gen'

    project_info_json = root/'project_info.json'

    primary_db = data/'primary_db'

    _dirs = [root, info, data, cache, tmp, other, src,export, project, tool, doc, vscode, journal, log]

    def get_directories(self):
        return self._dirs


PATH = PathInfo()

