import os
import pandas as pd
from pandas import DataFrame
from dagster import graph, op, OpExecutionContext
from ..common.mtable import generate_MTable
from ..resources.postgres_db import PostgresDB
from ..common import TABLE_DEFINITIONS


def _list_dir(relpath: str) -> list[str]:
    """List files in path (full filenames)"""

    out = []
    path = os.path.join(os.path.dirname(__file__), relpath)
    for file in os.listdir(path):
        out.append(os.path.normpath(f'{str(path)}{str(file)}'))
    return out

@op
def load_sapmle_data(context: OpExecutionContext, postgres_db: PostgresDB) -> None:
    """Load data sample as Dataframe"""

    table = generate_MTable(table_definition = TABLE_DEFINITIONS['data'], resource = postgres_db)
    table.create()
    relpath = '../data/source_data/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        table.insert(df)

@op
def load_mapping(context: OpExecutionContext, postgres_db: PostgresDB) -> None:
    """Load mapping file"""
    
    table = generate_MTable(table_definition = TABLE_DEFINITIONS['mapping'], resource = postgres_db)
    table.create()
    relpath = '../data/mapping/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, dtype=str, engine="odf")
        df = df.fillna(value='')
        table.insert(df)
    

@graph
def load_data_graph() -> None:
    load_sapmle_data()
    load_mapping()