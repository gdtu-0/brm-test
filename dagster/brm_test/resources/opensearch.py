import functools
from opensearchpy import OpenSearch
from opensearchpy.helpers.index import Index
from opensearchpy.helpers import bulk
from dagster import ConfigurableResource
from typing import Optional
import requests


class Opensearch(ConfigurableResource):

    """Dagster resource definition for Opensearch"""

    username: str
    password: str
    host: str
    port: int
    __client: Optional[object] = None

    def handle_connection(function):
        """Wrapper for handling connection"""

        @functools.wraps(function)
        def wrapper_handle_connection(self, *args, **kwargs):
            # We do not explicitly close connection becasue Dagster initializes (and deletes) resources
            # for every op/asset. So, after op/asset finish resource will be destroyed and GC will
            # invoke del for resource object witch will close the connection
            if not self.__client:
                self.__client = OpenSearch(
                    hosts=[{'host': self.host, 'port': self.port}],
                    http_auth=(self.username, self.password),
                    http_compress=False,
                    use_ssl=True,
                    verify_certs=False,
                    ssl_assert_hostname=False,
                    ssl_show_warn=False,
                )
            value = function(self, *args, **kwargs)
            return (value)
        return wrapper_handle_connection

    @handle_connection
    def create(self, index_name: str, properties: dict) -> None:
        """Create or replace index"""

        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 1
                }
            },
            'mappings': {
                'properties': properties
            }
        }

        if not self.__client.indices.exists(index_name):
            result = self.__client.indices.create(
                index_name,
                body=index_body
            )

    @handle_connection
    def delete(self, index_name: str) -> None:

        if self.__client.indices.exists(index_name):
            self.__client.indices.delete(index_name)

    @handle_connection
    def bulk_index(self, index_name: str, documents: list[dict]) -> None:
        """Bulk insert documents to index"""

        bulk(self.__client, documents)

    @handle_connection
    def exec_sql(self, sql: str) -> str:
        """Opensearch select"""

        sql_url = f"https://{self.host}:{self.port}/_plugins/_sql"
        data = {"query": sql}
        header = {'Content-type': 'application/json'}

        result = requests.post(url=sql_url, json=data, headers=header, auth=(
            self.username, self.password), verify=False)

        return result.text
