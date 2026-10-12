from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: Annotated[int, Field(ge=18, le=80)]
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: Annotated[int, Field(ge=0, le=50)]
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: Annotated[int, Field(ge=1, le=3650)]
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: Annotated[float, Field(ge=1.0, le=10000.0)]

    @model_validator(mode="after")
    def mission_validator(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        if not any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced_count = sum(
                1
                for member in self.crew
                if member.years_experience >= 5
            )
            if experienced_count < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced "
                    "crew (5+ years)"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def error_message(error: ValidationError) -> str:
    detail = error.errors()[0]
    ctx = detail.get("ctx")
    if ctx and "error" in ctx:
        return str(ctx["error"])
    return detail["msg"]


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2028, 5, 15),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="CM001",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=42,
                    specialization="Mission Command",
                    years_experience=18,
                ),
                CrewMember(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=10,
                ),
                CrewMember(
                    member_id="CM003",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=31,
                    specialization="Engineering",
                    years_experience=7,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )
    except ValidationError as e:
        print(error_message(e))

    print("\n=========================================")

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Failed Mission",
            destination="Moon",
            launch_date=datetime(2028, 1, 1),
            duration_days=100,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Wilson",
                    rank=Rank.officer,
                    age=28,
                    specialization="Engineering",
                    years_experience=4,
                ),
                CrewMember(
                    member_id="CM005",
                    name="Mary Jones",
                    rank=Rank.lieutenant,
                    age=33,
                    specialization="Science",
                    years_experience=8,
                ),
            ],
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(error_message(e))


if __name__ == "__main__":
    main()
