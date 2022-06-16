import dataclasses

__all__ = [
    'list_field_names_of_dataclass', 
    'iter_field_names_of_dataclass',
    'list_col_names_of_table']

def list_col_names_of_table(tb):
    keys = tb.__table__.columns.keys()
    return keys

def iter_field_names_of_dataclass(dc):
    return (field.name for field in dataclasses.fields(dc))

def list_field_names_of_dataclass(dc):
    return list(iter_field_names_of_dataclass(dc))
    