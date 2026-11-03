from violettrace.report import coverage_report


def test_coverage_counts_observed():
    report=coverage_report(["auth_failure"])
    assert report["observed"]==1 and report["total"]==3
