from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from .validation import _aware_instant


@dataclass(frozen=True)
class Observation:
    observation_id: str
    series: str
    effective_at: datetime
    available_at: datetime
    value: float
    source: str
    vintage: str = "first"
    revision_type: str = "none"
    quality: float = 1.0
    pipeline_position: str | None = None
    ancestry: tuple[str, ...] = ()
    evidence_role: str = "measurement"
    content_ancestry: tuple[str, ...] = ()
    carrier: str | None = None
    actor_id: str | None = None
    community_id: str | None = None
    semantic_variant: str | None = None

    def visible(self, as_of: datetime) -> bool:
        """Return point-in-time visibility using absolute UTC instants."""
        available = self.available_at
        if not _aware_instant(available) or not _aware_instant(as_of):
            raise ValueError("visibility requires UTC-convertible aware datetimes")
        return available.astimezone(UTC) <= as_of.astimezone(UTC)

    @property
    def is_propagation(self) -> bool:
        return self.evidence_role == "propagation"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["effective_at"] = self.effective_at.isoformat()
        data["available_at"] = self.available_at.isoformat()
        return data


@dataclass(frozen=True)
class OutcomeContract:
    event_id: str
    observable: str
    horizon_days: int
    threshold: float
    direction: str = "ge"
    vintage_policy: str = "first_release"


@dataclass(frozen=True)
class Forecast:
    forecast_id: str
    event_id: str
    origin: datetime
    horizon_end: datetime
    probability: float
    model: str
    baseline_probability: float | None = None
