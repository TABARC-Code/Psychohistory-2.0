from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class Observation:
    observation_id:str; series:str; effective_at:datetime; available_at:datetime; value:float
    source:str; vintage:str="first"; revision_type:str="none"; quality:float=1.0
    pipeline_position:str|None=None; ancestry:tuple[str,...]=()
    def visible(self, as_of:datetime)->bool: return self.available_at <= as_of
    def to_dict(self)->dict[str,Any]:
        d=asdict(self); d["effective_at"]=self.effective_at.isoformat(); d["available_at"]=self.available_at.isoformat(); return d

@dataclass(frozen=True)
class OutcomeContract:
    event_id:str; observable:str; horizon_days:int; threshold:float; direction:str="ge"; vintage_policy:str="first_release"

@dataclass(frozen=True)
class Forecast:
    forecast_id:str; event_id:str; origin:datetime; horizon_end:datetime; probability:float; model:str; baseline_probability:float|None=None
