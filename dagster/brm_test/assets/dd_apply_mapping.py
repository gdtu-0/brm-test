from dagster import asset, AssetExecutionContext
from ..resources.duck_db import DuckDB
from ..resources.postgres_db import PostgresDB
from ..common.mtable import generate_MTable
from ..common import TABLE_DEFINITIONS
from .load_source import source_data_loaded


@asset(deps=[source_data_loaded])
def dd_load_data(context: AssetExecutionContext, duckdb: DuckDB, postgres_db: PostgresDB) -> None:
    """Create DuckDB table and load data"""

    dd_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['dd_data'], resource=duckdb)
    pg_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['pg_data'], resource=postgres_db)

    dd_data_table.create()
    dd_data_table.truncate()
    pg_data = pg_data_table.select()
    # DuckDB has some issues with Decimal type
    pg_data = pg_data.astype({'amount': 'float64'})
    dd_data_table.insert(pg_data)


@asset(deps=[dd_load_data])
def dd_apply_mapping(context: AssetExecutionContext, duckdb: DuckDB, postgres_db: PostgresDB) -> None:
    """Apply mapping for DuckDB"""

    dd_data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['dd_data'], resource=duckdb)
    mapping_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['mapping'], resource=postgres_db)

    mapping_df = mapping_table.select()
    for index, rule in mapping_df.iterrows():
        result_df = dd_data_table.select(where=rule['where_cond'])
        if result_df is not None:
            results_count = result_df.shape[0]
        else:
            results_count = 0
        print(
            f"RULE {index}: WHERE {rule['where_cond']}\nRESULTS :{results_count} row(s)")
