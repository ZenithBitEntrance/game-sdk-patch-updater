"""Patch descriptor. One edge in the SDK version graph."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PatchDescriptor(BaseModel):
    version: str           # patch identifier / release tag
    from_version: str      # SDK version this patch applies to
    to_version: str        # SDK version this patch produces
    summary: str
    blob_url: str
    sha256: str | None = None
    size_bytes: int | None = None
    targets: list[str] = Field(default_factory=list)
    notes: str | None = None

    model_config = {"extra": "forbid"}