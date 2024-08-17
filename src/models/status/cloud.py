from pydantic import BaseModel, Field

class CloudStatus(BaseModel):
    enabled: bool = Field(
        False,
        description="Whether the device is connected to the cloud",
    )
    connected: bool = Field(
        False,
        description="Whether the device is connected to the cloud",
    )
