#!/usr/bin/env python3
"""Asset gate for distributable builds.

Only approved, documented assets are eligible for `build_assets/`. Reference
material is intentionally excluded even if it exists locally.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "ASSET_MANIFEST.json"
REQUIRED = {"id", "path", "author", "source", "license", "status"}
VALID_STATUS = {"approved", "needs_permission", "reference_only"}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assets = manifest.get("assets", [])
    approved = []
    problems = []
    seen = set()
    for asset in assets:
        missing = REQUIRED - set(asset)
        identifier = asset.get("id", "<missing-id>")
        if missing:
            problems.append(f"{identifier}: missing {', '.join(sorted(missing))}")
            continue
        if identifier in seen:
            problems.append(f"{identifier}: duplicate ID")
        seen.add(identifier)
        if asset["status"] not in VALID_STATUS:
            problems.append(f"{identifier}: invalid status {asset['status']!r}")
        if asset["status"] == "approved":
            asset_path = ROOT / asset["path"]
            if not asset_path.is_file():
                problems.append(f"{identifier}: approved file does not exist: {asset['path']}")
            else:
                approved.append(asset)
    print("Asset audit")
    print(f"  total registered: {len(assets)}")
    print(f"  eligible for build: {len(approved)}")
    print(f"  reference/permission pending: {len(assets) - len(approved)}")
    for problem in problems:
        print(f"  ERROR: {problem}")
    if problems:
        return 1
    print("PASS: asset registry is valid. Only approved assets may enter a distributable build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
