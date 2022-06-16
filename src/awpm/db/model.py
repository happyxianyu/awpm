import sqlalchemy as sa
from sqlalchemy import Column, BLOB, String
from sqlalchemy.orm import registry, Mapper
from sqlalchemy import Table

import json
import typing


__all__ = ['AWProjectInstallInfoRecord']



class StrList(sa.types.TypeDecorator):
    impl = sa.types.String

    cache_ok = True

    def process_bind_param(self, value:typing.Optional[typing.List[str]], dialect):
        if value is None or len(value) == 0:
            return ''
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value == '':
            return []
        else:
            return json.loads(value)

Base = registry().generate_base()


class AWProjectInstallInfoRecord(Base):
    __table__:Table
    __mapper__:Mapper
    __tablename__ = "AWProjectInstallInfoTable"
    id = Column(BLOB, primary_key=True)
    name = Column(String, default='', index=True)
    version = Column(String, default='')
    project_root = Column(String, nullable=False)
    export_paths = Column(StrList, default='')


