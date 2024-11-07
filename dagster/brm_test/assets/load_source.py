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

    table = generate_MTable(table_definition = TABLE_DEFINITIONS['data'], resource = postgres_db)
    table.create()
    relpath = '../data/source_data/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        table.insert(df)

@asset
def load_mapping(context: AssetExecutionContext, postgres_db: PostgresDB) -> None:
    """Load mapping file"""
    
    table = generate_MTable(table_definition = TABLE_DEFINITIONS['mapping'], resource = postgres_db)
    table.create()
    relpath = '../data/mapping/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        for index, row in df.iterrows():
            translate_to_where_cond(row)
        table.insert(df)