# VioletTrace

> A safe purple-team validation harness for defensive telemetry and detection-rule tests.

**Status:** MVP scaffold / research prototype. Not production-certified.

## Features
- Declarative simulation catalog.
- Safe local event fixture generation.
- Sigma-like detection metadata mapping.
- Coverage reporting for defensive controls.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
```

## Command-line usage

```bash
violet-trace                                        # catalog and an empty coverage report
violet-trace --events observed.json                 # review an observed-event fixture
violet-trace --events observed.json --output report.json
violet-trace --generate                             # include the synthetic event fixture
violet-trace --events observed.json --fail-on-unobserved
```

| Exit code | Meaning |
| --- | --- |
| `0` | The report was produced. |
| `1` | The events file could not be read or parsed, the report could not be written, or `--fail-on-unobserved` was given and a scenario has no telemetry. |
| `2` | The command line itself was wrong. |

Problems are reported as one-line messages. The command never prints a Python
traceback, so it can be used directly in a CI pipeline.

The events file must contain a JSON list. A list of event type strings and a list
of event objects with an `event_type` field are both accepted.

## Coverage report

| Field | Meaning |
| --- | --- |
| `total` | Number of scenarios in the catalog. |
| `observed` | Number of catalog scenarios for which telemetry was seen. |
| `coverage_percent` | Share of the catalog covered by the observed telemetry. |
| `observed_event_types` | Every event type that was seen, sorted. |
| `unobserved_event_types` | Catalog scenarios without telemetry. |
| `unknown_event_types` | Observed event types that are not in the catalog. |

An unknown event type is reported instead of being dropped: an event the catalog
does not know about is a gap in the catalog and has to stay visible.

## Python API

```python
from violettrace import coverage_report, generate_events, list_scenarios

for scenario in list_scenarios():
    print(scenario["id"], scenario["event_type"], scenario["sigma"]["level"])

fixture = generate_events()
report = coverage_report(fixture)
print(report["observed"], "of", report["total"], "scenarios covered")
```

`generate_events()` is deterministic: the same request always produces the same
fixture. Every generated event is marked `"synthetic": true` and carries the
scenario identifier, the technique identifier, a host name and a timestamp.

## Safety and scope
The MVP emits synthetic events and does not execute adversary techniques, establish persistence, evade detection, or modify real systems.

## Roadmap
- [x] Stable public API and versioned schemas
- [x] More unit, integration and adversarial tests
- [ ] Reproducible benchmarks and sample datasets
- [ ] Signed releases and dependency review
- [x] Documentation and contribution guide

## License
MIT. See [LICENSE](LICENSE). The license file carries the complete MIT text, including the warranty and liability clauses.
