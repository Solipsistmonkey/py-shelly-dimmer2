"""
`models` Package.

This package contains models representing various aspects of the Shelly
device status, including light status, input status, meter status, MQTT
status, temperature status, and more. These models are used for data
validation and serialization.
"""

from .light import LightStatus
from .status import Status

__all__ = ["Status", "LightStatus"]