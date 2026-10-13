"""Read/write the local SDK patch state file (.sdkstate)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config_loader import load_runtime
from ..models.patch import PatchDescriptor
from ..utils.logging import get_logger

log = get_logger(__name__)


class StateService:
    def __init__(self, root: Path, channel: str, cache_dir: Path):
        self.root = root
        self.channel = channel
        self.cache_dir = cache_dir
        self.state_path = root / ".sdkstate"

    @classmethod
    def from_context(cls, ctx: dict[str, Any]) -> "StateService":
        runtime = load_runtime()
        root = Path(ctx.get("root") or runtime["install"]["root"])
        cache_dir = Path(runtime["install"]["cache_dir"])
        return cls(root=root, channel=ctx["channel"], cache_dir=cache_dir)

    def _read(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {"sdk_version": "0.0.0", "applied": []}
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def local_sdk_version(self) -> str:
        return self._read()["sdk_version"]

    def applied_patches(self) -> list[PatchDescriptor]:
        return [PatchDescriptor.model_validate(p) for p in self._read().get("applied", [])]

    def record_applied(self, patch: PatchDescriptor) -> None:
        data = self._read()
        data["applied"].append(patch.model_dump())
        data["sdk_version"] = patch.to_version
        self._write(data)

    def record_rolled_back(self, patch: PatchDescriptor) -> None:
        data = self._read()
        data["applied"] = [p for p in data["applied"] if p["version"] != patch.version]
        data["sdk_version"] = patch.from_version
        self._write(data)