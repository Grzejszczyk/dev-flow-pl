"""Sprawdza kontrakt przypadków ewaluacji; nie uruchamia ani nie ocenia agenta."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PureWindowsPath


def strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def evaluation_errors(root: Path) -> list[str]:
    root = root.resolve()
    catalog = root / "evals" / "cases"
    fixtures = root / "evals" / "fixtures"
    errors: list[str] = []
    paths = sorted(catalog.glob("*.json"))
    if not paths:
        return ["evals/cases: brak przypadków"]
    seen: set[str] = set()
    covered: set[str] = set()
    for path in paths:
        label = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(catalog.resolve()):
            errors.append(f"{label}: plik poza katalogiem przypadków")
            continue
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            errors.append(f"{label}: niepoprawny JSON UTF-8")
            continue
        if not isinstance(pack, dict):
            errors.append(f"{label}: oczekiwany obiekt")
            continue
        if set(pack) != {"skill", "triggers", "cases"}:
            errors.append(f"{label}: oczekiwane pola skill, triggers, cases")
        skill = pack.get("skill")
        if not isinstance(skill, str) or not re.fullmatch(r"aew-[a-z0-9]+(?:-[a-z0-9]+)*", skill):
            errors.append(f"{label}: niepoprawna nazwa skilla")
        elif path.stem != skill or not (root / "skills" / skill / "SKILL.md").is_file():
            errors.append(f"{label}: nieznany skill lub niezgodna nazwa pliku")
        else:
            covered.add(skill)
        triggers = pack.get("triggers")
        if not isinstance(triggers, dict) or set(triggers) != {"positive", "negative"}:
            errors.append(f"{label}: wymagane triggers.positive i triggers.negative")
        else:
            for kind in ("positive", "negative"):
                if not strings(triggers[kind]) or len(triggers[kind]) < 2:
                    errors.append(f"{label}: {kind} wymaga co najmniej dwóch poleceń")
        cases = pack.get("cases")
        if not isinstance(cases, list) or not cases:
            errors.append(f"{label}: brak przypadków zachowania")
            continue
        for case in cases:
            if not isinstance(case, dict):
                errors.append(f"{label}: przypadek musi być obiektem")
                continue
            required = {"id", "prompt", "fixture", "setup", "expected", "forbidden", "evidence"}
            if set(case) != required:
                errors.append(f"{label}: niezgodne pola przypadku")
            case_id = case.get("id")
            if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
                errors.append(f"{label}: niepoprawny identyfikator")
            elif case_id in seen:
                errors.append(f"{label}: powtórzony identyfikator {case_id}")
            else:
                seen.add(case_id)
            for field in ("prompt", "setup"):
                if not isinstance(case.get(field), str) or not case[field].strip():
                    errors.append(f"{label}/{case_id}: brak {field}")
            for field in ("expected", "forbidden", "evidence"):
                if not strings(case.get(field)):
                    errors.append(f"{label}/{case_id}: brak {field}")
            fixture = case.get("fixture")
            if not isinstance(fixture, str) or not fixture.strip():
                errors.append(f"{label}/{case_id}: brak fixture")
                continue
            relative = Path(fixture)
            destination = (fixtures / relative).resolve()
            if (
                relative.is_absolute() or PureWindowsPath(fixture).drive
                or "\\" in fixture or ".." in relative.parts
                or not destination.is_relative_to(fixtures.resolve())
                or not destination.is_dir()
            ):
                errors.append(f"{label}/{case_id}: niebezpieczna lub brakująca fixture")
                continue
            # Nie kopiuj dowiązań prowadzących poza dozwolone dane.
            if any(not item.resolve().is_relative_to(fixtures.resolve())
                   for item in destination.rglob("*")):
                errors.append(f"{label}/{case_id}: fixture zawiera odwołanie poza katalog")
    skills = root / "skills"
    for folder in sorted(skills.iterdir()) if skills.is_dir() else []:
        if folder.is_dir() and (folder / "SKILL.md").is_file() and folder.name not in covered:
            errors.append(f"{folder.name}: brak pakietu ewaluacji")
    return errors


def main() -> int:
    errors = evaluation_errors(Path(__file__).resolve().parents[1])
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("Przypadki ewaluacji poprawne strukturalnie; nie uruchomiono agenta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
