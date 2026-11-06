"""Coverage reporting for defensive telemetry."""
from collections.abc import Iterable

from .catalog import CATALOG

__all__ = ["coverage_report"]


def _event_type(value):
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        value = value.get("event_type")
        return value.strip() if isinstance(value, str) and value.strip() else None
    return None


def coverage_report(observed_event_types):
    """Summarize which catalog scenarios the observed telemetry covers.

    Event types that are not part of the catalog are reported separately
    instead of being dropped: an unexpected event type is a gap in the
    catalog, and it has to stay visible.
    """
    if observed_event_types is None:
        observed_event_types = []
    elif isinstance(observed_event_types, (str, bytes, dict)):
        observed_event_types = [observed_event_types]
    elif not isinstance(observed_event_types, Iterable):
        observed_event_types = []
    observed = {t for t in (_event_type(v) for v in observed_event_types) if t}
    rows = []
    for scenario in CATALOG:
        rows.append({**scenario, "observed": scenario["event_type"] in observed,
                     "status": "telemetry-observed" if scenario["event_type"] in observed else "not-observed"})
    known = {scenario["event_type"] for scenario in CATALOG}
    observed_count = sum(r["observed"] for r in rows)
    total = len(rows)
    return {
        "total": total,
        "observed": observed_count,
        "scenarios": rows,
        "coverage_percent": round(100 * observed_count / total, 1) if total else 0.0,
        "observed_event_types": sorted(observed),
        "unobserved_event_types": sorted(known - observed),
        "unknown_event_types": sorted(observed - known),
    }
