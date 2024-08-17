from pydantic import BaseModel, Field

class Light(BaseModel):
    ison: bool = Field(
        ...,
        description="Whether the light is on or off",
    )
    source: str = Field(
        ...,
        description="The source of the light",
    )
    has_timer: bool = Field(
        ...,
        description="Whether the light has a timer",
    )
    timer_started: int = Field(
        ...,
        description="The time the timer started",
    )
    timer_duration: int = Field(
        ...,
        description="The duration of the timer",
    )
    timer_remaining: int = Field(
        ...,
        description="The remaining time on the timer",
    )
    mode: str = Field(
        "white"
        , description="The mode of the light",
    )
    brightness: int = Field(
        100,
        description="The brightness of the light in percent",
    )
    transition: int = Field(
        400,
        description="The transition time in milliseconds",
    )