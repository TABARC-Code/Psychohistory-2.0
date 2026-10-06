import json
from datetime import datetime
from pathlib import Path

from .core.models import Forecast, Observation
from .core.store import Store


def load_seed(store, root="."):
    root = Path(root)
    housing = json.loads((root / "data/seed/uk_housing_credit_2026.json").read_text())
    for row in housing["observations"]:
        month = row["month"]
        store.add_observation(
            Observation(
                observation_id=f"BOE_APPROVALS_{month}",
                series=housing["series"],
                effective_at=datetime.fromisoformat(f"{month}-01T00:00:00+00:00"),
                available_at=datetime.fromisoformat(row["available_at"]),
                value=row["value"],
                source="Bank of England Money and Credit",
                vintage="first_release",
                revision_type="none",
                pipeline_position="approval",
                ancestry=(f"UK_MORTGAGE_APPROVAL_EVENT_{month}",),
            )
        )

    for line in (root / "registry/forecast_ledger.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        store.add_forecast(
            Forecast(
                forecast_id=row["forecast_id"],
                event_id=row["event_id"],
                origin=datetime.fromisoformat(row["origin"]),
                horizon_end=datetime.fromisoformat(row["horizon_end"]),
                probability=row["probability"],
                model=row["model"],
                baseline_probability=row["baseline_probability"],
            )
        )


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="registry/psychohistory.db")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    load_seed(Store(args.db), args.root)


if __name__ == "__main__":
    main()
