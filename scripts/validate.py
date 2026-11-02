"""Validate this repository's small document and skill format (Python 3.11+).

Only the documented two-field frontmatter and quoted UI metadata are supported.
This is not a general YAML parser or an agent behavior evaluation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED = {".git", ".local", ".venv", "__pycache__"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json"}
LINK = re.compile(r"!?\[[^\]\n]+\]\(([^)\n]+)\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
NAME = re.compile(r"^aew-[a-z0-9]+(?:-[a-z0-9]+)*$")


def outside_code(text: str) -> str:
    """Remove fenced examples and inline code before looking for links."""
    kept: list[str] = []
    marker = ""
    length = 0
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence:
            token, tail = fence.groups()
            if not marker:
                marker, length = token[0], len(token)
                continue
            if token[0] == marker and len(token) >= length and not tail.strip():
                marker = ""
                continue
        if not marker:
            kept.append(re.sub(r"(`+).*?\1", "", line))
    return "\n".join(kept)


def markdown_errors(path: Path, root: Path, *, boundary: str = "repository") -> list[str]:
    errors: list[str] = []
    for raw in LINK.findall(outside_code(path.read_text(encoding="utf-8"))):
        # Angle-bracket destinations can contain spaces; plain ones cannot.
        target = raw.strip()
        if target.startswith("<") and ">" in target:
            target = target[1:target.index(">")]
        else:
            target = target.split()[0] if target else ""
        parsed = urlsplit(target)
        if boundary == "skill" and (parsed.scheme == "file" or re.match(r"^[A-Za-z]:", target)):
            errors.append(f"{path.name}: absolute local dependency escapes skill: {target}")
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(root.resolve()):
            errors.append(f"{path.name}: link escapes {boundary}: {target}")
        elif not destination.exists():
            errors.append(f"{path.name}: missing local link: {target}")
    return errors


def quoted_value(value: str, field: str, errors: list[str]) -> str:
    try:
        decoded = json.loads(value)
        if isinstance(decoded, str) and decoded.strip():
            return decoded
    except (json.JSONDecodeError, TypeError):
        pass
    errors.append(f"{field}: expected a non-empty one-line JSON string")
    return ""


def skill_errors(folder: Path) -> list[str]:
    errors: list[str] = []
    path = folder / "SKILL.md"
    if not path.is_file():
        return [f"{folder.name}: missing SKILL.md"]
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.+)", text, re.DOTALL)
    if not match:
        return [f"{folder.name}: invalid frontmatter or empty instructions"]
    frontmatter, body = match.groups()
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        key, separator, value = line.partition(":")
        if not separator or key not in {"name", "description"} or key in fields:
            errors.append(f"{folder.name}: unsupported or duplicate frontmatter field")
            continue
        fields[key] = value.strip()
    name = fields.get("name", "")
    if not NAME.fullmatch(name) or len(name) > 64 or name != folder.name:
        errors.append(f"{folder.name}: name must match folder and use aew- prefix")
    description = quoted_value(fields.get("description", ""), "description", errors)
    if len(description) > 1024:
        errors.append(f"{folder.name}: description exceeds 1024 characters")
    if re.search(r"\[TODO:", body, re.IGNORECASE):
        errors.append(f"{folder.name}: unfinished scaffold")
    metadata = folder / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{folder.name}: missing agents/openai.yaml")
    else:
        values: dict[str, str] = {}
        lines = metadata.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "interface:":
            errors.append(f"{folder.name}: expected interface metadata")
        for line in lines[1:]:
            if not line.strip():
                continue
            match = re.fullmatch(
                r"  (display_name|short_description|default_prompt): (.+)", line
            )
            if not match or match[1] in values:
                errors.append(f"{folder.name}: unsupported or duplicate UI field")
                continue
            values[match[1]] = quoted_value(match[2], match[1], errors)
        if not values.get("display_name"):
            errors.append(f"{folder.name}: missing UI display_name")
        if not 25 <= len(values.get("short_description", "")) <= 64:
            errors.append(f"{folder.name}: UI description must have 25-64 characters")
        if "default_prompt" in values and f"${name}" not in values["default_prompt"]:
            errors.append(f"{folder.name}: default_prompt must mention the skill")
    for resource in sorted(folder.rglob("*")):
        if not resource.resolve().is_relative_to(folder.resolve()):
            errors.append(f"{folder.name}: resource escapes skill: {resource.name}")
        elif resource.is_file() and resource.suffix == ".md":
            errors.extend(markdown_errors(resource, folder, boundary="skill"))
    return errors


def json_object(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            return value
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        pass
    errors.append(f"{path.name}: missing or invalid JSON object")
    return {}


def plugin_errors(root: Path) -> list[str]:
    """Check this repository's one skills-only root package and local catalog."""
    errors: list[str] = []
    manifest = json_object(root / "plugin.json", errors)
    name = manifest.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("plugin.json: invalid plugin name")
    version = manifest.get("version", "")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        errors.append("plugin.json: expected a semantic package version")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("plugin.json: expected portable Agent Plugins schema")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        errors.append("plugin.json: missing description")
    author = manifest.get("author", {})
    if not isinstance(author, dict) or not author.get("name"):
        errors.append("plugin.json: missing publisher name")
    extensions = manifest.get("extensions", {})
    overlay = extensions.get("com.openai", {}) if isinstance(extensions, dict) else {}
    if not isinstance(overlay, dict):
        errors.append("plugin.json: invalid OpenAI metadata")
        overlay = {}
    interface = overlay.get("interface", {})
    if not isinstance(interface, dict) or not interface.get("displayName"):
        errors.append("plugin.json: missing displayName")
    if any(field in overlay for field in ("apps", "hooks")):
        errors.append("plugin.json: this package must remain skills-only")
    for entry in ("mcp.json", ".mcp.json", ".app.json", "hooks", ".codex-plugin"):
        if (root / entry).exists():
            errors.append(f"{entry}: unexpected component in skills-only portable package")
    catalog = json_object(root / ".agents" / "plugins" / "marketplace.json", errors)
    if catalog.get("name") != "aew":
        errors.append("marketplace.json: expected marketplace aew")
    entries = catalog.get("plugins", [])
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        errors.append("marketplace.json: expected one plugin entry")
        return errors
    entry = entries[0]
    if entry.get("name") != name:
        errors.append("marketplace.json: plugin identity does not match manifest")
    source = entry.get("source", {})
    if not isinstance(source, dict):
        source = {}
    path = source.get("path", "")
    if source.get("source") != "local" or not isinstance(path, str) or not path.startswith("./"):
        errors.append("marketplace.json: expected a ./ local package path")
    else:
        resolved = (root / path).resolve()
        if resolved != root.resolve():
            errors.append("marketplace.json: package path must resolve to repository root")
    if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        errors.append("marketplace.json: unexpected install/auth policy")
    if entry.get("category") != "Productivity":
        errors.append("marketplace.json: expected Productivity category")
    return errors


