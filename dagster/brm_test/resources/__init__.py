from dagster import EnvVar
from .postgres_db import PostgresDB
from .clickhouse_db import ClickhouseDB
from .opensearch import Opensearch

# List of all project resources
PROJECT_RESOURCES = {
    "postgres_db": PostgresDB(
        dbname = EnvVar('POSTGRES_DB'),
        username = EnvVar('POSTGRES_USER'),
        password = EnvVar('POSTGRES_PASSWORD'),
        host = 'postgres',
        port = 5432
    ),
    "clickhouse_db": ClickhouseDB(
        database = EnvVar('CLICKHOUSE_DB'),
        username = EnvVar('CLICKHOUSE_USER'),
        password = EnvVar('CLICKHOUSE_PASSWORD'),
        host = 'clickhouse',
        port = 8123
    ),
    "opensearch": Opensearch(
        username = 'admin',
        password = EnvVar('OPENSEARCH_INITIAL_ADMIN_PASSWORD'),
        host = 'opensearch',
        port = 9200
    ),
}