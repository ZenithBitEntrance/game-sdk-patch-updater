"""`sdkpatch apply` — download and install the pending patch chain."""

from __future__ import annotations

from typing import Any

from ..services.install_service import InstallService
from ..services.manifest_service import ManifestService
from ..services.patch_chain_service import PatchChainService
from ..services.state_service import StateService
from ..utils.logging import get_logger

log = get_logger(__name__)


def run(ctx: dict[str, Any]) -> int:
    state = StateService.from_context(ctx)
    channel = ManifestService.from_context(ctx)
    chain = PatchChainService(channel=channel, state=state)
    installer = InstallService(state=state, chain=chain)

    pending = chain.pending_patches()
    if not pending:
        log.info("nothing to apply — SDK is up to date.")
        return 0

    for patch in pending:
        log.info("applying %s (%s)", patch.version, patch.summary)
        installer.apply_patch(patch)

    log.info("done. SDK is now at %s", state.local_sdk_version())
    return 0