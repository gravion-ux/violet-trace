from collections.abc import Iterable

from .catalog import CATALOG


def _event_type(value):
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        value = value.get("event_type")
        return value.strip() if isinstance(value, str) and value.strip() else None
    return None


def coverage_report(observed_event_types):
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
    return {"total": len(rows), "observed": sum(r["observed"] for r in rows), "scenarios": rows}
