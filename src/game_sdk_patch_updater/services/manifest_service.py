"""Fetch and cache release-channel manifests for the Game SDK runtime.

A manifest declares every SDK version a channel has published, the
patch blobs that bridge adjacent versions, and the channel's head
version. Manifests are fetched over HTTPS (or file:// for the local
channel) and validated against the channel's signature policy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from ..adapters.signing_adapter import SigningAdapter
from ..config_loader import load_channel
from ..models.manifest import ChannelManifest
from ..utils.logging import get_logger

log = get_logger(__name__)


class ManifestService:
    def __init__(self, channel_name: str, cache_dir: Path, signed: bool, public_key: str | None):
        self.channel_name = channel_name
        self.cache_dir = cache_dir
        self.signed = signed
        self.public_key = public_key

    @classmethod
    def from_context(cls, ctx: dict[str, Any]) -> "ManifestService":
        channel = load_channel(ctx["channel"])
        cache_dir = Path(ctx.get("root") or channel["cache_dir"]) / "manifests"
        return cls(
            channel_name=ctx["channel"],
            cache_dir=cache_dir,
            signed=channel["signed"],
            public_key=channel.get("public_key"),
        )

    def fetch(self) -> ChannelManifest:
        url = load_channel(self.channel_name)["manifest_url"]
        log.debug("fetching manifest %s", url)
        response = httpx.get(url, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
        raw = response.json()

        if self.signed:
            signing = SigningAdapter(self.public_key)
            if not signing.verify_detached(raw["payload"], raw["signature"]):
                raise ValueError(f"channel {self.channel_name!r} manifest signature invalid")

        manifest = ChannelManifest.model_validate(raw["payload"])
        self._write_cache(manifest)
        return manifest

    def _write_cache(self, manifest: ChannelManifest) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        target = self.cache_dir / f"{self.channel_name}.json"
        target.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")