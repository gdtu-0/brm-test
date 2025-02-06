from dagster import asset, AssetExecutionContext
from ..resources.clickhouse_db import ClickhouseDB
from ..resources.postgres_db import PostgresDB
from ..common.mtable import generate_MTable
from ..common import TABLE_DEFINITIONS
from .load_source import source_data_loaded


@asset(deps=[source_data_loaded])
def ch_load_data(context: AssetExecutionContext, clickhouse_db: ClickhouseDB, postgres_db: PostgresDB) -> None:
    """Create Clickhouse table and load data"""

    ch_data_table = generate_MTable(table_definition = TABLE_DEFINITIONS['ch_data'], resource = clickhouse_db)
    pg_data_table = generate_MTable(table_definition = TABLE_DEFINITIONS['pg_data'], resource = postgres_db)

    ch_data_table.create()
    ch_data_table.truncate()
    pg_data = pg_data_table.select()
    ch_data_table.insert(pg_data)

@asset(deps=[ch_load_data])
def ch_apply_mapping(context: AssetExecutionContext, clickhouse_db: ClickhouseDB, postgres_db: PostgresDB) -> None:
    """Apply mapping for Clickhouse DB"""

    ch_data_table = generate_MTable(table_definition = TABLE_DEFINITIONS['ch_data'], resource = clickhouse_db)
    mapping_table = generate_MTable(table_definition = TABLE_DEFINITIONS['mapping'], resource = postgres_db)

    mapping_df = mapping_table.select()
    for index, rule in mapping_df.iterrows():
        result_df = ch_data_table.select(where = rule['where_cond'])
        if result_df is not None:
            results_count = result_df.shape[0]
        else:
            results_count = 0
        print(f"RULE {index}: WHERE {rule['where_cond']}\nRESULTS :{results_count} row(s)")
