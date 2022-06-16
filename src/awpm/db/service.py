import typing
from contextlib import contextmanager
import dataclasses

import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from ..persistable import *

from .common import *
from .model import *
from .helper import iter_field_names_of_dataclass

__all__ = ['AWProjectInstallInfoService', 'AWDBServiceMngr']



class AWProjectInstallInfoService:
    def __init__(self, engine:sa.engine.Engine):
        self.engine = engine
        self._Session = sessionmaker(engine)
        # only for select
        self.project_install_info_fields = AWProjectInstallInfoRecord
        AWProjectInstallInfoRecord.__table__.create(bind=engine, checkfirst=True)

    def session(self) -> Session:
        return self._Session(future=True)

    @contextmanager
    def session_begin(self) -> typing.Iterator[Session]:
        with self._Session() as session:
            with session.begin():
                yield session
    
    def conn(self):
        return self.engine.connect()

    def add_project_info(self, project_info: AWProjectInstallInfo, replace_exists=True):
        # test not nullable fields
        assert isinstance(project_info.id, bytes)
        assert isinstance(project_info.project_root, str)

        with self.session_begin() as session:
            def simple_add():
                session.add(AWProjectInstallInfoRecord(
                        **DictObjectAdaptor(project_info, iter_field_names_of_dataclass(project_info))))

            if replace_exists:
                record = session.get(AWProjectInstallInfoRecord, project_info.id)
                if record is None:
                    simple_add()
                else:
                    DictObjectAdaptor(record).update(DictObjectAdaptor(project_info, 
                        filter(lambda n: n!='id',iter_field_names_of_dataclass(project_info))))
            else:
                simple_add()
            

    def add_batch_project_info(self, project_info_list: typing.List[AWProjectInstallInfo], replace_exists=True):
        # test not nullable fields
        record_list = []
        for project_info in project_info_list:
            assert isinstance(project_info.id, bytes)
            assert isinstance(project_info.project_root, str)

            record = AWProjectInstallInfoRecord()
            record.id = project_info.id
            record.name = project_info.name
            record.version = project_info.version
            record.project_root = project_info.project_root
            record.export_paths = project_info.export_paths
            record_list.append(record)
            
        with self.session_begin() as session:
            session:Session
            for record in record_list:
                if replace_exists:
                    raise NotImplementedError
                else:
                    session.add(record)
                

    def del_project_info(self, project_id: bytes):
        with self.session_begin() as session:
            session.delete(session.get(AWProjectInstallInfoRecord, project_id))

    def iter_project_info(self):
        with self.session() as session:
            for record in session.query(AWProjectInstallInfoRecord):
                yield self._make_project_install_info_from_record(record)

    def iter_fields_of_project_info(self, fields:list=None) -> typing.Iterator[tuple]:
        with self.session() as session:
            for row in session.query(*fields):
                yield tuple(getattr(row, field.key) for field in fields)

    def get_project_info(self, project_id: bytes) -> typing.Optional[AWProjectInstallInfo]:
        assert isinstance(project_id, bytes)

        with self.session() as session:
            record:AWProjectInstallInfoRecord = session.get(AWProjectInstallInfoRecord, project_id)
        
        if record is None:
            return
        else:
            return AWProjectInstallInfo(
                id=record.id, 
                name=record.name, 
                version=record.version, 
                project_root=record.project_root, 
                export_paths=record.export_paths)

    def list_project_info_by_name(self, name:str) -> typing.List[AWProjectInstallInfo]:
        assert isinstance(name, str)

        with self.session() as session:
            records:AWProjectInstallInfoRecord = session.query(AWProjectInstallInfoRecord).filter_by(name=name).all()
        
        return [
            self._make_project_install_info_from_record(record)
            for record in records
        ]


    @staticmethod
    def _make_project_install_info_from_record(record:AWProjectInstallInfoRecord):
        return AWProjectInstallInfo(
            id=record.id, 
            name=record.name, 
            version=record.version, 
            project_root=record.project_root, 
            export_paths=record.export_paths)


class AWDBServiceMngr:
    def __init__(self, service_data_path:Path, enable_debug=False):
        service_data_path.mkdir()
        db_path = service_data_path/'db'
        dbctx = AWDBContext(db_path, enable_debug)
        self.project_install_info_service = AWProjectInstallInfoService(dbctx.engine)
        
        