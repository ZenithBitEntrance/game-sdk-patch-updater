"""Apply a downloaded patch blob to the SDK install root.

The blob is a zstd-compressed tar of new/modified files plus a
`deletions.txt` listing paths to remove. Every target path is
resolved against the install root before any write.
"""

from __future__ import annotations

import tarfile
from pathlib import Path

import zstandard as zstd

from ..models.patch import PatchDescriptor
from ..utils.logging import get_logger

log = get_logger(__name__)


class PatchApplyAdapter:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def apply(self, blob: Path, patch: PatchDescriptor) -> None:
        with blob.open("rb") as fh:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(fh) as reader:
                with tarfile.open(fileobj=reader, mode="r|") as tar:
                    self._extract(tar)

    def revert(self, patch: PatchDescriptor) -> None:
        log.info("revert path for %s — restore from rollback cache", patch.version)
        backup = self.root / ".rollback" / patch.version
        if not backup.exists():
            raise FileNotFoundError(f"no rollback snapshot for {patch.version}")
        for stale in backup.rglob("*"):
            if stale.is_file():
                rel = stale.relative_to(backup)
                (self.root / rel).write_bytes(stale.read_bytes())

    def _extract(self, tar: tarfile.TarFile) -> None:
        for member in tar:
            target = (self.root / member.name).resolve()
            if not str(target).startswith(str(self.root)):
                raise ValueError(f"patch escapes install root: {member.name}")
            if member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                extracted = tar.extractfile(member)
                if extracted is None:
                    continue
                target.write_bytes(extracted.read())