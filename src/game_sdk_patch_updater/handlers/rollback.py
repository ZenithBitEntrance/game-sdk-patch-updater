"""`sdkpatch rollback` — revert the last N applied patches."""

from __future__ import annotations

from typing import Any

from ..services.install_service import InstallService
from ..services.state_service import StateService
from ..utils.logging import get_logger

log = get_logger(__name__)


def run(ctx: dict[str, Any]) -> int:
    state = StateService.from_context(ctx)
    installer = InstallService(state=state, chain=None)

    applied = state.applied_patches()
    if not applied:
        log.info("no applied patches to roll back.")
        return 1

    target = applied[-1]
    log.info("rolling back %s", target.version)
    installer.rollback_patch(target)
    log.info("SDK is now at %s", state.local_sdk_version())
    return 0