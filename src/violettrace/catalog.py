"""Declarative simulation catalog for VioletTrace.

Every scenario describes a synthetic, defensive-only event. The catalog holds
no executable technique and no real indicator.
"""
import copy

__all__ = ["CATALOG", "list_scenarios", "scenario_ids"]

CATALOG = [
  {"id":"PL001","name":"Repeated authentication failures","technique":"T1110","event_type":"auth_failure",
   "description":"Synthetic event fixture for validating failed-login telemetry.",
   "sigma":{"title":"VioletTrace synthetic authentication failures","level":"high",
            "logsource":{"product":"violet-trace","service":"synthetic-telemetry"},
            "detection":{"selection":{"event_type":"auth_failure"}},
            "fields":["event_type","scenario_id","host","timestamp"],
            "falsepositives":["Synthetic fixture events only"]}},
  {"id":"PL002","name":"New privileged group membership","technique":"T1098",
   "event_type":"privilege_membership_change","description":"Synthetic fixture for privilege-change monitoring.",
   "sigma":{"title":"VioletTrace synthetic privileged group membership","level":"high",
            "logsource":{"product":"violet-trace","service":"synthetic-telemetry"},
            "detection":{"selection":{"event_type":"privilege_membership_change"}},
            "fields":["event_type","scenario_id","host","timestamp"],
            "falsepositives":["Synthetic fixture events only"]}},
  {"id":"PL003","name":"Unexpected service creation","technique":"T1543",
   "event_type":"service_created","description":"Synthetic fixture for service-installation telemetry.",
   "sigma":{"title":"VioletTrace synthetic service creation","level":"medium",
            "logsource":{"product":"violet-trace","service":"synthetic-telemetry"},
            "detection":{"selection":{"event_type":"service_created"}},
            "fields":["event_type","scenario_id","host","timestamp"],
            "falsepositives":["Synthetic fixture events only"]}}
]


def list_scenarios():
    # Deep copy so callers cannot mutate the shared catalog.
    return copy.deepcopy(CATALOG)


def scenario_ids():
    """Return the catalog identifiers in catalog order."""
    return [scenario["id"] for scenario in CATALOG]
