"""Local install state. Persisted to .sdkstate in the SDK install root."""

from __future__ import annotations

from pydantic import BaseModel

from .patch import PatchDescriptor


class InstallState(BaseModel):
    sdk_version: str = "0.0.0"
    channel: str = "stable"
    applied: list[PatchDescriptor] = []
    last_check_utc: str | None = None

    model_config = {"extra": "ignore"}