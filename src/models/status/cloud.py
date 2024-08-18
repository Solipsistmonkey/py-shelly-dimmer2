"""
Cloud Status Model.

This module defines the `CloudStatus` model, representing the status of
the cloud connection of a Shelly device.
"""

from pydantic import BaseModel, Field

class CloudStatus(BaseModel):
    """
    A model representing the cloud connection status.

    Attributes
    ----------
    enabled : bool
        Whether the device is connected to the cloud.
    connected : bool
        Whether the device is currently connected to the cloud.
    """

    enabled: bool = Field(
        False,
        description="Whether the device is connected to the cloud",
    )
    connected: bool = Field(
        False,
        description="Whether the device is connected to the cloud",
    )
