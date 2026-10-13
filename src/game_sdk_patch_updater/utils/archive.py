"""Helpers for reading patch archives and listing target paths."""

from __future__ import annotations

from pathlib import Path

import zstandard as zstd


def decompress_zst(blob: Path, out: Path) -> Path:
    dctx = zstd.ZstdDecompressor()
    with blob.open("rb") as src, out.open("wb") as dst:
        dctx.copy_stream(src, dst)
    return out