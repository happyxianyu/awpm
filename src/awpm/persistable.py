from dataclasses import dataclass
import typing
import json
import base64

__all__ = ['AWProjectInstallInfo']

@dataclass
class AWProjectInstallInfo:
    id: bytes = None
    name: typing.Optional[str] = None          # default is ''
    version: typing.Optional[str] = None       # default is ''
    project_root: str = None
    export_paths: typing.List[str] = None      # default is []

    def to_json(self):
        return json.dumps(
            dict(
                id=base64.urlsafe_b64encode(self.id).decode('utf8'),
                name=self.name,
                version=self.version,
                project_root=self.project_root,
                export_paths=self.export_paths
            ), indent=4
        )



