from dagster import Definitions
from .assets import PROJECT_ASSETS
from .resources import PROJECT_RESOURCES
from .jobs import PROJECT_JOBS

# Set dagster definitions
defs = Definitions(
    assets=PROJECT_ASSETS,
    resources=PROJECT_RESOURCES,
    # jobs=PROJECT_JOBS,
    # schedules = PROJECT_SCHEDULES,
    # sensors = PROJECT_SENSORS,
)
