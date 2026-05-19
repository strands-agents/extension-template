#!/usr/bin/env python3
"""
Template Setup Script

Run this after cloning the template to customize it for your project.
This script will:
1. Ask for your project details
2. Ask which components you want to keep
3. Rename files and directories
4. Replace placeholder values throughout the codebase
5. Delete unused components
6. Delete itself when done

Usage:
    python setup_template.py
"""

import os
import re
import shutil
import sys

COMPONENTS = {
    "tool": {
        "name": "Tool",
        "description": "Add capabilities to agents using the @tool decorator",
        "files": ["tool.py"],
        "test_files": ["test_tool.py"],
        "exports": ["template_tool"],
    },
    "model": {
        "name": "Model Provider",
        "description": "Integrate custom LLM APIs",
        "files": ["model.py"],
        "test_files": ["test_model.py"],
        "exports": ["TemplateModel"],
    },
    "plugin": {
        "name": "Plugin",
        "description": "Extend agent behavior with hooks and tools in a composable package",
        "files": ["plugin.py"],
        "test_files": ["test_plugin.py"],
        "exports": ["TemplatePlugin"],
    },
    "session_manager": {
        "name": "Session Manager",
        "description": "Persist conversations across restarts",
        "files": ["session_manager.py"],
        "test_files": ["test_session_manager.py"],
        "exports": ["TemplateSessionManager"],
    },
    "conversation_manager": {
        "name": "Conversation Manager",
        "description": "Control context window and message history",
        "files": ["conversation_manager.py"],
        "test_files": ["test_conversation_manager.py"],
        "exports": ["TemplateConversationManager"],
    },
}


def to_snake_case(name: str) -> str:
    """Convert to snake_case (e.g., my_tool)."""
    s = re.sub(r"[-\s]+", "_", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_pascal_case(name: str) -> str:
    """Convert to PascalCase (e.g., MyTool)."""
    words = re.split(r"[-_\s]+", name)
    return "".join(word.capitalize() for word in words)


def to_kebab_case(name: str) -> str:
    """Convert to kebab-case (e.g., my-tool)."""
    s = to_snake_case(name)
    return s.replace("_", "-")


def get_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default."""
    if default:
        result = input(f"{prompt} [{default}]: ").strip()
        return result if result else default
    return input(f"{prompt}: ").strip()


def select_components() -> list[str]:
    """Prompt user to select which components to keep."""
    print("\nWhich components do you want to include?\n")

    for i, (key, info) in enumerate(COMPONENTS.items(), 1):
        print(f"  {i}. {info['name']} - {info['description']}")

    print()
    selection = get_input("Enter numbers separated by commas (e.g., 1,2)", "1")

    selected = []
    for num in selection.split(","):
        num = num.strip()
        if num.isdigit():
            idx = int(num) - 1
            if 0 <= idx < len(COMPONENTS):
                selected.append(list(COMPONENTS.keys())[idx])

    if not selected:
        print("❌ No valid components selected")
        sys.exit(1)

    return selected


def replace_in_file(filepath: str, replacements: dict[str, str]) -> None:
    """Replace all occurrences in a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def update_init_file(src_dir: str, selected: list[str], replacements: dict[str, str]) -> None:
    """Update __init__.py to only export selected components."""
    init_path = os.path.join(src_dir, "__init__.py")

    imports = []
    exports = []

    for key in selected:
        info = COMPONENTS[key]
        for export in info["exports"]:
            # Apply replacements to get the new name
            new_export = export
            for old, new in replacements.items():
                new_export = new_export.replace(old, new)

            module = info["files"][0].replace(".py", "")
            # Apply replacements to module name too
            new_module = module
            for old, new in replacements.items():
                new_module = new_module.replace(old, new)

            # Get the package name from src_dir (apply replacements for renamed package)
            package_name = os.path.basename(src_dir)
            for old, new in replacements.items():
                package_name = package_name.replace(old, new)
            imports.append(f"from {package_name}.{new_module} import {new_export}")
            exports.append(f'    "{new_export}",')

    imports.sort()
    exports.sort()

    content = f'''"""Strands Package."""

{chr(10).join(imports)}

__all__ = [
{chr(10).join(exports)}
]
'''

    with open(init_path, "w", encoding="utf-8") as f:
        f.write(content)


def delete_unused_components(src_dir: str, selected: list[str]) -> None:
    """Delete component files that weren't selected."""
    for key, info in COMPONENTS.items():
        if key not in selected:
            # Delete source files
            for filename in info["files"]:
                filepath = os.path.join(src_dir, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"  ✓ Removed {filepath}")

            # Delete test files
            for filename in info["test_files"]:
                filepath = os.path.join("tests", filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"  ✓ Removed {filepath}")


def _strip_monorepo_from_pyproject() -> None:
    """Drop the monorepo-only [tool.hatch.version.raw-options] block."""
    path = "pyproject.toml"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text = re.sub(
        r"\n\[tool\.hatch\.version\.raw-options\][^\[]*",
        "\n",
        text,
        count=1,
    )
    if new_text != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"  ✓ De-monorepoized {path}")


