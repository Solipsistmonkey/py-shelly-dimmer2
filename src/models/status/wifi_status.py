from pydantic import BaseModel, Field, IPvAnyAddress, NegativeInt


class WifiStatus(BaseModel):
    connected: bool = Field(
        True, description="Whether the device is connected to WiFi", )
    ssid: str = Field(
        "", description="The name of the WiFi network", )
    ip: IPvAnyAddress = Field(
        "192.168.1.99", description="The IP address assigned to the device", )
    rssi: NegativeInt = Field(
        -60, description="The signal strength of the WiFi network", )


