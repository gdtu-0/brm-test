from .load_source import (
    load_mapping,
    load_sapmle_data,
    source_data_loaded
)

from .pg_apply_mapping import (
    pg_apply_mapping,    
)

from .ch_apply_mapping import(
    ch_load_data,
    ch_apply_mapping,
)

from .os_apply_mapping import(
    os_load_data
)

PROJECT_ASSETS = [
    load_mapping,
    load_sapmle_data,
    source_data_loaded,
    pg_apply_mapping,
    ch_load_data,
    ch_apply_mapping,
    os_load_data,
]