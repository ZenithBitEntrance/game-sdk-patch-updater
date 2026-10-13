# Security Policy

## Scope

`game-sdk-patch-updater` downloads and applies patch blobs to a local
Game SDK runtime. The threat surface is:

- **Manifest tampering** — a malicious manifest redirecting the updater
  to an attacker-controlled blob host.
- **Patch blob tampering** — a blob whose content does not match the
  SHA-256 declared in the manifest.
- **Path traversal** — a patch whose target paths escape the SDK
  install root.
- **Privilege escalation** — patches that drop executables outside the
  install root or write to registry keys the updater was not asked to
  touch.

## Mitigations

- Every manifest is fetched over HTTPS and its `signature` field is
  verified against the channel's pinned public key when the channel
  declares `signed = true`.
- Every patch blob is SHA-256 verified after download and before apply.
- All target paths are resolved and checked against the install root
  before any file is written.
- The install root is locked with `portalocker` for the duration of
  the apply step; concurrent updaters fail fast rather than racing.

## Reporting a vulnerability

Do not open a public issue for a security bug. Email the maintainers
listed in the channel config, or open a private security advisory on
the GitHub repo. Include a reproducer, the channel name, and the
manifest that triggers the issue.

We aim to acknowledge within 72 hours.