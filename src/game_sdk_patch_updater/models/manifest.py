"""Channel manifest model. One manifest per channel, versioned by release."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .patch import PatchDescriptor


class ChannelManifest(BaseModel):
    channel: str
    head_version: str
    published_at: str
    patches: list[PatchDescriptor] = Field(default_factory=list)
    sdk_platform: str = "windows-x64"

    model_config = {"extra": "forbid"}