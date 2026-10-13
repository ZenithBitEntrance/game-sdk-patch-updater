# Contributing to game-sdk-patch-updater

`game-sdk-patch-updater` keeps a local Game SDK runtime in sync with a
remote release channel. It fetches channel manifests, resolves the
required patch chain, downloads and verifies patch blobs, then applies
them to the SDK install root under a cross-process lock.

## Repo layout

- `src/game_sdk_patch_updater/__main__.py` — CLI entry point
- `handlers/` — thin command handlers, one per CLI verb, no business logic
- `services/` — business services (manifest, patch chain, install)
- `models/` — pydantic data models for manifests, patches, state
- `adapters/` — platform adapters (Windows registry, file locking, signing)
- `utils/` — hashing, archive, logging helpers
- `config/` — channel + runtime defaults

Handlers stay thin. If you find yourself parsing a manifest inside a
handler, it belongs in `services/`. If you find yourself calling
`winreg` directly, it belongs in `adapters/`.

## Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
ruff check src tests
mypy src
```

## Patch channels

Channels are declared in `config/channels.toml`. `stable` and `beta`
are maintained by the core team. Custom channels are welcome for
modding distributions — open a PR adding the channel and a short note
on who maintains it.

## Pull requests

- Keep handlers under ~40 lines.
- New services need at least one test in `tests/`.
- Patch-apply code paths MUST be tested against a fixture SDK tree,
  never against a live install.
- Run `ruff` and `mypy` before opening the PR. CI runs both.

## Reporting issues

Include the output of `sdkpatch doctor --verbose`, your channel name,
and the SDK version you were on before the failure.