import importlib

from violettrace.catalog import list_scenarios


def _catalog():
    """Return the catalog module at runtime."""
    return importlib.import_module("violettrace.catalog")


def test_every_scenario_carries_detection_metadata():
    for scenario in list_scenarios():
        assert scenario["id"]
        assert scenario["event_type"]
        assert scenario["technique"]
        assert scenario["description"]


def test_every_scenario_carries_sigma_like_metadata():
    for scenario in list_scenarios():
        sigma = scenario["sigma"]
        assert sigma["title"]
        assert sigma["logsource"]["product"]
        assert sigma["detection"]["selection"]["event_type"] == scenario["event_type"]
        assert "event_type" in sigma["fields"]
        assert sigma["level"] in {"informational", "low", "medium", "high", "critical"}


def test_the_scenario_ids_are_unique():
    ids = [scenario["id"] for scenario in list_scenarios()]
    assert len(ids) == len(set(ids))


def test_the_catalog_module_exposes_the_scenario_ids():
    catalog = _catalog()
    assert catalog.scenario_ids() == [scenario["id"] for scenario in list_scenarios()]


def test_a_mutated_catalog_entry_does_not_change_the_catalog():
    scenarios = list_scenarios()
    scenarios[0]["sigma"]["detection"]["selection"]["event_type"] = "MUTATED"
    assert list_scenarios()[0]["sigma"]["detection"]["selection"]["event_type"] != "MUTATED"
