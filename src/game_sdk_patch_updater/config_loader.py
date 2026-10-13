"""Load channel and runtime config from TOML."""

from __future__ import annotations

import tomllib
from functools import lru_cache
from pathlib import Path

_CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


@lru_cache(maxsize=1)
def _channels() -> dict:
    with (_CONFIG_DIR / "channels.toml").open("rb") as fh:
        return tomllib.load(fh)["channels"]


@lru_cache(maxsize=1)
def load_runtime() -> dict:
    with (_CONFIG_DIR / "runtime.toml").open("rb") as fh:
        return tomllib.load(fh)


def load_channel(name: str) -> dict:
    channels = _channels()
    if name not in channels:
        raise KeyError(f"unknown channel {name!r}; known: {sorted(channels)}")
    return channels[name]