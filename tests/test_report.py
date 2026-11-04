from violettrace.catalog import list_scenarios
from violettrace.report import coverage_report


def test_coverage_counts_observed():
    report=coverage_report(["auth_failure"])
    assert report["observed"]==1 and report["total"]==3


def test_list_scenarios_does_not_expose_mutable_global_state():
    scenarios=list_scenarios()
    scenarios[0]["name"]="MUTATED"
    assert list_scenarios()[0]["name"]!="MUTATED"


def test_coverage_accepts_event_objects():
    report=coverage_report([{"event_type":"auth_failure"}])
    assert report["observed"]==1


def test_coverage_accepts_single_event_string():
    report=coverage_report("auth_failure")
    assert report["observed"]==1


def test_coverage_ignores_unusable_event_values():
    report=coverage_report([None,{"event_type":None},42])
    assert report["observed"]==0 and report["total"]==3
