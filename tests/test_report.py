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


def test_coverage_reports_the_unobserved_scenarios():
    report=coverage_report(["auth_failure"])
    assert report["unobserved_event_types"]==["privilege_membership_change","service_created"]


def test_coverage_reports_an_unknown_event_type():
    report=coverage_report(["auth_failure","unmapped_signal"])
    assert report["unknown_event_types"]==["unmapped_signal"]
    assert report["observed"]==1


def test_coverage_reports_a_percentage():
    report=coverage_report(["auth_failure"])
    assert report["coverage_percent"]==round(100/3,1)


def test_coverage_lists_the_observed_event_types():
    report=coverage_report(["auth_failure","service_created"])
    assert report["observed_event_types"]==["auth_failure","service_created"]


def test_coverage_of_an_empty_catalog_is_zero_percent():
    report=coverage_report([])
    assert report["coverage_percent"]==0.0
    assert report["unknown_event_types"]==[]
