from pandas import DataFrame
from typing import Optional
from dataclasses import dataclass
from dagster import ConfigurableResource
from ..resources.postgres_db import PostgresDB
from ..resources.clickhouse_db import ClickhouseDB
from ..resources.opensearch import Opensearch
from ..resources.duck_db import DuckDB
import ast


@dataclass
class TableDefinition:
    """Table definition dataclass"""

    name: str
    column_definitions: dict
    extra: Optional[str] = None

    @property
    def columns(self) -> tuple:
        return tuple(self.column_definitions.keys())


class MTable:
    """Base MTable class"""

    def __init__(self, table_definition: TableDefinition, resource: ConfigurableResource):
        self.__table_definition = table_definition
        self.__resource = resource

    @property
    def table_definition(self) -> TableDefinition:

        return self.__table_definition

    @property
    def resource(self) -> ConfigurableResource:

        return self.__resource

    def create(self) -> None:
        """Base create method"""

        raise NotImplementedError

    def truncate(self) -> None:
        """Base truncate method"""

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

        columns_str = ",\n  ".join(
            f'{name} {specs}' for name, specs in self.table_definition.column_definitions.items())
        create_str = f"CREATE TABLE IF NOT EXISTS {self.table_definition.name} (\n  {columns_str}\n)"
        sql_str = f"{create_str};"
        self.resource.exec_sql_no_fetch(sql_str)

    def truncate(self) -> None:
        """PostgreSQL truncate method"""

        sql_str = f"TRUNCATE {self.table_definition.name};"
        self.resource.exec_sql_no_fetch(sql_str)

    def insert(self, data: DataFrame):
        """PostgreSQL insert method"""

        columns_str = ", ".join(name for name in data.columns)
        insert_str = f"INSERT INTO {self.table_definition.name}\n  ({columns_str})\nVALUES %s"
        sql_str = insert_str

        self.resource.exec_insert(sql=sql_str, values=list(
            data.itertuples(index=False, name=None)))

    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """PostgreSQL select method"""

        if columns:
            columns_str = ", ".join(name for name in columns)
        else:
            columns_str = ", ".join(
                name for name in self.table_definition.columns)
        select_str = f"SELECT\n  {columns_str}\n"
        from_str = f"FROM {self.table_definition.name}"
        if where:
            where_str = "\nWHERE " + where
        else:
            where_str = ''
        if extra:
            extra_str = '\n' + extra
        else:
            extra_str = ''
        sql_str = f"{select_str}{from_str}{where_str}{extra_str};"
        result = self.resource.exec_sql_dict_cursor(sql=sql_str)
        if result:
            return DataFrame.from_dict(result)
        else:
            return None


class MTable_CH(MTable):
    """MTable implementation for Clickhouse"""

    def create(self) -> None:
        """Clickhouse create method"""

        columns_str = ",\n  ".join(
            f'{name} {specs}' for name, specs in self.table_definition.column_definitions.items())
        create_str = f"CREATE TABLE IF NOT EXISTS {self.table_definition.name} (\n  {columns_str}\n)"
        if self.table_definition.extra:
            create_str = f'{create_str}\n{self.table_definition.extra}'
        sql_str = f"{create_str};"
        self.resource.exec_command(sql_str)

        sql_str = f"TRUNCATE {self.table_definition.name};"
        self.resource.exec_command(sql_str)

    def truncate(self) -> None:
        """Clickhouse truncate method"""

        sql_str = f"TRUNCATE {self.table_definition.name};"
        self.resource.exec_command(sql_str)

    def insert(self, data: DataFrame):
        """Clickhouse insert method"""

        column_names = list(name for name in data.columns)
        self.resource.exec_insert(table_name=self.table_definition.name, values=list(
            data.itertuples(index=False, name=None)), column_names=column_names)

    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """Clickhouse select method"""

        if columns:
            columns_str = ", ".join(name for name in columns)
        else:
            columns_str = ", ".join(
                name for name in self.table_definition.columns)
        select_str = f"SELECT\n  {columns_str}\n"
        from_str = f"FROM {self.table_definition.name}"
        if where:
            where_str = "\nWHERE " + where
        else:
            where_str = ''
        if extra:
            extra_str = '\n' + extra
        else:
            extra_str = ''
        sql_str = f"{select_str}{from_str}{where_str}{extra_str};"
        return self.resource.exec_query(sql=sql_str)


