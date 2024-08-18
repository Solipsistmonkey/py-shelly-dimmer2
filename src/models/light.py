"""
Light Status Model.

This module defines the `LightStatus` model, representing the status of a light in the Shelly device.
"""

from pydantic import BaseModel, Field


class LightStatus(BaseModel):
    """
    A model representing the status of a light.

    Attributes
    ----------
    is_on : bool
        Whether the light is on or off.
    source : str
        The source of the light (e.g., cloud, http).
    has_timer : bool
        Whether the light has a timer.
    timer_started : int
        The time the timer started.
    timer_duration : int
        The duration of the timer.
    timer_remaining : int
        The remaining time on the timer.
    mode : str
        The mode of the light (default is "white").
    brightness : int
        The brightness of the light in percent.
    transition : int
        The transition time in milliseconds.
    """

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
        "white",
        description="The mode of the light",
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
