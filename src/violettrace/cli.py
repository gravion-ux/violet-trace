import argparse
import json
from pathlib import Path

from .catalog import list_scenarios
from .report import coverage_report


def main():
    p=argparse.ArgumentParser();p.add_argument("--events",type=Path);a=p.parse_args()
    events=json.loads(a.events.read_text(encoding="utf-8")) if a.events else []
    print(json.dumps({"catalog":list_scenarios(),"coverage":coverage_report(events)},indent=2))
if __name__=="__main__":main()
