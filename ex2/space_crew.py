from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum
from typing import Self


class Rank(Enum):
    cadet = 1
    officer = 2
    lituenant = 3
    captain = 4
    commander = 5


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age = Annotated[int, Field(ge=18, le=80)]
    specialization = Field(min_length=3, max_length=30)
    years_experience = Annotated[int, Field(ge=0, le=50)]
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: Annotated[int, Field(ge=1, le=3650)]
    crew: list[CrewMember] = Field(min_items=1, max_items=12)
    mission_status: str = "planned"
    budget_millions: Annotated[float, Field(ge=1.0, le=10000.0)]
