"""Resolve the ordered patch chain between the local SDK and channel head."""

from __future__ import annotations

from semver import Version

from ..models.patch import PatchDescriptor
from .manifest_service import ManifestService
from .state_service import StateService
from ..utils.logging import get_logger

log = get_logger(__name__)


class PatchChainService:
    def __init__(self, channel: ManifestService, state: StateService):
        self.channel = channel
        self.state = state

    def latest_channel_version(self) -> str:
        manifest = self.channel.fetch()
        return manifest.head_version

    def pending_patches(self) -> list[PatchDescriptor]:
        manifest = self.channel.fetch()
        local = Version.parse(self.state.local_sdk_version())

        chain: list[PatchDescriptor] = []
        cursor = local
        by_from = {p.from_version: p for p in manifest.patches}

        while str(cursor) != manifest.head_version:
            step = by_from.get(str(cursor))
            if step is None:
                raise RuntimeError(
                    f"no patch edge from {cursor} to {manifest.head_version} "
                    f"on channel {self.channel.channel_name!r}"
                )
            chain.append(step)
            cursor = Version.parse(step.to_version)

        log.debug("resolved %d patches %s -> %s", len(chain), local, manifest.head_version)
        return chain