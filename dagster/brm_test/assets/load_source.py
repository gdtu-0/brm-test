import os
import pandas as pd
from dagster import asset, AssetExecutionContext
from ..resources.postgres_db import PostgresDB
from ..common.mtable import generate_MTable
from ..common import TABLE_DEFINITIONS
from ..common.translator import translate_to_where_cond


def _list_dir(relpath: str) -> list[str]:
    """List files in path (full filenames)"""

    out = []
    path = os.path.join(os.path.dirname(__file__), relpath)
    for file in os.listdir(path):
        out.append(os.path.normpath(f'{str(path)}{str(file)}'))
    return out


@asset
def load_sapmle_data(context: AssetExecutionContext, postgres_db: PostgresDB) -> None:
    """Load data sample as Dataframe"""

    table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['pg_data'], resource=postgres_db)
    table.create()
    table.truncate()
    relpath = '../data/source_data/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        table.insert(df)


@asset
def load_mapping(context: AssetExecutionContext, postgres_db: PostgresDB) -> None:
    """Load mapping file"""

    table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['mapping'], resource=postgres_db)
    table.create()
    table.truncate()
    relpath = '../data/mapping/'
    where_cond_column_name = 'where_cond'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        conds = {}
        for index, row in df.iterrows():
            conds[index] = translate_to_where_cond(row)
        df[where_cond_column_name] = pd.Series(conds)
        table.insert(df)


@asset(deps=[load_sapmle_data, load_mapping])
def source_data_loaded(context: AssetExecutionContext, postgres_db: PostgresDB) -> None:
    """Source data loaded"""

    data_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['pg_data'], resource=postgres_db)
    mapping_table = generate_MTable(
        table_definition=TABLE_DEFINITIONS['mapping'], resource=postgres_db)

    data_test_df = data_table.select(columns='*', extra='LIMIT 1')
    mapping_test_df = mapping_table.select(columns='*', extra='LIMIT 1')

    print(data_test_df)
    print(mapping_test_df)
