"""`sdkpatch check` — report whether the local SDK is behind the channel."""

from __future__ import annotations

from typing import Any

from ..services.manifest_service import ManifestService
from ..services.patch_chain_service import PatchChainService
from ..services.state_service import StateService
from ..utils.logging import get_logger

log = get_logger(__name__)


def run(ctx: dict[str, Any]) -> int:
    state = StateService.from_context(ctx)
    channel = ManifestService.from_context(ctx)
    chain = PatchChainService(channel=channel, state=state)

    local = state.local_sdk_version()
    remote = chain.latest_channel_version()
    pending = chain.pending_patches()

    log.info("local SDK version:  %s", local)
    log.info("channel head:       %s", remote)
    if not pending:
        log.info("SDK is up to date.")
        return 0

    log.info("pending patches:    %d", len(pending))
    for patch in pending:
        log.info("  %s  %s", patch.version, patch.summary)
    return 0