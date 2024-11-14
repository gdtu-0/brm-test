from pandas import DataFrame
from typing import Optional
from dataclasses import dataclass
from dagster import ConfigurableResource
from ..resources.postgres_db import PostgresDB


@dataclass
class TableDefinition:
    """Table definition dataclass"""

    name: str
    column_definitions: dict

    @property
    def columns(self) -> tuple:
        return tuple(self.column_definitions.keys())

class MTable:
    """Base MTable class"""

    _table_definition: TableDefinition
    _resource: ConfigurableResource

    def __init__(self, table_definition: TableDefinition, resource: ConfigurableResource):
        self._table_definition = table_definition
        self._resource = resource

    def create(self) -> None:
        """Base create method"""

        raise NotImplementedError
    
    def insert(self, data: DataFrame) -> None:
        """Base insert method"""

        raise NotImplementedError
    
    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """Base select method"""

        raise NotImplementedError


class MTable_PG(MTable):
    """MTable implementation for PostgreSQL"""

    def create(self) -> None:
        """PostgreSQL create method"""
        
        columns_str = ",\n  ".join(f'{name} {specs}' for name, specs in self._table_definition.column_definitions.items())
        create_str = f"CREATE TABLE IF NOT EXISTS {self._table_definition.name} (\n  {columns_str}\n)"
        sql_str = f"{create_str};"
        self._resource.exec_sql_no_fetch(sql_str)

        sql_str = f"TRUNCATE {self._table_definition.name};"
        self._resource.exec_sql_no_fetch(sql_str)

    def insert(self, data: DataFrame):
        """PostgreSQL insert method"""

        columns_str = ", ".join(name for name in data.columns)
        insert_str = f"INSERT INTO {self._table_definition.name}\n  ({columns_str})\nVALUES %s"
        sql_str = insert_str

        self._resource.exec_insert(sql = sql_str, values = list(data.itertuples(index = False, name = None)))

    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """PostgreSQL select method"""

        if columns:
            columns_str = ", ".join(name for name in columns)
        else:
            columns_str = ", ".join(name for name in self._table_definition.columns)
        select_str = f"SELECT\n  {columns_str}\n"
        from_str = f"FROM {self._table_definition.name}"
        if where:
            where_str = "\nWHERE " + where
        else:
            where_str = ''
        if extra:
            extra_str = '\n' + extra
        else:
            extra_str = ''
        sql_str = f"{select_str}{from_str}{where_str}{extra_str};"
        result = self._resource.exec_sql_dict_cursor(sql = sql_str)
        if result:
            return DataFrame.from_dict(result)
        else:
            return None


def generate_MTable(table_definition: TableDefinition, resource: ConfigurableResource) -> MTable:
    """MTable generator"""

    if resource.__class__ is PostgresDB:
        mtable = MTable_PG(table_definition, resource)
    else:
        raise NotImplementedError
    
    return mtable