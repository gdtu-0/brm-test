from dagster import Definitions
from .resources import PROJECT_RESOURCES
from .jobs import PROJECT_JOBS

# Set dagster definitions
defs = Definitions(
    # assets = ASSET_DEFINITIONS,
    resources = PROJECT_RESOURCES,
    jobs = PROJECT_JOBS,
    # schedules = PROJECT_SCHEDULES,
    # sensors = PROJECT_SENSORS,
)