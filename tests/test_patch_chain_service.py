"""Chain resolution tests against a fixture manifest."""

from __future__ import annotations

from pathlib import Path

import pytest

from game_sdk_patch_updater.models.manifest import ChannelManifest
from game_sdk_patch_updater.models.patch import PatchDescriptor
from game_sdk_patch_updater.services.patch_chain_service import PatchChainService


class _FakeManifestService:
    def __init__(self, manifest: ChannelManifest):
        self.channel_name = "test"
        self._manifest = manifest

    def fetch(self) -> ChannelManifest:
        return self._manifest


class _FakeStateService:
    def __init__(self, version: str):
        self._version = version

    def local_sdk_version(self) -> str:
        return self._version


def _patch(frm: str, to: str) -> PatchDescriptor:
    return PatchDescriptor(
        version=f"p-{to}",
        from_version=frm,
        to_version=to,
        summary=f"{frm} -> {to}",
        blob_url=f"file://./{to}.patch.zst",
        sha256="0" * 64,
    )


def test_resolves_linear_chain():
    manifest = ChannelManifest(
        channel="test",
        head_version="1.3.0",
        published_at="2026-01-01T00:00:00Z",
        patches=[_patch("1.1.0", "1.2.0"), _patch("1.2.0", "1.3.0")],
    )
    chain = PatchChainService(
        channel=_FakeManifestService(manifest),
        state=_FakeStateService("1.1.0"),
    )
    pending = chain.pending_patches()
    assert [p.to_version for p in pending] == ["1.2.0", "1.3.0"]


def test_missing_edge_raises():
    manifest = ChannelManifest(
        channel="test",
        head_version="2.0.0",
        published_at="2026-01-01T00:00:00Z",
        patches=[_patch("1.0.0", "1.1.0")],
    )
    chain = PatchChainService(
        channel=_FakeManifestService(manifest),
        state=_FakeStateService("1.0.0"),
    )
    with pytest.raises(RuntimeError, match="no patch edge"):
        chain.pending_patches()