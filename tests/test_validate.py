"""Regression tests for broken documents, portable paths and skill contracts."""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate import markdown_errors, plugin_errors, skill_errors, validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def make_skill(self):
        folder = self.root / "skills" / "aew-example"
        self.write(
            "skills/aew-example/SKILL.md",
            '---\nname: aew-example\ndescription: "Review a supplied change."\n'
            '---\n# Example\nInspect the requested artifact and report evidence.\n',
        )
        self.write(
            "skills/aew-example/agents/openai.yaml",
            'interface:\n  display_name: "Example"\n'
            '  short_description: "Review changes with concrete evidence"\n',
        )
        return folder

    def test_existing_relative_links_and_external_links_are_accepted(self):
        self.write("docs/actual file.md", "# File\n")
        path = self.write(
            "README.md",
            "[local](docs/actual%20file.md#section)\n"
            "[angle](<docs/actual file.md>)\n[external](https://example.com/missing)\n",
        )
        self.assertEqual([], markdown_errors(path, self.root))

    def test_missing_target_is_reported_but_fenced_examples_are_ignored(self):
        path = self.write(
            "README.md",
            "[broken](missing.md)\n"
            "```markdown\n[example](example.md)\n```\n"
            "`[inline](inline.md)`\n",
        )
        errors = markdown_errors(path, self.root)
        self.assertEqual(1, len(errors))
        self.assertIn("missing.md", errors[0])

    def test_link_escape_is_rejected_even_when_destination_exists(self):
        path = self.write("README.md", "[outside](../)\n")
        self.assertIn("escapes repository", markdown_errors(path, self.root)[0])

    def test_portable_skill_is_valid_and_mismatched_identity_is_rejected(self):
        folder = self.make_skill()
        self.assertEqual([], skill_errors(folder))
        path = folder / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "name: aew-example", "name: aew-other"
        ), encoding="utf-8")
        self.assertTrue(any("match folder" in error for error in skill_errors(folder)))

    def test_unfinished_skill_and_invalid_ui_metadata_are_rejected(self):
        folder = self.make_skill()
        path = folder / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "[TODO: finish]\n", encoding="utf-8")
        self.write(
            "skills/aew-example/agents/openai.yaml",
            'interface:\n  display_name: "Example"\n  short_description: "short"\n',
        )
        errors = skill_errors(folder)
        self.assertTrue(any("unfinished scaffold" in error for error in errors))
        self.assertTrue(any("25-64" in error for error in errors))

    def test_duplicate_frontmatter_is_rejected(self):
        folder = self.make_skill()
        path = folder / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "name: aew-example\n", "name: aew-example\nname: aew-example\n"
        ), encoding="utf-8")
        self.assertTrue(any("duplicate frontmatter" in error for error in skill_errors(folder)))

    def test_invalid_encoding_is_reported_without_crashing(self):
        self.write("README.md", "# Valid\n")
        self.write("AGENTS.md", "# Rules\n")
        self.write("docs/workflow.md", "# Workflow\n")
        self.write("docs/authorization.md", "# Permissions\n")
        self.make_skill()
        (self.root / "docs" / "invalid.md").write_bytes(b"\xff")
        errors, _, _ = validate(self.root)
        self.assertTrue(any("invalid UTF-8" in error for error in errors))


class PluginValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manifest = {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "dev-flow",
            "version": "0.1.0",
            "description": "Workflow skills",
            "author": {"name": "Publisher"},
            "extensions": {"com.openai": {"interface": {"displayName": "Workflow"}}},
        }
        self.catalog = {
            "name": "aew",
            "plugins": [{
                "name": "dev-flow",
                "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }],
        }

    def save(self):
        catalog = self.root / ".agents" / "plugins" / "marketplace.json"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(json.dumps(self.catalog) + "\n", encoding="utf-8")
        (self.root / "plugin.json").write_text(json.dumps(self.manifest) + "\n", encoding="utf-8")

    def test_root_package_and_catalog_match(self):
        self.save()
        self.assertEqual([], plugin_errors(self.root))

    def test_mismatched_plugin_identity_is_rejected(self):
        self.catalog["plugins"][0]["name"] = "other-plugin"
        self.save()
        self.assertTrue(any("identity" in error for error in plugin_errors(self.root)))

    def test_package_path_cannot_escape_or_point_at_another_folder(self):
        for path in ("./../", "./other", "/outside"):
            with self.subTest(path=path):
                self.catalog["plugins"][0]["source"]["path"] = path
                self.save()
                self.assertTrue(any("path" in error for error in plugin_errors(self.root)))

    def test_broken_json_is_reported(self):
        self.save()
        (self.root / "plugin.json").write_text("{broken", encoding="utf-8")
        self.assertTrue(any("invalid JSON" in error for error in plugin_errors(self.root)))

    def test_executable_component_is_rejected_for_this_package(self):
        self.save()
        (self.root / "mcp.json").write_text("{}\n", encoding="utf-8")
        self.assertTrue(any("unexpected component" in error for error in plugin_errors(self.root)))

    def test_invalid_version_and_install_policy_are_reported(self):
        self.manifest["version"] = "main"
        self.catalog["plugins"][0]["policy"]["installation"] = "INSTALLED_BY_DEFAULT"
        self.save()
        errors = plugin_errors(self.root)
        self.assertTrue(any("version" in error for error in errors))
        self.assertTrue(any("policy" in error for error in errors))


class SkillBoundaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / "skills/aew-example"
        (self.folder / "agents").mkdir(parents=True)
        self.entry = self.folder / "SKILL.md"
        self.entry.write_text(
            '---\nname: aew-example\ndescription: "Analizuj zmianę."\n---\n# Skill\n',
            encoding="utf-8",
        )
        (self.folder / "agents/openai.yaml").write_text(
            'interface:\n  display_name: "Przykład"\n'
            '  short_description: "Analiza zmiany z konkretnymi dowodami"\n',
            encoding="utf-8",
        )
        (self.root / "docs").mkdir()
        (self.root / "docs/workflow.md").write_text("# Standard\n", encoding="utf-8")

    def test_skill_cannot_require_repository_document(self):
        with self.entry.open("a", encoding="utf-8") as stream:
            stream.write("[standard](../../docs/workflow.md)\n")
        self.assertTrue(any("escapes skill" in error for error in skill_errors(self.folder)))

    def test_nested_reference_cannot_require_sibling(self):
        reference = self.folder / "references/details.md"
        reference.parent.mkdir()
        reference.write_text("[outside](../../../docs/workflow.md)\n", encoding="utf-8")
        self.assertTrue(any("escapes skill" in error for error in skill_errors(self.folder)))

    def test_own_reference_external_url_and_code_example_remain_valid(self):
        reference = self.folder / "references/details.md"
        reference.parent.mkdir()
        reference.write_text("[entry](../SKILL.md)\n", encoding="utf-8")
        with self.entry.open("a", encoding="utf-8") as stream:
            stream.write("[own](references/details.md)\n[docs](https://example.com/docs)\n"
                         "```md\n[example](../../missing.md)\n```\n")
        self.assertEqual([], skill_errors(self.folder))

    def test_local_absolute_dependency_is_rejected(self):
        for target in ("C:/outside/file.md", "file:///tmp/guide.md"):
            with self.subTest(target=target):
                original = self.entry.read_text(encoding="utf-8")
                self.entry.write_text(original + f"[local]({target})\n", encoding="utf-8")
                self.assertTrue(any("skill" in error for error in skill_errors(self.folder)))
                self.entry.write_text(original, encoding="utf-8")

    def test_skill_resource_symlink_escape(self):
        try:
            (self.folder / "outside.md").symlink_to(self.root / "docs/workflow.md")
        except (OSError, NotImplementedError):
            self.skipTest("Brak uprawnień do dowiązań; kontrola także w CI Linux.")
        self.assertTrue(any("escapes skill" in error for error in skill_errors(self.folder)))


if __name__ == "__main__":
    unittest.main()
