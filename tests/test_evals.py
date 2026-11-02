"""Testy kontraktu danych pilotażu, bez wywołań modeli."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_evals import evaluation_errors


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "skills/aew-example").mkdir(parents=True)
        (self.root / "skills/aew-example/SKILL.md").write_text("example\n", encoding="utf-8")
        (self.root / "evals/fixtures/project").mkdir(parents=True)
        self.path = self.root / "evals/cases/aew-example.json"
        self.path.parent.mkdir(parents=True)
        self.case = {
            "id": "example", "prompt": "Przeanalizuj.", "fixture": "project",
            "setup": "Czysty syntetyczny projekt.",
            "expected": ["Analiza"], "forbidden": ["Edycja"],
            "evidence": ["Diff i ślad"],
        }
        self.pack = {
            "skill": "aew-example",
            "triggers": {"positive": ["Analizuj", "Oceń zakres"],
                         "negative": ["Napisz wiersz", "Wyjaśnij pojęcie"]},
            "cases": [self.case],
        }

    def check(self):
        self.path.write_text(json.dumps(self.pack, ensure_ascii=False) + "\n", encoding="utf-8")
        return evaluation_errors(self.root)

    def test_valid_catalog(self):
        self.assertEqual([], self.check())

    def test_missing_catalog(self):
        self.assertTrue(evaluation_errors(self.root))

    def test_broken_json_is_reported(self):
        self.path.write_text("{broken\n", encoding="utf-8")
        self.assertTrue(any("JSON" in error for error in evaluation_errors(self.root)))

    def test_unknown_skill_and_missing_coverage(self):
        self.pack["skill"] = "aew-missing"
        errors = self.check()
        self.assertTrue(any("nieznany skill" in error for error in errors))
        self.assertTrue(any("brak pakietu" in error for error in errors))

    def test_duplicate_id_across_cases(self):
        self.pack["cases"].append(dict(self.case))
        self.assertTrue(any("powtórzony" in error for error in self.check()))

    def test_required_evidence_and_triggers(self):
        for mutation in ("expected", "forbidden", "evidence"):
            with self.subTest(field=mutation):
                original = self.case[mutation]
                self.case[mutation] = []
                self.assertTrue(any(mutation in error for error in self.check()))
                self.case[mutation] = original
        self.pack["triggers"]["negative"] = ["jedno"]
        self.assertTrue(any("negative" in error for error in self.check()))

    def test_invalid_shapes_do_not_crash(self):
        for value in ([], None, 12):
            with self.subTest(value=value):
                self.path.write_text(json.dumps(value), encoding="utf-8")
                self.assertTrue(evaluation_errors(self.root))
        self.pack["cases"] = [None]
        self.assertTrue(self.check())

    def test_fixture_escape_absolute_missing_and_windows_paths(self):
        for value in ("../cases", "/tmp", "C:/tmp", "C:tmp", "..\\cases", "missing", ""):
            with self.subTest(fixture=value):
                self.case["fixture"] = value
                self.assertTrue(any("fixture" in error for error in self.check()))

    def test_fixture_symlink_escape(self):
        link = self.root / "evals/fixtures/project/outside"
        try:
            link.symlink_to(self.root / "skills", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Tworzenie dowiązań niedostępne; przypadek wykonywany także w CI Linux.")
        self.assertTrue(any("poza katalog" in error for error in self.check()))


if __name__ == "__main__":
    unittest.main()
