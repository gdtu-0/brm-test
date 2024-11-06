from pandas import DataFrame
from typing import Optional
from dagster import ConfigurableResource
from ..resources.postgres_db import PostgresDB


class MTable:
    """Base MTable class"""

    resource: ConfigurableResource
    name: str
    columns: tuple[str]

    def __init__(self, resource: ConfigurableResource):
        self.resource = resource

    def create(self) -> None:
        """Base create method"""

        raise NotImplementedError
    
    def insert(self) -> None:
        """Base insert method"""

        raise NotImplementedError
    
    def select(self) -> DataFrame:
        """Base select method"""

        raise NotImplementedError


class MTable_PG(MTable):
    """MTable implementation for PostgreSQL"""

    def create(self, name: str, columns: dict[str, str], data: Optional[DataFrame] = None) -> None:
        """PostgreSQL create method"""
        
        self.name = name
        self.columns = tuple(columns.keys())
        
        columns_str = ",\n  ".join(f'{name} {specs}' for name, specs in columns.items())
        create_str = f"CREATE TABLE IF NOT EXISTS {self.name} (\n  {columns_str}\n)"
        sql_str = f"{create_str};"

        self.resource.exec_sql_no_fetch(sql_str)

    def insert(self, values: list[tuple]):
        """PostgreSQL insert method"""

        columns_str = ", ".join(name for name in self.columns)
        insert_str = f"INSERT INTO {self.name}\n  ({columns_str})\nVALUES %s"
        sql_str = f"{insert_str}"
        self.resource.exec_insert(sql = sql_str, values = values)


def generate_MTable(resource: ConfigurableResource) -> MTable:
    """MTable generator"""

    if resource.__class__ is PostgresDB:
        mtable = MTable_PG(resource)
    else:
        raise NotImplementedError
    
    return mtable