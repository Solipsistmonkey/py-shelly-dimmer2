"""
Input Status Model.

This module defines the `InputStatus` model, representing the status of an
input in the Shelly device.
"""

from pydantic import BaseModel, Field

class InputStatus(BaseModel):
    """
    A model representing the status of an input.

    Attributes
    ----------
    input : int
        The current state of the input.
    event : str
        The event type associated with the input.
    event_counter : int
        The event count, alias "event_cnt".
    """

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
