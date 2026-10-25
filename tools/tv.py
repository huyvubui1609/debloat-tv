#!/usr/bin/env python3
"""Send Android TV remote keys and pull an on-device screenshot over ADB.

Examples:
    python3 tools/tv.py --screenshot shots/current.png
    python3 tools/tv.py --screenshot shots/right.png DPAD_RIGHT

Set TV_HOST and TV_PORT to select the ADB endpoint. Defaults match relay.py.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot", required=True, type=Path,
                        help="local PNG path to save the TV screenshot")
    parser.add_argument("keys", nargs="*", help="Android key names/codes to send first")
    args = parser.parse_args()

    adb = os.environ.get("ADB", "adb")
    host = os.environ.get("TV_HOST", "127.0.0.1")
    port = os.environ.get("TV_PORT", "15555")
    target = f"{host}:{port}"

    def run(*command: str, capture: bool = False) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run([adb, "-s", target, *command], check=True,
                              stdout=subprocess.PIPE if capture else None)

    try:
        for key in args.keys:
            run("shell", "input", "keyevent", key)
            time.sleep(0.25)
        time.sleep(0.45)
        image = run("exec-out", "screencap", "-p", capture=True).stdout or b""
        if len(image) <= 8 or not image.startswith(b"\x89PNG\r\n\x1a\n"):
            print("TV returned an empty or invalid screenshot (protected video/input may do this).",
                  file=sys.stderr)
            return 1
        args.screenshot.parent.mkdir(parents=True, exist_ok=True)
        args.screenshot.write_bytes(image)
        print(f"Saved {len(image)} bytes from {target} to {args.screenshot}")
        return 0
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"TV ADB command failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
