"""Command-line interface for Direct with CRUD operations and interactive menu."""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from direct.colors import color, BOLD, CYAN, DIM, GREEN, RED, YELLOW
from direct.interactive import interactive_menu
from direct.manager import PathManager


def output_target_path(target_path: str) -> None:
    """Print the resolved path and write to DIRECT_JUMP_FILE if configured by shell."""
    if jump_file := os.getenv("DIRECT_JUMP_FILE"):
        try:
            Path(jump_file).write_text(target_path, encoding="utf-8")
        except Exception:
            pass
    print(target_path)


def display_paths(paths: Dict[str, str], script_name: str = "direct") -> None:
    """Print the formatted list of available path shortcuts."""
    print(f"{color('Available paths', BOLD + CYAN)}:")
    if not paths:
        print(f"  {color('(No paths configured)', DIM)}")
        return

    key_width = max(len(key) for key in paths)
    for index, (key, value) in enumerate(paths.items(), start=1):
        number = color(str(index).rjust(2), DIM)
        key_label = color(key.ljust(key_width), GREEN)
        arrow = color("->", DIM)
        print(f"  {number}. {key_label} {arrow} {value}")

    print()
    print(f"Usage: {color(f'{script_name} <name>', YELLOW)}")


def run(argv: Optional[List[str]] = None) -> int:
    """Execute the Direct shortcut resolver and interactive menu.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].

    Returns:
        int: Exit status code (0 for success, 1 for errors).
    """
    if argv is None:
        argv = sys.argv[1:]

    script_name = "direct"
    manager = PathManager()

    # If no arguments provided: launch interactive menu (or list paths if non-interactive)
    if not argv:
        if sys.stdin.isatty():
            selected_path = interactive_menu(manager, script_name=script_name)
            if selected_path:
                output_target_path(selected_path)
            return 0
        display_paths(manager.list_paths(), script_name=script_name)
        return 0

    # Resolve shortcut name using the go.py logic
    name = argv[0].strip().lower()
    target_path = manager.resolve(name)
    if target_path:
        output_target_path(target_path)
        return 0

    error_label = color("ERROR", BOLD + RED)
    hint = color(f"run {script_name} with no arguments to list available keys", YELLOW)
    print(f"{error_label}: '{argv[0]}' is not a known path ({hint})")
    return 1


def main() -> None:
    """Entrypoint for console script."""
    sys.exit(run())
