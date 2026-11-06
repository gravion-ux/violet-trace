"""Synthetic event fixture generation.

The generator produces deterministic, clearly-labelled synthetic telemetry. It
never executes a technique, never touches a real system, and never produces a
value that could be mistaken for a live indicator.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from .catalog import CATALOG

__all__ = ["DEFAULT_HOST", "generate_events"]

DEFAULT_HOST = "violet-lab-01"

# A fixed epoch keeps the generated fixture byte-for-byte reproducible.
_EPOCH = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)


def _timestamp(index: int) -> str:
    moment = _EPOCH + timedelta(seconds=index * 60)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_events(scenario_ids=None, *, host: str = DEFAULT_HOST) -> list[dict]:
    """Return synthetic telemetry events for the requested scenarios.

    ``scenario_ids`` selects a subset of the catalog; ``None`` returns every
    scenario in catalog order. The result is deterministic: the same request
    always produces the same events.
    """
    if scenario_ids is None:
        selected = list(CATALOG)
    else:
        if isinstance(scenario_ids, str):
            scenario_ids = [scenario_ids]
        wanted = [str(item) for item in scenario_ids]
        selected = [scenario for scenario in CATALOG if scenario["id"] in wanted]
    events = []
    for index, scenario in enumerate(selected):
        events.append(
            {
                "event_type": scenario["event_type"],
                "scenario_id": scenario["id"],
                "technique": scenario["technique"],
                "host": host,
                "timestamp": _timestamp(index),
                "synthetic": True,
            }
        )
    return events
