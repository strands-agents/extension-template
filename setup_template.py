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

    # Remove template-specific files that don't belong to the user's project
    cleanup_targets = [
        "CODE_OF_CONDUCT.md",  # template repo's own conduct file
        "CONTRIBUTING.md",     # template repo's own contributing guide
        "NOTICE",              # Amazon's copyright notice for the template
    ]
    for target in cleanup_targets:
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            print(f"  ✓ Removed {target}")

    # Remove this setup script
    script_path = os.path.abspath(__file__)
    if os.path.exists(script_path):
        os.remove(script_path)
        print("  ✓ Removed setup_template.py")

    print("\n✅ Setup complete!\n")
    print("Next steps:")
    print("  1. Review the generated files")
    print("  2. Install dev dependencies: pip install -e '.[dev]'")
    print("  3. Run checks: hatch run prepare")
    print("  4. Start implementing your components")
    print()


if __name__ == "__main__":
    main()
