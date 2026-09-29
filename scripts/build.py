#!/usr/bin/env python3
"""Build complete services and composed subsets from canonical parts."""
import sys

from check import ROOT, catalog_material, check


def build(root=ROOT):
    check(root, verify_generated=False)
    _, _, _, generated = catalog_material(root)
    for path, text in generated.items():
        file = root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
    return len(generated)


if __name__ == "__main__":
    try:
        print(f"Built {build()} generated lists")
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
