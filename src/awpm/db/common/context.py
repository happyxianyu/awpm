import sqlalchemy as sa
from sqlalchemy.pool import SingletonThreadPool

from .common import *


__all__ = ['AWDBContext']

class AWDBContext:
    def __init__(self, db_path:Path, enable_debug=False):
        self.db_path = db_path
        self.engine = sa.create_engine(
            'sqlite+pysqlite:///' + db_path.absolute().str, 
            echo=enable_debug, 
            future=True,
            poolclass=SingletonThreadPool)
        
    


