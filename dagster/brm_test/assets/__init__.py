from .load_source import (
    load_mapping,
    load_sapmle_data,
    source_data_loaded
)

from .pg_apply_mapping import (
    pg_apply_mapping,    
)

PROJECT_ASSETS = [
    load_mapping,
    load_sapmle_data,
    source_data_loaded,
    pg_apply_mapping,
]