def _strip_monorepo_from_readme() -> None:
    """Drop the monorepo callout and the python-v tag-prefix wording."""
    path = "README.md"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out: list[str] = []
    # The "Run the setup script" section walks users through a script that has
    # self-deleted by the time they read this README, so drop it and renumber
    # the next heading.
    skip_setup_section = False
    for line in lines:
        if line.startswith("### 2. Run the setup script"):
            skip_setup_section = True
            continue
        if skip_setup_section:
            if line.startswith("### "):
                skip_setup_section = False
                out.append(line.replace("### 3. ", "### 2. ", 1))
            continue
        if "This is the Python half of the" in line:
            continue
        # The hoist puts the package at the repo root, so the python/ subdir
        # referenced in the clone instructions no longer exists.
        line = line.replace("cd your-repo-name/python", "cd your-repo-name")
        if "tag prefixed `python-v`" in line:
            line = (
                "2. Create a release on GitHub with a tag prefixed `v`, "
                "e.g. `v0.1.0`. hatch-vcs strips the prefix so the package "
                "version is just `0.1.0`.\n"
            )
        out.append(line)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(out)
    print(f"  ✓ De-monorepoized {path}")


def _hoist_workflows() -> None:
    """Rewrite python workflow files in place and rename to root names."""
    workflows_dir = "../.github/workflows"
    ci_src = os.path.join(workflows_dir, "ci-python.yml")
    if os.path.exists(ci_src):
        with open(ci_src, "r", encoding="utf-8") as f:
            ci = f.read()
        ci = ci.replace("name: CI - Python", "name: CI")
        ci = re.sub(r"\n    paths:\n(?:      - .+\n)+", "\n", ci)
        ci = re.sub(r"\ndefaults:\n  run:\n    working-directory: python\n", "\n", ci)
        ci_dst = os.path.join(workflows_dir, "ci.yml")
        with open(ci_dst, "w", encoding="utf-8") as f:
            f.write(ci)
        os.remove(ci_src)
        print(f"  ✓ Renamed {ci_src} → {ci_dst}")

    pub_src = os.path.join(workflows_dir, "publish-python.yml")
    if os.path.exists(pub_src):
        with open(pub_src, "r", encoding="utf-8") as f:
            pub = f.read()
        pub = pub.replace("name: Publish Python to PyPI", "name: Publish to PyPI")
        # Drop "Triggered when a release is published with a tag prefixed `python-v`..." comment
        pub = re.sub(r"\n# Triggered when[^\n]*\n(?:# [^\n]*\n)*", "\n", pub)
        # Drop check-tag job and `needs: check-tag` + `if:` guard
        pub = re.sub(
            r"  check-tag:\n(?:    [^\n]*\n|\n)+?(?=\n  [a-z])",
            "",
            pub,
        )
        pub = re.sub(r"    needs: check-tag\n    if: [^\n]+\n", "", pub)
        pub = re.sub(r"\ndefaults:\n  run:\n    working-directory: python\n", "\n", pub)
        pub = pub.replace("path: python/dist/", "path: dist/")
        pub_dst = os.path.join(workflows_dir, "publish.yml")
        with open(pub_dst, "w", encoding="utf-8") as f:
            f.write(pub)
        os.remove(pub_src)
        print(f"  ✓ Renamed {pub_src} → {pub_dst}")


