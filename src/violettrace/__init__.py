"""VioletTrace: safe purple-team validation harness for defensive telemetry.

Public API
----------
``list_scenarios``   the declarative simulation catalog
``generate_events``  deterministic synthetic event fixtures
``coverage_report``  coverage summary for observed telemetry
"""
from .catalog import CATALOG, list_scenarios, scenario_ids
from .events import generate_events
from .report import coverage_report

__all__ = [
    "CATALOG",
    "__version__",
    "coverage_report",
    "generate_events",
    "list_scenarios",
    "scenario_ids",
]

__version__ = "0.2.0"
