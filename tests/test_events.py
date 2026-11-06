import importlib

from violettrace.catalog import list_scenarios


def _events():
    """Return the event generator module at runtime.

    Resolving the module inside the test keeps a missing module a test
    failure instead of a collection error.
    """
    return importlib.import_module("violettrace.events")


def test_an_event_is_generated_for_every_scenario():
    events = _events().generate_events()
    assert len(events) == len(list_scenarios())
    assert [event["event_type"] for event in events] == [
        scenario["event_type"] for scenario in list_scenarios()
    ]


def test_generated_events_are_marked_as_synthetic():
    for event in _events().generate_events():
        assert event["synthetic"] is True
        assert event["scenario_id"]
        assert event["technique"]
        assert event["host"]
        assert event["timestamp"].endswith("Z")


def test_the_generated_fixture_is_deterministic():
    module = _events()
    assert module.generate_events() == module.generate_events()


def test_a_subset_of_scenarios_can_be_selected():
    events = _events().generate_events(["PL001"])
    assert len(events) == 1
    assert events[0]["scenario_id"] == "PL001"


def test_an_unknown_scenario_id_is_ignored():
    assert _events().generate_events(["PL999"]) == []


def test_the_host_can_be_overridden():
    events = _events().generate_events(host="lab-42")
    assert {event["host"] for event in events} == {"lab-42"}


def test_the_generated_fixture_covers_every_scenario():
    module = _events()
    events = module.generate_events()
    assert {event["event_type"] for event in events} == {
        scenario["event_type"] for scenario in list_scenarios()
    }
