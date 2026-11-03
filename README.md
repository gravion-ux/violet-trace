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

## Safety and scope
The MVP emits synthetic events and does not execute adversary techniques, establish persistence, evade detection, or modify real systems.

## Roadmap
- [ ] Stable public API and versioned schemas
- [ ] More unit, integration and adversarial tests
- [ ] Reproducible benchmarks and sample datasets
- [ ] Signed releases and dependency review
- [ ] Documentation and contribution guide

## License
MIT. See [LICENSE](LICENSE).
