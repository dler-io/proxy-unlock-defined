#!/usr/bin/env python3
"""Validate the catalog and domain ownership without network access."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
LABEL = re.compile(r"[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?\Z")
OVERLAP_KEYS = ("parent_service", "parent_rule", "child_service", "child_rule")


def read_lines(path):
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def valid_rule(rule):
    host = rule.removeprefix("+.")
    return (bool(host) and len(host) <= 253 and
            all(LABEL.fullmatch(label) for label in host.split(".")))


def ownership_keys(rule):
    if rule.startswith("+."):
        return (rule[2:], "." + rule[2:])
    return (rule,)


def find_overlaps(rules):
    found = set()
    for parent_service, patterns in rules.items():
        for parent in patterns:
            if not parent.startswith("+."):
                continue
            for child_service, children in rules.items():
                if parent_service == child_service:
                    continue
                for child in children:
                    if child.removeprefix("+.").endswith("." + parent[2:]):
                        found.add((parent_service, parent, child_service, child))
    return found


def lint_rules(rules, approvals, removed):
    errors, owners = [], {}
    for service, patterns in rules.items():
        if not patterns:
            errors.append(f"{service}: empty ruleset")
        if patterns != sorted(set(patterns)):
            errors.append(f"{service}: rules must be sorted and unique")
        for pattern in patterns:
            if not valid_rule(pattern):
                errors.append(f"{service}: invalid domain pattern {pattern!r}")
                continue
            if pattern.removeprefix("+.") in removed:
                errors.append(f"{service}: removed domain reintroduced: {pattern}")
            for key in ownership_keys(pattern):
                if key in owners:
                    errors.append(f"duplicate match {key}: {owners[key]} and {service}")
                else:
                    owners[key] = service
    allowed = set()
    for item in approvals:
        if set(item) != set(OVERLAP_KEYS) | {"reason"} or not item.get("reason", "").strip():
            errors.append("overlap approval requires four match fields and a reason")
            continue
        key = tuple(item[k] for k in OVERLAP_KEYS)
        if key in allowed:
            errors.append(f"duplicate overlap approval: {key}")
        allowed.add(key)
    observed = find_overlaps(rules)
    errors.extend(f"unapproved suffix overlap: {key}" for key in sorted(observed - allowed))
    errors.extend(f"stale overlap approval: {key}" for key in sorted(allowed - observed))
    return errors


def load_catalog(root=ROOT):
    data = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or set(data) != {"schema_version", "services"}:
        raise ValueError("unsupported catalog schema")
    if not isinstance(data["services"], list) or not data["services"]:
        raise ValueError("catalog must contain at least one service")
    entries, seen, paths, rules = {}, set(), set(), {}
    for item in data["services"]:
        service, path, status = item["id"], item["path"], item["status"]
        if not ID.fullmatch(service) or service.casefold() in seen:
            raise ValueError(f"invalid or case-insensitively duplicate service: {service}")
        directory = {"imported": "services", "review": "review", "legacy": "legacy"}.get(status)
        if directory is None or path != f"{directory}/{service}.list" or path in paths:
            raise ValueError(f"invalid catalog path or status: {service}")
        file = root / path
        if file.is_symlink() or not file.is_file():
            raise ValueError(f"ruleset missing or symlinked: {path}")
        if not item.get("name") or set(item) - {"id", "name", "path", "status", "note"}:
            raise ValueError(f"invalid catalog fields: {service}")
        entries[service], rules[service] = item, read_lines(file)
        seen.add(service.casefold())
        paths.add(path)
    actual = {str(p.relative_to(root)) for directory in ("services", "review", "legacy")
              for p in (root / directory).rglob("*.list")}
    if actual != paths:
        raise ValueError(f"uncataloged or missing files: {sorted(actual ^ paths)}")
    return entries, rules


def check(root=ROOT):
    entries, rules = load_catalog(root)
    approvals = json.loads((root / "policy/overlaps.json").read_text(encoding="utf-8"))
    removed = read_lines(root / "policy/removed-domains.txt")
    if removed != sorted(set(removed)) or any(not valid_rule(x) or x.startswith("+.") for x in removed):
        raise ValueError("removed domains must be sorted, unique bare domain names")
    errors = lint_rules(rules, approvals, set(removed))
    if errors:
        raise ValueError("\n".join(errors))
    return entries, rules, approvals


def main():
    try:
        entries, rules, approvals = check()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(entries)} lists, {sum(map(len, rules.values()))} domain patterns, "
          f"{len(approvals)} documented suffix overlaps, no duplicate ownership")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
