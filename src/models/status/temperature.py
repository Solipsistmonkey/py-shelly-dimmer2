"""
Temperature Status Model.

This module defines the `TempStatus` model, representing the temperature
status of a Shelly device.
"""

from pydantic import BaseModel, Field

class TempStatus(BaseModel):
    """
    A model representing the temperature status.

    Attributes
    ----------
    celcius : float
        The temperature in Celsius (alias "tC").
    fahrenheit : float
        The temperature in Fahrenheit (alias "tF").
    is_valid : bool
        Whether the temperature meter self-check is OK.
    """

    celcius: float = Field(
        ...,
        description="The temperature in celcius",
        alias="tC",
    )
    fahrenheit: float = Field(
        ...,
        description="The temperature in fahrenheit",
        alias="tF",
    )
    is_valid: bool = Field(
        ...,
        description="Whether the temperature meter self-check is OK",
    )
