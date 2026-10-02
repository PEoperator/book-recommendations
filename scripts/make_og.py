#!/usr/bin/env python3
"""Render the social share card (og.png, 1200x630) from scripts/og.html.

Usage:  python3 scripts/make_og.py [--chrome /path/to/chrome]

Serves the repo root on a local port (so the self-hosted Archivo font and
Untitled.jpg load exactly as on the site), screenshots scripts/og.html with
headless Chrome/Chromium at 1200x630, then re-encodes the PNG with Pillow
(256-colour palette, optimized) to keep the file small.
Requires: Google Chrome or Chromium, Pillow.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "og.png"
W, H = 1200, 630


def find_chrome(explicit: str | None) -> str:
    if explicit:
        return explicit
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit("Chrome/Chromium not found; pass --chrome /path/to/binary")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome")
    args = ap.parse_args()
    chrome = find_chrome(args.chrome)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):  # keep output clean
            pass

    handler = functools.partial(Quiet, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    try:
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.png"
            subprocess.run(
                [
                    chrome,
                    "--headless=new",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    "--no-first-run",
                    "--no-default-browser-check",
                    f"--user-data-dir={tmp}/profile",
                    f"--window-size={W},{H}",
                    "--virtual-time-budget=5000",
                    f"--screenshot={raw}",
                    f"http://127.0.0.1:{port}/scripts/og.html",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            img = Image.open(raw).convert("RGB")
    finally:
        server.shutdown()

    if img.size != (W, H):
        raise SystemExit(f"Unexpected screenshot size {img.size}, expected {(W, H)}")

    pal = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    pal.save(OUT, format="PNG", optimize=True)
    print(f"Wrote {OUT.relative_to(ROOT)}: {W}x{H}, {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
