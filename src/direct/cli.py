"""Command-line interface for Direct."""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from direct.colors import color, BOLD, CYAN, DIM, GREEN, RED, YELLOW
from direct.manager import PathManager


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
    """Execute the CLI application.

    Args:
        argv: Command-line arguments excluding program name. Defaults to sys.argv[1:].

    Returns:
        int: Exit status code (0 for success, 1 for errors).
    """
    if argv is None:
        argv = sys.argv[1:]

    # Determine caller display name (e.g. 'direct' or 'python main.py')
    invoked_name = Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "direct"
    if invoked_name in ("main.py", "__main__.py"):
        display_name = "python main.py"
    else:
        display_name = "direct"

    manager = PathManager()
    paths = manager.list_paths()

    if not argv:
        display_paths(paths, script_name=display_name)
        return 0

    name = argv[0].strip()
    target_path = manager.resolve(name)

    if target_path:
        print(target_path)
        return 0

    error_label = color("ERROR", BOLD + RED)
    hint = color(f"run {display_name} with no arguments to list available keys", YELLOW)
    print(f"{error_label}: '{name}' is not a known path ({hint})")
    return 1


def main() -> None:
    """Entrypoint for console script."""
    sys.exit(run())
