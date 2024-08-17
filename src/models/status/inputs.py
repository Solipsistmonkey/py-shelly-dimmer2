from pydantic import BaseModel, Field

class InputStatus(BaseModel):
    input: int = Field(
        ...,
        description="Current state of the input",
    )
    event: str = Field(
        ...,
        description="The event type",
    )
    event_counter: int = Field(
        ...,
        description="The event count",
        alias="event_cnt",
    )