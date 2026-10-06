import argparse
import json
from datetime import UTC, datetime

from .core.store import Store
from .pipeline import evaluate


def dt(value):
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def main():
    parser = argparse.ArgumentParser(prog="psychohistory")
    parser.add_argument("--db", default="registry/psychohistory.db")
    sub = parser.add_subparsers(dest="cmd", required=True)
    evaluate_parser = sub.add_parser("evaluate")
    evaluate_parser.add_argument("--as-of", required=True)
    args = parser.parse_args()
    store = Store(args.db)
    if args.cmd == "evaluate":
        print(json.dumps(evaluate(store, dt(args.as_of)), indent=2))


if __name__ == "__main__":
    main()
