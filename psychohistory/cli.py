import argparse
import json
from datetime import datetime

from .core.store import Store
from .core.validation import _aware_instant
from .pipeline import evaluate


def dt(value):
    parsed = datetime.fromisoformat(value)
    # A wall clock without an offset is not a verified information cutoff.
    # Do not quietly turn it into UTC and shift the point-in-time evidence set.
    if not _aware_instant(parsed):
        raise ValueError("--as-of must include an explicit timezone offset or Z")
    return parsed


def main():
    parser = argparse.ArgumentParser(prog="psychohistory")
    parser.add_argument("--db", default="registry/psychohistory.db")
    sub = parser.add_subparsers(dest="cmd", required=True)
    evaluation = sub.add_parser("evaluate")
    evaluation.add_argument("--as-of", required=True)
    args = parser.parse_args()
    store = Store(args.db)
    if args.cmd == "evaluate":
        print(json.dumps(evaluate(store, dt(args.as_of)), indent=2))


if __name__ == "__main__":
    main()
