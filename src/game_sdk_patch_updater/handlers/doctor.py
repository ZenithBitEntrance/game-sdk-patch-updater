"""`sdkpatch doctor` — inspect the local SDK runtime and channel state."""

from __future__ import annotations

from typing import Any

from ..adapters.registry_adapter import RegistryAdapter
from ..services.state_service import StateService
from ..utils.logging import get_logger

log = get_logger(__name__)


def run(ctx: dict[str, Any]) -> int:
    state = StateService.from_context(ctx)
    registry = RegistryAdapter()

    log.info("install root:     %s", state.root)
    log.info("channel:          %s", state.channel)
    log.info("SDK version:      %s", state.local_sdk_version())
    log.info("applied patches:  %d", len(state.applied_patches()))
    log.info("cache dir:        %s", state.cache_dir)

    if ctx.get("verbose"):
        for key, value in registry.read_sdk_keys().items():
            log.info("registry %-24s %s", key, value)

    return 0