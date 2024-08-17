from pydantic import BaseModel, Field

class UpdateStatus(BaseModel):
    status: str = Field(
        ...,
        description="The status of the update",
    )
    has_update: bool = Field(
        ...,
        description="Whether an update is available",
    )
    new_version: str = Field(
        ...,
        description="The new version available",
    )
    old_version: str = Field(
        ...,
        description="The current version",
    )
    beta_version: str = Field(
        ...,
        description="The beta version available",
    )
