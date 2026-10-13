"""Logging configuration for the CLI and services."""

from __future__ import annotations

import logging

_LOGGER = logging.getLogger("game_sdk_patch_updater")
_CONFIGURED = False


def configure_logging(verbose: bool = False) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%H:%M:%S"))
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return _LOGGER.getChild(name.rsplit(".", 1)[-1])