class MTable_OS(MTable):
    """MTable implementation for OpenSearch"""

    def create(self) -> None:
        """OpenSearch create method"""

        self.resource.create(
            index_name=self.table_definition.name,
            properties=self.table_definition.column_definitions
        )

    def truncate(self) -> None:
        """OpenSearch truncate method"""

        self.resource.delete(index_name=self.table_definition.name)

    def insert(self, data: DataFrame):
        """OpenSearch insert method"""

        documents = data.to_dict('records')
        id = 0
        for document in documents:
            id = id + 1
            document["_index"] = self.table_definition.name
            document["_id"] = id

        self.resource.bulk_index(
            index_name=self.table_definition.name,
            documents=documents,
        )

    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """OpenSearch select method"""

        if columns:
            columns_str = ", ".join(name for name in columns)
        else:
            columns_str = ", ".join(
                name for name in self.table_definition.columns)
        select_str = f"SELECT\n  {columns_str}\n"
        from_str = f"FROM {self.table_definition.name}"
        if where:
            where_str = "\nWHERE " + where
        else:
            where_str = ''
        sql_str = f"{select_str}{from_str}{where_str}"

        output = self.resource.exec_sql(sql=sql_str)
        ast_out = ast.literal_eval(output)

        try:
            ast_out["error"]
        except KeyError:
            if ast_out["total"] > 0:
                print(ast_out["datarows"])
        else:
            print(ast_out["error"])
            print(sql_str)
            # raise Exception
        return None


class MTable_DD(MTable):
    """MTable implementation for DuckDB"""

    def create(self) -> None:
        """DuckDB create method"""

        columns_str = ",\n  ".join(
            f'{name} {specs}' for name, specs in self.table_definition.column_definitions.items())
        create_str = f"CREATE TABLE IF NOT EXISTS {self.table_definition.name} (\n  {columns_str}\n)"
        sql_str = f"{create_str};"
        self.resource.exec_sql_no_fetch(sql_str)

    def truncate(self) -> None:
        """DuckDB truncate method"""

        sql_str = f"TRUNCATE {self.table_definition.name};"
        self.resource.exec_sql_no_fetch(sql_str)

    def insert(self, data: DataFrame):
        """DuckDB insert method"""

        self.resource.import_from_pandas(
            table_name=self.table_definition.name, df=data)

    def select(self, columns: Optional[tuple] = None, where: Optional[str] = None, extra: Optional[str] = None) -> Optional[DataFrame]:
        """DuckDB select method"""

        if columns:
            columns_str = ", ".join(name for name in columns)
        else:
            columns_str = ", ".join(
                name for name in self.table_definition.columns)
        select_str = f"SELECT\n  {columns_str}\n"
        from_str = f"FROM {self.table_definition.name}"
        if where:
            where_str = "\nWHERE " + where
        else:
            where_str = ''
        sql_str = f"{select_str}{from_str}{where_str}"

        return self.resource.select_as_df(sql=sql_str)


def generate_MTable(table_definition: TableDefinition, resource: ConfigurableResource) -> MTable:
    """MTable generator"""

    if resource.__class__ is PostgresDB:
        mtable = MTable_PG(table_definition, resource)
    elif resource.__class__ is ClickhouseDB:
        mtable = MTable_CH(table_definition, resource)
    elif resource.__class__ is Opensearch:
        mtable = MTable_OS(table_definition, resource)
    elif resource.__class__ is DuckDB:
        mtable = MTable_DD(table_definition, resource)
    else:
        raise NotImplementedError

    return mtable
