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
