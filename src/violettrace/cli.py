"""Command-line entry point for VioletTrace.

Problems are reported as one-line messages instead of Python tracebacks so the
tool can be used directly in CI pipelines.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .catalog import list_scenarios
from .events import generate_events
from .report import coverage_report

EXIT_OK = 0
EXIT_INVALID_INPUT = 1
EXIT_USAGE = 2

NOTICE = (
    "VioletTrace emits synthetic telemetry only. It does not execute adversary "
    "techniques, establish persistence, evade detection, or modify real systems."
)


def _load_events(path: Path):
    """Read the observed-event fixture, or report the problem."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"violet-trace: cannot read events file {path}: {exc.strerror or exc}"
    try:
        events = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"violet-trace: {path} is not valid JSON: {exc.msg} (line {exc.lineno})"
    if not isinstance(events, list):
        return None, f"violet-trace: {path} must contain a JSON list of events"
    return events, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="violet-trace",
        description="Coverage reporting and synthetic fixture generation for defensive telemetry.",
    )
    parser.add_argument("--events", type=Path, help="JSON file with the observed event types")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Include the generated synthetic event fixture in the report",
    )
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report")
    parser.add_argument(
        "--fail-on-unobserved",
        action="store_true",
        help="Exit with status 1 when at least one catalog scenario has no telemetry",
    )
    args = parser.parse_args(argv)

    events = []
    if args.events is not None:
        events, error = _load_events(args.events)
        if error is not None:
            print(error, file=sys.stderr)
            return EXIT_INVALID_INPUT

    report = {
        "tool": "VioletTrace",
        "mode": "defensive-telemetry-coverage",
        "schema_version": 1,
        "catalog": list_scenarios(),
        "coverage": coverage_report(events),
        "notice": NOTICE,
    }
    if args.generate:
        report["generated_events"] = generate_events()

    rendered = json.dumps(report, indent=2)
    if args.output:
        try:
            args.output.write_text(rendered + "\n", encoding="utf-8")
        except OSError as exc:
            print(
                f"violet-trace: cannot write report to {args.output}: {exc.strerror or exc}",
                file=sys.stderr,
            )
            return EXIT_INVALID_INPUT
    print(rendered)

    if args.fail_on_unobserved and report["coverage"]["unobserved_event_types"]:
        return EXIT_INVALID_INPUT
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
