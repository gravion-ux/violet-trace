import json
import sys
from pathlib import Path

from violettrace import cli


def test_cli_decodes_events_file_as_utf8(tmp_path, monkeypatch, capsys):
    events=tmp_path/"events.json"
    events.write_text(json.dumps(["créé"],ensure_ascii=False),encoding="utf-8")
    original=Path.read_text

    def legacy_default_read_text(self,*args,**kwargs):
        # emulate a system whose default encoding is not UTF-8
        if "encoding" not in kwargs:
            return self.read_bytes().decode("cp1252")
        return original(self,*args,**kwargs)

    monkeypatch.setattr(Path,"read_text",legacy_default_read_text)
    captured={}

    def fake_coverage(observed):
        captured["events"]=observed
        return {"total":0,"observed":0,"scenarios":[]}

    monkeypatch.setattr(cli,"coverage_report",fake_coverage)
    monkeypatch.setattr(sys,"argv",["violettrace","--events",str(events)])
    cli.main()
    capsys.readouterr()
    assert captured["events"]==["créé"]


def test_cli_prints_a_json_report(tmp_path, capsys):
    code = cli.main([])
    captured = capsys.readouterr()
    assert code == cli.EXIT_OK
    report = json.loads(captured.out)
    assert report["tool"] == "VioletTrace"
    assert report["mode"] == "defensive-telemetry-coverage"
    assert report["schema_version"] == 1
    assert report["coverage"]["total"] == 3
    assert "notice" in report


def test_cli_reads_the_observed_events(tmp_path, capsys):
    events = tmp_path / "events.json"
    events.write_text(json.dumps(["auth_failure"]), encoding="utf-8")
    code = cli.main(["--events", str(events)])
    report = json.loads(capsys.readouterr().out)
    assert code == cli.EXIT_OK
    assert report["coverage"]["observed"] == 1


def test_cli_reports_a_missing_events_file_without_a_traceback(tmp_path, capsys):
    code = cli.main(["--events", str(tmp_path / "absent.json")])
    captured = capsys.readouterr()
    assert code == cli.EXIT_INVALID_INPUT
    assert "violet-trace:" in captured.err
    assert "Traceback" not in captured.err


def test_cli_reports_invalid_json_without_a_traceback(tmp_path, capsys):
    events = tmp_path / "events.json"
    events.write_text("{not json", encoding="utf-8")
    code = cli.main(["--events", str(events)])
    captured = capsys.readouterr()
    assert code == cli.EXIT_INVALID_INPUT
    assert "violet-trace:" in captured.err
    assert "Traceback" not in captured.err


def test_cli_rejects_a_json_root_that_is_not_a_list(tmp_path, capsys):
    events = tmp_path / "events.json"
    events.write_text(json.dumps({"event_type": "auth_failure"}), encoding="utf-8")
    code = cli.main(["--events", str(events)])
    captured = capsys.readouterr()
    assert code == cli.EXIT_INVALID_INPUT
    assert "violet-trace:" in captured.err
    assert "Traceback" not in captured.err


def test_cli_writes_the_report_to_the_output_path(tmp_path, capsys):
    output = tmp_path / "report.json"
    code = cli.main(["--output", str(output)])
    capsys.readouterr()
    assert code == cli.EXIT_OK
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written["tool"] == "VioletTrace"


def test_cli_reports_an_unwritable_output_path_without_a_traceback(tmp_path, capsys):
    output = tmp_path / "missing-directory" / "report.json"
    code = cli.main(["--output", str(output)])
    captured = capsys.readouterr()
    assert code == cli.EXIT_INVALID_INPUT
    assert "violet-trace:" in captured.err
    assert "Traceback" not in captured.err


def test_cli_generates_the_synthetic_fixture_on_request(capsys):
    code = cli.main(["--generate"])
    report = json.loads(capsys.readouterr().out)
    assert code == cli.EXIT_OK
    assert len(report["generated_events"]) == 3
    assert all(event["synthetic"] for event in report["generated_events"])


def test_cli_has_no_generated_fixture_by_default(capsys):
    cli.main([])
    report = json.loads(capsys.readouterr().out)
    assert "generated_events" not in report


def test_cli_fail_on_unobserved_returns_a_failing_status(capsys):
    code = cli.main(["--fail-on-unobserved"])
    capsys.readouterr()
    assert code == cli.EXIT_INVALID_INPUT


def test_cli_fail_on_unobserved_succeeds_on_full_coverage(tmp_path, capsys):
    events = tmp_path / "events.json"
    events.write_text(
        json.dumps(["auth_failure", "privilege_membership_change", "service_created"]),
        encoding="utf-8",
    )
    code = cli.main(["--events", str(events), "--fail-on-unobserved"])
    capsys.readouterr()
    assert code == cli.EXIT_OK
