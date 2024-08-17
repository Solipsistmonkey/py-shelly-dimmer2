from pydantic import BaseModel, Field

class LightStatus(BaseModel):
    is_on: bool = Field(
        ...,
        description="Whether the light is on or off",
        alias="ison",
        repr=True,
    )
    source: str = Field(
        ...,
        description="The source of the light (e.g. cloud, http)",
        repr=False,
    )
    has_timer: bool = Field(
        ...,
        description="Whether the light has a timer",
        repr=False,
    )
    timer_started: int = Field(
        ...,
        description="The time the timer started",
        repr=False,
    )
    timer_duration: int = Field(
        ...,
        description="The duration of the timer",
        repr=False,
    )
    timer_remaining: int = Field(
        ...,
        description="The remaining time on the timer",
        repr=False,
    )
    mode: str = Field(
        "white"
        , description="The mode of the light",
        repr=False,
    )
    brightness: int = Field(
        100,
        description="The brightness of the light in percent",
        repr=True,
    )
    transition: int = Field(
        400,
        description="The transition time in milliseconds",
        repr=True,
    )


