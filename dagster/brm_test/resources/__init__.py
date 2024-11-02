from dagster import EnvVar
from .postgres_db import PostgresDB

# List of all project resources
PROJECT_RESOURCES = {
    "postgres_db": PostgresDB(
        dbname = EnvVar('POSTGRES_DB'),
        username = EnvVar('POSTGRES_USER'),
        password = EnvVar('POSTGRES_PASSWORD'),
        host = 'postgres',
        port = 5432),
}