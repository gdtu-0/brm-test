import functools
import psycopg2  # type: ignore
import psycopg2.extras  # type: ignore
from typing import Optional
from dagster import ConfigurableResource


class PostgresDB(ConfigurableResource):
    """Dagster resource definition for Postgres database"""

    dbname: str
    username: str
    password: str
    host: str
    port: int
    __connection: Optional[object] = None

    def handle_connection(function):
        """Wrapper for handling connection"""

        @functools.wraps(function)
        def wrapper_handle_connection(self, *args, **kwargs):
            # We do not explicitly close connection becasue Dagster initializes (and deletes) resources
            # for every op/asset. So, after op/asset finish resource will be destroyed and GC will
            # invoke del for resource object witch will close the connection
            if not self.__connection:
                self.__connection = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.username,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
            value = function(self, *args, **kwargs)
            return (value)
        return wrapper_handle_connection

    @handle_connection
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database"""

        sql_str = f"SELECT EXISTS (\n\tSELECT FROM information_schema.tables WHERE table_name = \'{table_name}\'\n);"

        exists = False
        with self.__connection.cursor() as cursor:
            cursor.execute(sql_str)
            exists = cursor.fetchone()[0]
        return (exists)

    @handle_connection
    def exec_sql_dict_cursor(self, sql: str) -> Optional[list]:
        """Execute SQL statement with dict cursor"""

        with self.__connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(sql)
            responce = cursor.fetchall()
            if not responce:
                return None
            else:
                result = []
                for row in responce:
                    result.append(dict(row))
                return (result)

    @handle_connection
    def exec_sql_no_fetch(self, sql: str) -> None:
        """Execute SQL statement and return nothing"""

        with self.__connection.cursor() as cursor:
            cursor.execute(sql)
            self.__connection.commit()

    @handle_connection
    def exec_insert(self, sql: str, values: list[tuple]):
        """Special case for insert statement"""

        with self.__connection.cursor() as cursor:
            psycopg2.extras.execute_values(
                cursor, sql, values, template=None, page_size=100)
            self.__connection.commit()
