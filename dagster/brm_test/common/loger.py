import time
from datetime import datetime
from pandas import DataFrame
from dagster import ConfigurableResource
from ..common.mtable import generate_MTable
from ..common import TABLE_DEFINITIONS


class Loger:
    """Log implementation"""

    def __init__(self, resource: ConfigurableResource, db: str):
        self.__db = db
        self.__log_table = generate_MTable(
            table_definition=TABLE_DEFINITIONS['log_data'], resource=resource)
        self.__log_table.create()

    def __enter__(self):
        self.__stat_time = datetime.fromtimestamp(time.time())

    def __exit__(self, exc_type, exc_value, traceback):
        self.__end_time = datetime.fromtimestamp(time.time())
        duration = self.__end_time - self.__stat_time
        duration = duration.total_seconds()
        data = {'db': [self.__db],
                'ts_begin': [self.__stat_time],
                'ts_end': [self.__end_time],
                'duration': [duration],
                }
        self.__log_table.insert(data=DataFrame.from_dict(data))
