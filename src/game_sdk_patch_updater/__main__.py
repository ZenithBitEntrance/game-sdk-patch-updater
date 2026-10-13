"""CLI entry point. Dispatches to thin handlers under handlers/."""

from __future__ import annotations

import argparse
import sys

from .handlers import apply as apply_handler
from .handlers import check as check_handler
from .handlers import doctor as doctor_handler
from .handlers import rollback as rollback_handler
from .utils.logging import configure_logging


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sdkpatch",
        description="Auto-updater and patch installer for Game SDK runtimes.",
    )
    parser.add_argument("--root", help="SDK install root (overrides config)")
    parser.add_argument("--channel", default="stable", help="Release channel name")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="Show whether a patch is available")
    sub.add_parser("apply", help="Download and apply the pending patch chain")
    sub.add_parser("rollback", help="Revert the last N applied patches")
    sub.add_parser("doctor", help="Inspect the local SDK runtime and channel state")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    configure_logging(args.verbose)

    ctx = {
        "root": args.root,
        "channel": args.channel,
        "verbose": args.verbose,
    }

    dispatch = {
        "check": check_handler.run,
        "apply": apply_handler.run,
        "rollback": rollback_handler.run,
        "doctor": doctor_handler.run,
    }
    return dispatch[args.command](ctx)


if __name__ == "__main__":
    sys.exit(main())