from pydantic import BaseModel, Field

class MQTTStatus(BaseModel):
    connected: bool = Field(
        ...,
        description="Whether the MQTT connection is established",
    )