"""
MQTT Status Model.

This module defines the `MQTTStatus` model, representing the MQTT
connection status of a Shelly device.
"""

from pydantic import BaseModel, Field

class MQTTStatus(BaseModel):
    """
    A model representing the MQTT connection status.

    Attributes
    ----------
    connected : bool
        Whether the MQTT connection is established.
    """

    connected: bool = Field(
        ...,
        description="Whether the MQTT connection is established",
    )
