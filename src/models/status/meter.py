from typing import List
from pydantic import BaseModel, Field

class MeterStatus(BaseModel):
    power: float = Field(
        ...,
        description="The current power usage in watts",
    )
    overpower: float = Field(
        ...,
        description=(
            "Value in watts on which an overpower condition is detected"
        ),
    )
    is_valid: bool = Field(
        ...,
        description="Whether the power metering self-check has passed",
    )
    timestamp: int = Field(
        ...,
        description="The timestamp of the last power measurement",
    )
    counters: List[float] = Field(
        ...,
        description="The counters for the meter",
    )
    total: float = Field(
        ...,
        description="The total power usage in kWh",
    )