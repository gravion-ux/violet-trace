# Remediation notes — 2026-11

This document records the audit and remediation applied to VioletTrace in November 2026.
It is additive: the original README, SECURITY.md, CONTRIBUTING.md and example files
remain in the repository and were updated only where they were inaccurate or
inconsistent.

## Method

Every source file was read line by line and each suspected defect was confirmed with
an executable regression test. The new tests were first run against the previously
published revision to confirm the defect was real (red phase: 26 failing tests), and
only then were the fixes applied (green phase: 34 passing tests).

## Defects fixed

| Severity | Defect | Fix |
| --- | --- | --- |
| Medium | The command line raised a raw Python traceback for a missing events file, for invalid JSON, and for an unwritable report file | `cli.main` reports one-line messages and uses exit codes `0` / `1` / `2` |
| Medium | A JSON document whose root was not a list was accepted silently and produced an empty coverage report, which looked like a clean run | The root must be a JSON list; anything else is reported as an error |
| Medium | The README promised "safe local event fixture generation", but the project had no event generator at all | New `violettrace.events` module with a deterministic `generate_events()`, exposed with `--generate` |
| Medium | The README promised "Sigma-like detection metadata mapping", but the catalog only carried a technique identifier | Every scenario now carries a `sigma` block with title, level, log source, detection selection and fields |
| Low | The command line read `sys.argv` directly, so it could not be called as a function and could not be tested | `cli.main(argv)` accepts an argument list and falls back to `sys.argv` |
| Low | A report could not be written to a file and a CI pipeline had no way to fail on a coverage gap | `--output` and `--fail-on-unobserved` options, with an explicit error when the report cannot be written |
| Low | An observed event type that was not part of the catalog was dropped without a trace, so a gap in the catalog was invisible | The report lists `unknown_event_types` beside `unobserved_event_types` |
| Low | The coverage report gave only a count, so a reader could not tell which scenarios were missing | The report adds `coverage_percent`, `observed_event_types` and `unobserved_event_types` |
| Low | The package exposed no public API and the report carried no format marker | `violettrace.__all__`, `violettrace.__version__`, and `schema_version` in the report |

## Documentation and spelling corrections

- `LICENSE` shipped a truncated MIT text: the warranty and liability clauses were
  missing. The complete, canonical MIT text is now in place.
- Spelling was inconsistent across the same file set (`behaviour` in `CONTRIBUTING.md`
  against `authorization` in `SECURITY.md` and `normalized` in `README.md`). The
  prose now uses one convention throughout: American English.
- The roadmap listed "Documentation and contribution guide" as unfinished while
  `CONTRIBUTING.md`, `SECURITY.md` and this file exist. The checklist now reflects
  reality, and "Stable public API and versioned report schema" is marked complete.
- The README documented no command-line usage, no exit codes and no explanation of
  the coverage report. All three are now documented.
- A dictionary spelling scan (`codespell`) now reports no misspelling in this
  repository.

## Continuous integration hardening

The workflow previously ran the test suite only. It now also runs a credential scan
on every push and pull request.

| Job | What it does |
| --- | --- |
| `secret-scan` | Runs `scripts/scan-secrets.py`, which fails the build when the repository contains a high-confidence credential pattern (cloud keys, tokens, private key blocks, JWTs) or a file that must never be committed (`.env`, `*.pem`, `*.key`, `*.p12`, `id_rsa`, credential files) |

The scanner is the one already used by the Gravion Toolkit split repositories, so
every toolkit project now shares one definition of what counts as a secret. A
"soft" match, such as a dummy `api_key` inside a test fixture, is reported for
review but does not fail the build.

## Verification

| Check | Before | After |
| --- | --- | --- |
| Secret scan in CI | absent | present |
| Tests | 8 | 34 |
| `ruff check .` | clean | clean |
| Modules | `catalog`, `report` | `catalog`, `events`, `report` |
| Promised features implemented | 2 of 4 | 4 of 4 |

## Residual limitations

- The catalog holds three synthetic scenarios. Coverage is measured against that
  catalog only, so a high percentage says nothing about a real detection program.
- The Sigma-like metadata is a mapping shape, not a runnable Sigma rule. It is not
  exported to a `.yml` file and it has not been validated by a Sigma engine.
- The generated fixture is deterministic and synthetic. It carries no real
  indicator and is not meant to be replayed against a production telemetry source.
- Event types are matched exactly, after trimming surrounding whitespace. A
  telemetry source that changes the case of an event type is reported as an
  unknown event type rather than as a covered scenario.
