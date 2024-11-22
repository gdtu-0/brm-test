import functools
import clickhouse_connect
from pandas import DataFrame
from dagster import ConfigurableResource
from typing import Optional


class ClickhouseDB(ConfigurableResource):
    """Dagster resource definition for Clickhouse database"""

    database: str
    username: str
    password: str
    host: str
    port: int
    _client: Optional[object]=None


    def handle_connection(function):
        """Wrapper for handling connection"""

        @functools.wraps(function)
        def wrapper_handle_connection(self, *args, **kwargs):
            # We do not explicitly close connection becasue Dagster initializes (and deletes) resources
            # for every op/asset. So, after op/asset finish resource will be destroyed and GC will
            # invoke del for resource object witch will close the connection
            if not self._client:
                self._client = clickhouse_connect.get_client(
                    database = self.database,
                    host = self.host,
                    port = self.port,
                    username = self.username,
                    password = self.password,
                )
            value = function(self, *args, **kwargs)
            return(value)
        return wrapper_handle_connection
    

    @handle_connection
    def exec_command(self, sql: str) -> None:
        """Execute SQL statement and return nothing"""

        self._client.command(sql)
    

    @handle_connection
    def exec_insert(self, table_name: str, values: list[tuple], column_names: list):
        """Special case for insert statement"""

        self._client.insert(table_name, values, column_names)
    

    @handle_connection
    def exec_query(self, sql: str) -> DataFrame:
        """Execute SQL query and return results as Pandas Dataframe"""

        return self._client.query_df(sql)