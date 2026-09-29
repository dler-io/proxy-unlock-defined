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


def generated_text(service, parts, patterns):
    return (f"# {service}\n# Generated from: {', '.join(parts)}\n"
            "# Edit the canonical parts and run python3 scripts/build.py\n" +
            "\n".join(patterns) + "\n")


def catalog_material(root=ROOT):
    data = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or set(data) != {"schema_version", "services"}:
        raise ValueError("unsupported catalog schema")
    if not isinstance(data["services"], list) or not data["services"]:
        raise ValueError("catalog must contain at least one service")
    entries, seen, paths, rules, resources, generated = {}, set(), set(), {}, {}, {}

    def add_resource(key, item, patterns):
        if not ID.fullmatch(key) or key.casefold() in seen:
            raise ValueError(f"case-insensitively duplicate ruleset: {key}")
        seen.add(key.casefold())
        resources[key] = {**item, "rules": patterns}

    def canonical(path):
        file = root / path
        if any(p.is_symlink() for p in (file, *file.parents)) or not file.is_file():
            raise ValueError(f"ruleset missing or symlinked: {path}")
        values = read_lines(file)
        if not values or values != sorted(set(values)):
            raise ValueError(f"{path}: rules must be nonempty, sorted and unique")
        return values

    for item in data["services"]:
        service, path, status = item["id"], item["path"], item["status"]
        if not ID.fullmatch(service) or service.casefold() in seen:
            raise ValueError(f"invalid or case-insensitively duplicate service: {service}")
        directory = {"imported": "services", "review": "review", "legacy": "legacy"}.get(status)
        if directory is None or path != f"{directory}/{service}.list" or path in paths:
            raise ValueError(f"invalid catalog path or status: {service}")
        if not item.get("name") or set(item) - {"id", "name", "path", "status", "note", "parts", "subsets"}:
            raise ValueError(f"invalid catalog fields: {service}")
        paths.add(path)
        if "parts" not in item:
            if "subsets" in item:
                raise ValueError(f"{service}: subsets require canonical parts")
            patterns = canonical(path)
        else:
            if not isinstance(item["parts"], list) or not item["parts"]:
                raise ValueError(f"{service}: parts must be a nonempty list")
            part_rules, part_paths = {}, {}
            for part in item["parts"]:
                key, part_path = part["id"], part["path"]
                if (not ID.fullmatch(key) or part_path != f"parts/{service}/{key}.list"
                        or part_path in paths or not part.get("name")
                        or set(part) != {"id", "name", "path"}):
                    raise ValueError(f"{service}: invalid part")
                values = canonical(part_path)
                part_rules[key], part_paths[key] = values, part_path
                paths.add(part_path)
                add_resource(f"{service}_{key}", {"path": part_path, "status": status,
                             "name": part["name"], "parent": service}, values)
            # Keep duplicates here so ownership validation rejects overlapping parts.
            patterns = sorted(p for values in part_rules.values() for p in values)
            generated[path] = generated_text(service, list(part_paths.values()), patterns)
            for subset in item.get("subsets", []):
                key, subset_path, selected = subset["id"], subset["path"], subset["parts"]
                if (not ID.fullmatch(key) or subset_path != f"subsets/{service}/{key}.list"
                        or subset_path in paths or not subset.get("name")
                        or set(subset) != {"id", "name", "path", "parts"}
                        or not isinstance(selected, list) or not selected
                        or len(set(selected)) != len(selected)
                        or any(p not in part_rules for p in selected)):
                    raise ValueError(f"{service}: invalid subset")
                values = sorted(p for part in selected for p in part_rules[part])
                generated[subset_path] = generated_text(f"{service} / {key}",
                                                       [part_paths[p] for p in selected], values)
                paths.add(subset_path)
                add_resource(f"{service}_{key}", {"path": subset_path, "status": status,
                             "name": subset["name"], "parent": service}, values)
        entries[service], rules[service] = item, patterns
        add_resource(service, item, patterns)
    actual = {str(p.relative_to(root)) for directory in ("services", "review", "legacy", "parts", "subsets")
              for p in (root / directory).rglob("*.list")}
    if actual - paths or paths - actual - generated.keys():
        raise ValueError(f"uncataloged or missing files: {sorted(actual ^ paths)}")
    for path in generated:
        file = root / path
        if any(p.is_symlink() for p in (file, *file.parents)):
            raise ValueError(f"generated ruleset cannot be symlinked: {path}")
    return entries, rules, resources, generated


def load_catalog(root=ROOT, verify_generated=True):
    entries, rules, _, generated = catalog_material(root)
    if verify_generated:
        for path, expected in generated.items():
            file = root / path
            if not file.is_file() or file.read_text(encoding="utf-8") != expected:
                raise ValueError(f"{path}: stale generated list; run python3 scripts/build.py")
    return entries, rules


def check(root=ROOT, verify_generated=True):
    entries, rules = load_catalog(root, verify_generated)
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
    print(f"PASS: {len(entries)} services, {sum(map(len, rules.values()))} domain patterns, "
          f"{len(approvals)} documented suffix overlaps, no duplicate ownership")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
