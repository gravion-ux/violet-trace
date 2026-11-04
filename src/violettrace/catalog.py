import copy

CATALOG = [
  {"id":"PL001","name":"Repeated authentication failures","technique":"T1110","event_type":"auth_failure",
   "description":"Synthetic event fixture for validating failed-login telemetry."},
  {"id":"PL002","name":"New privileged group membership","technique":"T1098",
   "event_type":"privilege_membership_change","description":"Synthetic fixture for privilege-change monitoring."},
  {"id":"PL003","name":"Unexpected service creation","technique":"T1543",
   "event_type":"service_created","description":"Synthetic fixture for service-installation telemetry."}
]
def list_scenarios():
    # Deep copy so callers cannot mutate the shared catalog.
    return copy.deepcopy(CATALOG)
