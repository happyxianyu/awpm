from sqlalchemy.engine import Engine
from sqlalchemy import event

from .common import *

__all__ = []

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    logger.info('configure sqlite')
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.close()




