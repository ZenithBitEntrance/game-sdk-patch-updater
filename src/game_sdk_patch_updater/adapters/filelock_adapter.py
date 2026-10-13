"""Cross-process lock around the SDK install root."""

from __future__ import annotations

from pathlib import Path

import portalocker


class FileLockAdapter:
    def __init__(self, lock_path: Path):
        self.lock_path = lock_path

    def __enter__(self) -> "FileLockAdapter":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.lock_path.open("w")
        portalocker.lock(self._fh, portalocker.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        portalocker.unlock(self._fh)
        self._fh.close()