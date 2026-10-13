"""Download, verify, and apply patch blobs to the SDK install root."""

from __future__ import annotations

from pathlib import Path

from ..adapters.filelock_adapter import FileLockAdapter
from ..adapters.patch_apply_adapter import PatchApplyAdapter
from ..models.patch import PatchDescriptor
from ..utils.hashing import sha256_file
from ..utils.logging import get_logger
from .patch_chain_service import PatchChainService
from .state_service import StateService

log = get_logger(__name__)


class InstallService:
    def __init__(self, state: StateService, chain: PatchChainService | None):
        self.state = state
        self.chain = chain
        self.applier = PatchApplyAdapter(state.root)
        self.lock = FileLockAdapter(state.root / ".patch.lock")

    def apply_patch(self, patch: PatchDescriptor) -> None:
        with self.lock:
            blob = self._download_blob(patch)
            digest = sha256_file(blob)
            if digest != patch.sha256:
                raise ValueError(
                    f"patch {patch.version} blob hash mismatch: "
                    f"expected {patch.sha256}, got {digest}"
                )
            self.applier.apply(blob, patch)
            self.state.record_applied(patch)
            log.info("patch %s applied", patch.version)

    def rollback_patch(self, patch: PatchDescriptor) -> None:
        with self.lock:
            self.applier.revert(patch)
            self.state.record_rolled_back(patch)
            log.info("patch %s rolled back", patch.version)

    def _download_blob(self, patch: PatchDescriptor) -> Path:
        target = self.state.cache_dir / "blobs" / f"{patch.version}.patch.zst"
        if target.exists():
            return target
        target.parent.mkdir(parents=True, exist_ok=True)
        log.debug("downloading blob %s", patch.blob_url)
        import httpx

        with httpx.stream("GET", patch.blob_url, timeout=60.0) as resp:
            resp.raise_for_status()
            with target.open("wb") as fh:
                for chunk in resp.iter_bytes(chunk_size=1 << 16):
                    fh.write(chunk)
        return target