"""Detached signature verification for signed release channels."""

from __future__ import annotations

import base64
from pathlib import Path


class SigningAdapter:
    def __init__(self, public_key_path: str | None):
        self.public_key_path = Path(public_key_path) if public_key_path else None

    def verify_detached(self, payload: dict, signature_b64: str) -> bool:
        if self.public_key_path is None:
            return False
        try:
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            from cryptography.exceptions import InvalidSignature
        except ImportError:
            raise RuntimeError("cryptography is required for signed channels")

        import json

        key = load_pem_public_key(self.public_key_path.read_bytes())
        message = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        try:
            key.verify(base64.b64decode(signature_b64), message)
            return True
        except InvalidSignature:
            return False