"""
Wi-Fi Status Model.

This module defines the `WifiStatus` model, representing the Wi-Fi
connection status of a Shelly device.
"""

from pydantic import BaseModel, Field, IPvAnyAddress, NegativeInt

class WifiStatus(BaseModel):
    """
    A model representing the Wi-Fi connection status.

    Attributes
    ----------
    connected : bool
        Whether the device is connected to Wi-Fi.
    ssid : str
        The name of the Wi-Fi network.
    ip : IPvAnyAddress
        The IP address assigned to the device.
    rssi : NegativeInt
        The signal strength of the Wi-Fi network.
    """

    connected: bool = Field(
        True,
        description="Whether the device is connected to Wi-Fi",
    )
    ssid: str = Field(
        "",
        description="The name of the Wi-Fi network",
    )
    ip: IPvAnyAddress = Field(
        "192.168.1.99",
        description="The IP address assigned to the device",
    )
    rssi: NegativeInt = Field(
        -60,
        description="The signal strength of the Wi-Fi network",
    )
