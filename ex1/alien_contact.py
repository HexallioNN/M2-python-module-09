from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum
from typing import Self


class ContactType(Enum):
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: Annotated[float, Field(ge=0.0, le=10.0)]
    duration_minutes: Annotated[int, Field(ge=1, le=1440)]
    witness_count: Annotated[int, Field(ge=1, le=100)]
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                'Contact ID must start with "AC" (Alien Contact)')
        if (
            self.contact_type == ContactType.physical
            and not self.is_verified
        ):
            raise ValueError(
                "Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if (
            self.signal_strength > 7.0
            and self.message_received is None
        ):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")

        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False
    )
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.name}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")

    print("======================================")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Unknown Sector",
            contact_type=ContactType.telepathic,
            signal_strength=5.0,
            duration_minutes=20,
            witness_count=1,
            message_received="We come in peace",
            is_verified=True
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])
