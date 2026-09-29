#!/usr/bin/env python3
"""Render a proxy-unlock fragment with explicit service/outbound bindings."""
import argparse
import json
import re
from urllib.parse import quote

from check import ROOT, check


def render(bindings, ref="main", include_review=False):
    entries, _, _ = check(ROOT)
    selected = {}
    for binding in bindings:
        service, sep, region = binding.partition("=")
        if not sep or service not in entries:
            raise ValueError(f"unknown service or invalid SERVICE=OUTBOUND: {binding}")
        if service in selected:
            raise ValueError(f"duplicate service: {service}")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", region):
            raise ValueError(f"invalid outbound name: {region}")
        if entries[service]["status"] != "imported" and not include_review:
            raise ValueError(f"{service} needs explicit --include-review")
        selected[service] = region
    if not selected or not ref or any(ord(c) < 32 for c in ref):
        raise ValueError("at least one service and a nonempty ref are required")
    lines = ["# Merge into the existing proxy-unlock section; retain its rules/outbounds",
             "proxy-unlock:", "  rule-interval: 600", "  defined:"]
    for service, region in sorted(selected.items()):
        url = ("https://raw.githubusercontent.com/dler-io/proxy-unlock-defined/" +
               quote(ref, safe="") + "/" + entries[service]["path"])
        lines.extend([f"    {service}:", f"      url: {json.dumps(url)}",
                      f"      region: {json.dumps(region)}"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service", action="append", required=True, metavar="SERVICE=OUTBOUND")
    parser.add_argument("--ref", default="main", help="branch, tag or commit SHA")
    parser.add_argument("--include-review", action="store_true", help="explicitly include review/legacy entries")
    args = parser.parse_args()
    try:
        print(render(args.service, args.ref, args.include_review), end="")
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
