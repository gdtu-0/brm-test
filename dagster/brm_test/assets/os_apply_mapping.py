from dagster import asset, AssetExecutionContext
from ..resources.opensearch import Opensearch
from ..resources.postgres_db import PostgresDB
from ..common.mtable import generate_MTable
from ..common import TABLE_DEFINITIONS
from ..common.loger import Loger
from .load_source import source_data_loaded


@asset(deps=[source_data_loaded])
def os_load_data(context: AssetExecutionContext, opensearch: Opensearch, postgres_db: PostgresDB) -> None:
    """Create Opensearch index and load data"""

    os_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['os_data'], resource=opensearch)
    pg_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['pg_data'], resource=postgres_db)

    os_data_table.truncate()
    os_data_table.create()
    pg_data = pg_data_table.select()
    os_data_table.insert(pg_data)


@asset(deps=[os_load_data])
def os_apply_mapping(context: AssetExecutionContext, opensearch: Opensearch, postgres_db: PostgresDB) -> None:
    """Apply mapping for Opensearch"""

    os_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['os_data'], resource=opensearch)
    mapping_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['mapping'], resource=postgres_db)

    mapping_df = mapping_table.select()
    with Loger(resource=postgres_db, db="Opensearch"):
        for index, rule in mapping_df.iterrows():
            result_df = os_data_table.select(where=rule['where_cond'])
            if result_df is not None:
                results_count = result_df.shape[0]
            else:
                results_count = 0
            print(
                f"RULE {index}: WHERE {rule['where_cond']}\nRESULTS :{results_count} row(s)")
