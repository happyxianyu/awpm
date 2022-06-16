import typing
import os
import subprocess
from dataclasses import dataclass

from .common import *
from .util import *
from .persistable import *
from .db import *

__all__ = ['AWProjectManager']


class AWProjectManager:
    @dataclass
    class PathInfo:
        root:Path
        db_service:Path
        script:Path
        def __init__(self, root:Path) -> None:
            self.root = root
            self.db_service = root/'primary_db'
            self.script = root/'script'
        
    def __init__(self, data_root: Path):
        self.PATH = PATH = self.PathInfo(data_root)
        # self.data_root = data_root
        # db_service_data_path = data_root/'primary_db'
        service_mngr = AWDBServiceMngr(PATH.db_service)
        self.project_install_info_service = service_mngr.project_install_info_service

    def add_project(self, project_info: AWProjectInstallInfo):
        # export paths must be relative to root
        assert project_info.export_paths is None or not any(map(os.path.isabs, project_info.export_paths))
        self.project_install_info_service.add_project_info(project_info)
        return self._update_export_path()

    def del_project(self, project_id: bytes):
        self.project_install_info_service.del_project_info(project_id)
        return self._update_export_path()

    def iter_project_info(self):
        return self.project_install_info_service.iter_project_info()

    def get_project_info(self, project_id: bytes) -> typing.Optional[AWProjectInstallInfo]:
        return self.project_install_info_service.get_project_info(project_id)

    def list_project_info_by_name(self, name:str):
        return self.project_install_info_service.list_project_info_by_name(name)

    def _update_export_path(self):
        service = self.project_install_info_service
        fields = service.project_install_info_fields
        abs_export_paths = []
        for proj_root, export_paths in service.iter_fields_of_project_info([fields.project_root, fields.export_paths]):
            proj_root = Path(proj_root)
            abs_export_paths += [(proj_root/export_path).str for export_path in export_paths]
        if INFO.os == Constants.windows:
            if len(abs_export_paths):
                paths_str = '"' + ';'.join(abs_export_paths) + '"'
                res = run_cmd(f"setx AWPM_EXPORT {paths_str}", cwd=None)
            else:
                res = run_cmd('setx AWPM_EXPORT ""', cwd=None)
            return res.returncode == 0
        elif INFO.os == Constants.linux:
            raise NotImplementedError
        else:
            raise NotImplementedError



