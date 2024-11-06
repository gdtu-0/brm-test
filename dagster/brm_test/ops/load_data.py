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
def load_sapmle_data(context: OpExecutionContext) -> None:
    """Load data sample as Dataframe"""
    relpath = '../data/source_data/'
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        # df = pd.read_excel(filename, engine="odf")

@op
def load_mapping(context: OpExecutionContext, postgres_db: PostgresDB) -> None:
    """Load mapping file"""
    relpath = '../data/mapping/'
    table = generate_MTable(postgres_db)
    table.create(name='mapping', columns=TABLE_DEFINITIONS['mapping'])
    for filename in _list_dir(relpath):
        context.log.info(f"Loading {filename}")
        df = pd.read_excel(filename, engine="odf")
        df = df.fillna(value='')
        table.insert(values=list(df.itertuples(index = False, name = None)))
    

@graph
def load_data_graph() -> None:
    load_sapmle_data()
    load_mapping()