def _hoist_to_root() -> str:
    """Move contents of cwd (python/) to repo root, chdir there. Returns new cwd."""
    src_root = os.path.abspath(".")
    dst_root = os.path.abspath("..")
    for entry in os.listdir(src_root):
        src = os.path.join(src_root, entry)
        dst = os.path.join(dst_root, entry)
        if os.path.exists(dst):
            if os.path.isdir(dst) and not os.path.islink(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        shutil.move(src, dst)
    os.chdir(dst_root)
    os.rmdir(src_root)
    print(f"  ✓ Hoisted python/ contents to repo root")
    return dst_root


def main() -> None:
    print("\n🔧 Strands Template Setup\n")
    print("This will customize the template for your project.\n")

    # Gather information
    package_name = get_input("Package name (e.g., 'google', 'aws', 'slack')")
    if not package_name:
        print("❌ Package name is required")
        sys.exit(1)

    # Generate variations
    snake_name = to_snake_case(package_name)
    pascal_name = to_pascal_case(package_name)
    kebab_name = to_kebab_case(package_name)

    print(f"\n  PyPI package: strands-{kebab_name}")
    print(f"  Module:       strands_{snake_name}")
    print(f"  Classes:      {pascal_name}Model, {pascal_name}Hooks, etc.")

    # Select components
    selected = select_components()
    selected_names = [COMPONENTS[k]["name"] for k in selected]
    print(f"\n  Selected: {', '.join(selected_names)}")

    # Optional info
    print()
    author_name = get_input("Author name", "Your Name")
    author_email = get_input("Author email", "your.email@example.com")
    github_username = get_input("GitHub username", "yourusername")
    description = get_input("Package description", f"Strands Agents components for {package_name}")

    # Confirm
    print("\n" + "=" * 50)
    confirm = get_input("\nProceed with setup? (y/n)", "y")
    if confirm.lower() != "y":
        print("Setup cancelled.")
        sys.exit(0)

    print("\n⏳ Setting up project...\n")

    # Define replacements
    replacements = {
        # Package/module names
        "strands-template": f"strands-{kebab_name}",
        "strands_template": f"strands_{snake_name}",
        # Class names
        "TemplateModel": f"{pascal_name}Model",
        "TemplatePlugin": f"{pascal_name}Plugin",
        "TemplateSessionManager": f"{pascal_name}SessionManager",
        "TemplateConversationManager": f"{pascal_name}ConversationManager",
        # Function names
        "template_tool": f"{snake_name}_tool",
        # Plugin name
        "template-plugin": f"{kebab_name}-plugin",
        # Author info
        "Your Name": author_name,
        "your.email@example.com": author_email,
        "yourusername": github_username,
        "Your package description": description,
    }

    # Determine which files to process based on selection
    files_to_process = ["pyproject.toml", "README.md"]

    for key in selected:
        info = COMPONENTS[key]
        for filename in info["files"]:
            files_to_process.append(f"src/strands_template/{filename}")
        for filename in info["test_files"]:
            files_to_process.append(f"tests/{filename}")

    # Always process __init__.py
    files_to_process.append("src/strands_template/__init__.py")

    # Process files
    for filepath in files_to_process:
        if os.path.exists(filepath):
            replace_in_file(filepath, replacements)
            print(f"  ✓ Updated {filepath}")

    # Delete unused components
    print("\n🗑️  Removing unused components...")
    delete_unused_components("src/strands_template", selected)

    # Update __init__.py with only selected exports
    new_src = f"src/strands_{snake_name}"
    update_init_file("src/strands_template", selected, replacements)

    # Rename source directory
    old_src = "src/strands_template"
    if os.path.exists(old_src) and old_src != new_src:
        shutil.move(old_src, new_src)
        print(f"\n  ✓ Renamed {old_src} → {new_src}")

    # Clean up
    print("\n🧹 Cleaning up...")

    # Remove template-specific files that don't belong to the user's project.
    # These live at the repo root (one level up from python/) since this is a
    # monorepo template.
    cleanup_targets = [
        "../CODE_OF_CONDUCT.md",  # template repo's own conduct file
        "../CONTRIBUTING.md",     # template repo's own contributing guide
        "../NOTICE",              # Amazon's copyright notice for the template
    ]
    for target in cleanup_targets:
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            print(f"  ✓ Removed {target}")

    # Optionally drop the sibling TypeScript half of the monorepo and hoist
    # this package to the repo root so the generated repo looks like a normal
    # single-language project.
    print()
    drop_sibling = get_input("Drop the TypeScript half and hoist this package to the repo root? (y/n)", "y")
    hoisted = False
    if drop_sibling.lower() == "y":
        sibling_targets = [
            "../typescript",
            "../.github/workflows/ci-typescript.yml",
            "../.github/workflows/publish-typescript.yml",
            "../README.md",
        ]
        for target in sibling_targets:
            if os.path.exists(target):
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                print(f"  ✓ Removed {target}")

        _strip_monorepo_from_pyproject()
        _strip_monorepo_from_readme()
        _hoist_workflows()
        _hoist_to_root()
        hoisted = True

    # Remove this setup script (path may have changed if we hoisted).
    script_path = os.path.abspath("setup_template.py" if hoisted else __file__)
    if os.path.exists(script_path):
        os.remove(script_path)
        print("  ✓ Removed setup_template.py")

    print("\n✅ Setup complete!\n")
    if hoisted:
        print(
            "⚠️  Your shell is still in the now-deleted python/ directory. "
            "Run `cd ..` before continuing.\n"
        )
    print("Next steps:")
    print("  1. Review the generated files")
    print("  2. Install dev dependencies: pip install -e '.[dev]'")
    print("  3. Run checks: hatch run prepare")
    print("  4. Start implementing your components")
    print()


if __name__ == "__main__":
    main()
