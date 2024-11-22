from dagster import EnvVar
from .postgres_db import PostgresDB
from .clickhouse_db import ClickhouseDB

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
}