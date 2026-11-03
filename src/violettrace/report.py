from .catalog import CATALOG


def coverage_report(observed_event_types):
    observed=set(observed_event_types)
    rows=[]
    for scenario in CATALOG:
        rows.append({**scenario,"observed":scenario["event_type"] in observed,
                     "status":"telemetry-observed" if scenario["event_type"] in observed else "not-observed"})
    return {"total":len(rows),"observed":sum(r["observed"] for r in rows),"scenarios":rows}