def validate(root: Path) -> tuple[list[str], int, int]:
    root = root.resolve()
    errors: list[str] = []
    files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and not EXCLUDED.intersection(path.relative_to(root).parts)
    )
    markdown_count = 0
    for path in files:
        if path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(root)}: invalid UTF-8")
            continue
        if text.startswith("\ufeff"):
            errors.append(f"{path.relative_to(root)}: unexpected byte-order mark")
        if text and not text.endswith("\n"):
            errors.append(f"{path.relative_to(root)}: missing final newline")
        if path.suffix == ".md":
            markdown_count += 1
            errors.extend(markdown_errors(path, root))
    skills_root = root / "skills"
    folders = sorted(path for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    if not folders:
        errors.append("skills/: no skills found")
    for folder in folders:
        try:
            errors.extend(skill_errors(folder))
        except UnicodeDecodeError:
            errors.append(f"{folder.name}: invalid UTF-8 skill metadata")
    for required in ("README.md", "AGENTS.md", "docs/workflow.md", "docs/authorization.md"):
        if not (root / required).is_file():
            errors.append(f"missing required file: {required}")
    errors.extend(plugin_errors(root))
    return errors, markdown_count, len(folders)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors, markdown_count, skill_count = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {markdown_count} Markdown files and {skill_count} skills.")
    print("Validated root plugin manifest and local marketplace catalog.")
    print("Scope: local file links, constrained metadata and package contracts; no agent runs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
