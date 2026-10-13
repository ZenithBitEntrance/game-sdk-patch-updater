"""Read Game SDK keys from the Windows registry (install metadata)."""

from __future__ import annotations

import sys

_KEY_ROOT = r"Software\\GameSDK\\Runtime"


class RegistryAdapter:
    def read_sdk_keys(self) -> dict[str, str]:
        if sys.platform != "win32":
            return {}
        import winreg

        out: dict[str, str] = {}
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _KEY_ROOT) as key:
                idx = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, idx)
                    except OSError:
                        break
                    out[name] = str(value)
                    idx += 1
        except FileNotFoundError:
            return {}
        return out