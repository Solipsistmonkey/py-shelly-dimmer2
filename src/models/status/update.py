"""
Update Status Model.

This module defines the `UpdateStatus` model, representing the update
status of a Shelly device.
"""

from pydantic import BaseModel, Field

class UpdateStatus(BaseModel):
    """
    A model representing the update status.

    Attributes
    ----------
    status : str
        The status of the update.
    has_update : bool
        Whether an update is available.
    new_version : str
        The new version available.
    old_version : str
        The current version.
    beta_version : str
        The beta version available.
    """

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
