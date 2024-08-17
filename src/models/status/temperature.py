from pydantic import BaseModel, Field

class TempStatus(BaseModel):
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
        description="Whether the temperature meter self-checks OK",
    )