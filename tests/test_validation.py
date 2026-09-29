import sys
import json
import shutil
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check import ROOT, check, lint_rules, read_lines, valid_rule
from build import build
from render import render


class ValidationTests(unittest.TestCase):
    def test_domain_scope_is_preserved(self):
        self.assertEqual(lint_rules({"Service": ["+.example.com"]}, [], set()), [])
        self.assertTrue(valid_rule("api.example.com"))
        self.assertTrue(valid_rule("+.bbc"))
        for value in ["+", "*", "*.example.com", "https://example.com", "example..com", "EXAMPLE.com", "example.com."]:
            self.assertFalse(valid_rule(value), value)

    def test_root_alias_is_a_conflict(self):
        errors = lint_rules({"A": ["+.example.com"], "B": ["example.com"]}, [], set())
        self.assertTrue(any("duplicate match example.com" in x for x in errors))

    def test_cross_service_identical_suffix_is_a_conflict(self):
        errors = lint_rules({"A": ["+.example.com"], "B": ["+.example.com"]}, [], set())
        self.assertEqual(sum("duplicate match" in x for x in errors), 2)

    def test_nested_exception_requires_documented_approval(self):
        rules = {"Google": ["+.example.com"], "AI": ["api.example.com"]}
        self.assertTrue(lint_rules(rules, [], set()))
        approval = {"parent_service": "Google", "parent_rule": "+.example.com",
                    "child_service": "AI", "child_rule": "api.example.com", "reason": "specific service"}
        self.assertEqual(lint_rules(rules, [approval], set()), [])
        self.assertTrue(lint_rules({"Google": rules["Google"]}, [approval], set()))

    def test_removed_domain_cannot_be_reintroduced(self):
        for pattern in ["old.example.com", "+.old.example.com"]:
            self.assertTrue(lint_rules({"A": [pattern]}, [], {"old.example.com"}))
        # This policy removes entries; it is not a runtime domain denylist
        self.assertEqual(lint_rules({"A": ["+.example.com"]}, [], {"old.example.com"}), [])

    def test_ip_literals_are_not_domain_rules(self):
        for pattern in ["192.0.2.1", "+.192.0.2.1", "2001:db8::1", "192.0.2.0/24"]:
            self.assertFalse(valid_rule(pattern), pattern)
            self.assertTrue(lint_rules({"Service": [pattern]}, [], set()), pattern)
        self.assertTrue(valid_rule("192.0.2.1.example.com"))

    def test_render_requires_explicit_valid_bindings(self):
        output = render(["Netflix=SG", "AI=AI"], ref="a" * 40)
        self.assertIn("/" + "a" * 40 + "/services/Netflix.list", output)
        self.assertIn('region: "SG"', output)
        for bindings in [["Missing=SG"], ["Netflix=SG", "Netflix=JP"], ["Netflix="], ["Shared=CA"]]:
            with self.assertRaises(ValueError):
                render(bindings)
        self.assertIn("review/Shared.list", render(["Shared=CA"], include_review=True))

    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve() / "rules"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return root

    def test_part_edit_updates_full_service_from_one_source(self):
        root = self.fixture()
        part = root / "parts/MyTVSuper/Core.list"
        values = read_lines(part) + ["+.new.example.invalid"]
        part.write_text("\n".join(sorted(values)) + "\n")
        with self.assertRaisesRegex(ValueError, "stale generated"):
            check(root)
        build(root)
        check(root)
        self.assertIn("+.new.example.invalid", read_lines(root / "services/MyTVSuper.list"))
        self.assertNotIn("+.new.example.invalid", read_lines(root / "parts/MyTVSuper/Analytics.list"))

    def test_duplicate_between_parts_is_rejected(self):
        root = self.fixture()
        part = root / "parts/MyTVSuper/Analytics.list"
        part.write_text("\n".join(sorted(read_lines(part) + ["+.tvb.com"])) + "\n")
        with self.assertRaisesRegex(ValueError, "duplicate match"):
            build(root)

    def test_nested_overlap_between_parts_is_rejected(self):
        for pattern in ["stream.tvb.com", "+.stream.tvb.com"]:
            with self.subTest(pattern=pattern):
                root = self.fixture()
                part = root / "parts/MyTVSuper/Analytics.list"
                part.write_text("\n".join(sorted(read_lines(part) + [pattern])) + "\n")
                with self.assertRaisesRegex(ValueError, "suffix overlap between parts"):
                    build(root)
                with self.assertRaisesRegex(ValueError, "suffix overlap between parts"):
                    check(root)

    def test_composed_subset_and_full_service_update_together(self):
        root = self.fixture()
        part = root / "parts/Unclassified/JapaneseSites.list"
        values = sorted(read_lines(part) + ["+.new.example.invalid"])
        part.write_text("\n".join(values) + "\n")
        build(root)
        check(root)
        for path in ["subsets/Unclassified/Japanese.list", "review/Unclassified.list"]:
            self.assertIn("+.new.example.invalid", read_lines(root / path))

    def test_subset_rejects_unknown_parts(self):
        root = self.fixture()
        path = root / "catalog.json"
        catalog = json.loads(path.read_text())
        service = next(s for s in catalog["services"] if s["id"] == "Unclassified")
        service["subsets"][0]["parts"] = ["Missing"]
        path.write_text(json.dumps(catalog))
        with self.assertRaisesRegex(ValueError, "invalid subset"):
            build(root)

    def test_render_disjoint_parts_and_reject_duplicate_selection(self):
        output = render(["CanalPlus_MyCanal=DE", "CanalPlus_Core=FR"])
        self.assertIn("parts/CanalPlus/MyCanal.list", output)
        self.assertIn('region: "FR"', output)
        with self.assertRaisesRegex(ValueError, "overlapping selections"):
            render(["CanalPlus=FR", "CanalPlus_Core=FR"])
        with self.assertRaisesRegex(ValueError, "overlapping selections"):
            render(["Unclassified_Japanese=JP", "Unclassified_JapaneseSites=JP"], include_review=True)

    def test_review_status_applies_to_parts_and_composed_subsets(self):
        for ruleset in ["Shared_ThePlatform", "Unclassified_Japanese"]:
            with self.assertRaisesRegex(ValueError, "include-review"):
                render([ruleset + "=US"])
        self.assertIn("subsets/Unclassified/Japanese.list",
                      render(["Unclassified_Japanese=JP"], include_review=True))


if __name__ == "__main__":
    unittest.main()
