import functools
import duckdb
from dagster import ConfigurableResource
from pandas import DataFrame
from typing import Optional


class DuckDB(ConfigurableResource):
    """Dagster resource definition for DuckDB"""

    __connection: Optional[object]=None


    def handle_connection(function):
        """Wrapper for handling connection"""

        @functools.wraps(function)
        def wrapper_handle_connection(self, *args, **kwargs):
            # We do not explicitly close connection becasue Dagster initializes (and deletes) resources
            # for every op/asset. So, after op/asset finish resource will be destroyed and GC will
            # invoke del for resource object witch will close the connection
            if not self.__connection:
                self.__connection = duckdb.connect("brm_test.duckdb")
            value = function(self, *args, **kwargs)
            return(value)
        return wrapper_handle_connection


    @handle_connection
    def table_exists(self, table_name:str) -> bool:
        """Check if table exists in database"""

        sql_str = f"SELECT EXISTS (\n\tSELECT table_name FROM information_schema.tables WHERE table_name = \'{table_name}\'\n);"

        exists = False
        self.__connection.sql(sql_str)
        exists = self.__connection.sql(sql_str).fetchone()[0]
        return(exists)
    

    @handle_connection
    def import_from_pandas(self, table_name: str, df: DataFrame) -> None:
        """Import table from Pandas Dataframe"""

        if self.table_exists(table_name = table_name):
            self.__connection.sql(f"TRUNCATE TABLE {table_name}")
        
        self.__connection.sql(f"INSERT INTO {table_name} SELECT * FROM df")
    

    @handle_connection
    def select_as_df(self, sql: str) -> Optional[DataFrame]:
        """Execute select statement and return results as Pandas Dataframe"""

        return self.__connection.sql(sql).df()
    

    @handle_connection
    def exec_sql_no_fetch(self, sql: str) -> None:
        """Execute SQL statement and return nothing"""

        self.__connection.sql(sql)