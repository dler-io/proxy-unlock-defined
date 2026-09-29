import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check import lint_rules, valid_rule
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

    def test_render_requires_explicit_valid_bindings(self):
        output = render(["Netflix=SG", "AI=AI"], ref="a" * 40)
        self.assertIn("/" + "a" * 40 + "/services/Netflix.list", output)
        self.assertIn('region: "SG"', output)
        for bindings in [["Missing=SG"], ["Netflix=SG", "Netflix=JP"], ["Netflix="], ["Shared=CA"]]:
            with self.assertRaises(ValueError):
                render(bindings)
        self.assertIn("review/Shared.list", render(["Shared=CA"], include_review=True))


if __name__ == "__main__":
    unittest.main()
