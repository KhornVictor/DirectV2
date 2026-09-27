"""Command-line interface for Direct with CRUD operations and interactive menu."""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from direct.colors import color, BOLD, CYAN, DIM, GREEN, RED, YELLOW
from direct.interactive import interactive_menu
from direct.manager import PathManager


def display_paths(paths: Dict[str, str], script_name: str = "direct") -> None:
    """Print the formatted list of available path shortcuts."""
    print(f"{color('Available paths', BOLD + CYAN)}:")
    if not paths:
        print(f"  {color('(No paths configured)', DIM)}")
        print()
        print(f"Add one using: {color(f'{script_name} add <name> [path]', YELLOW)}")
        return

    key_width = max(len(key) for key in paths)
    for index, (key, value) in enumerate(paths.items(), start=1):
        number = color(str(index).rjust(2), DIM)
        key_label = color(key.ljust(key_width), GREEN)
        arrow = color("->", DIM)
        print(f"  {number}. {key_label} {arrow} {value}")

    print()
    print(f"Usage: {color(f'{script_name} <name>', YELLOW)}")
    print(f"       {color(f'{script_name} add <name> [path]', YELLOW)}")
    print(f"       {color(f'{script_name} remove <name>', YELLOW)}")


def display_help(script_name: str = "direct") -> None:
    """Display comprehensive command usage help."""
    title = color("Direct - Directory Shortcut & Navigation Tool", BOLD + CYAN)
    print(f"{title}\n")
    print(f"{color('Usage:', BOLD)}")
    print(f"  {color(script_name, GREEN)}                           Open interactive menu to view, add, edit, or delete")
    print(f"  {color(f'{script_name} <name>', GREEN)}                    Resolve and output the path for <name>")
    print(f"  {color(f'{script_name} add <name> [path]', GREEN)}         Add a shortcut (defaults to current directory)")
    print(f"  {color(f'{script_name} set <name> [path]', GREEN)}         Set or overwrite a shortcut (defaults to cwd)")
    print(f"  {color(f'{script_name} update <name> <path>', GREEN)}      Update an existing shortcut path")
    print(f"  {color(f'{script_name} rm <name>', GREEN)}                 Remove a shortcut (aliases: remove, del)")
    print(f"  {color(f'{script_name} ls', GREEN)}                        Print paths list without interactive menu (alias: list)")
    print(f"  {color(f'{script_name} menu', GREEN)}                      Launch interactive menu explicitly (alias: -i)")
    print(f"  {color(f'{script_name} help', GREEN)}                      Show this help guide\n")
    print(f"{color('Examples:', BOLD)}")
    print(f"  {script_name}                              # Opens interactive list & CRUD menu")
    print(f"  {script_name} add project                  # Adds current folder as 'project'")
    print(f"  {script_name} add work C:\\Projects\\Work     # Adds custom path as 'work'")
    print(f"  {script_name} update work C:\\NewPath        # Updates 'work'")
    print(f"  {script_name} rm project                   # Removes 'project'")
    print(f"  {script_name} work                         # Prints path for 'work'")


def resolve_path_input(path_input: Optional[str]) -> str:
    """Resolve a user path string or default to current directory."""
    if path_input:
        return str(Path(path_input).expanduser().resolve())
    return str(Path.cwd().resolve())


def handle_add(manager: PathManager, args: List[str], script_name: str) -> int:
    """Handle the 'add' command."""
    if not args:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut name is required.")
        print(f"Usage: {color(f'{script_name} add <name> [path]', YELLOW)}")
        return 1

    name = args[0].strip()
    path_arg = args[1].strip() if len(args) > 1 else None
    resolved_path = resolve_path_input(path_arg)

    try:
        manager.add(name, resolved_path)
    except ValueError as err:
        print(f"{color('ERROR', BOLD + RED)}: {err}")
        hint = color(
            f"Use '{script_name} update {name} <path>' or '{script_name} set {name} [path]' to overwrite.",
            YELLOW,
        )
        print(f"Hint: {hint}")
        return 1

    print(f"{color('SUCCESS', BOLD + GREEN)}: Added shortcut '{name}' -> '{resolved_path}'")
    if not Path(resolved_path).exists():
        print(f"{color('WARNING', BOLD + YELLOW)}: Target directory '{resolved_path}' does not currently exist.")
    return 0


def handle_update(manager: PathManager, args: List[str], script_name: str) -> int:
    """Handle the 'update' command."""
    if not args:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut name is required.")
        print(f"Usage: {color(f'{script_name} update <name> <path>', YELLOW)}")
        return 1

    name = args[0].strip()
    path_arg = args[1].strip() if len(args) > 1 else None
    resolved_path = resolve_path_input(path_arg)

    try:
        manager.update(name, resolved_path)
    except KeyError as err:
        print(f"{color('ERROR', BOLD + RED)}: {err}")
        hint = color(f"Use '{script_name} add {name} [path]' to create it.", YELLOW)
        print(f"Hint: {hint}")
        return 1

    print(f"{color('SUCCESS', BOLD + GREEN)}: Updated shortcut '{name}' -> '{resolved_path}'")
    if not Path(resolved_path).exists():
        print(f"{color('WARNING', BOLD + YELLOW)}: Target directory '{resolved_path}' does not currently exist.")
    return 0


def handle_set(manager: PathManager, args: List[str], script_name: str) -> int:
    """Handle the 'set' command (create or update)."""
    if not args:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut name is required.")
        print(f"Usage: {color(f'{script_name} set <name> [path]', YELLOW)}")
        return 1

    name = args[0].strip()
    path_arg = args[1].strip() if len(args) > 1 else None
    resolved_path = resolve_path_input(path_arg)

    try:
        _, was_updated = manager.set(name, resolved_path)
    except ValueError as err:
        print(f"{color('ERROR', BOLD + RED)}: {err}")
        return 1

    action = "Updated" if was_updated else "Added"
    print(f"{color('SUCCESS', BOLD + GREEN)}: {action} shortcut '{name}' -> '{resolved_path}'")
    if not Path(resolved_path).exists():
        print(f"{color('WARNING', BOLD + YELLOW)}: Target directory '{resolved_path}' does not currently exist.")
    return 0


def handle_remove(manager: PathManager, args: List[str], script_name: str) -> int:
    """Handle the 'remove'/'rm' command."""
    if not args:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut name to remove is required.")
        print(f"Usage: {color(f'{script_name} rm <name>', YELLOW)}")
        return 1

    name = args[0].strip()
    try:
        old_path = manager.remove(name)
    except KeyError as err:
        print(f"{color('ERROR', BOLD + RED)}: {err}")
        return 1

    print(f"{color('SUCCESS', BOLD + GREEN)}: Removed shortcut '{name}' (was '{old_path}')")
    return 0


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

    # When no arguments are provided:
    # In interactive terminal (TTY): launch the interactive CRUD menu.
    # In non-interactive environments (pipes/scripts): print static table.
    if not argv:
        if sys.stdin.isatty():
            selected_path = interactive_menu(manager, script_name=display_name)
            if selected_path:
                print(selected_path)
            return 0
        display_paths(manager.list_paths(), script_name=display_name)
        return 0

    command = argv[0].strip().lower()
    sub_args = argv[1:]

    # Explicit interactive menu command
    if command in ("menu", "-i", "--interactive"):
        selected_path = interactive_menu(manager, script_name=display_name)
        if selected_path:
            print(selected_path)
        return 0

    # Help commands
    if command in ("help", "--help", "-h"):
        display_help(script_name=display_name)
        return 0

    # Non-interactive list commands
    if command in ("list", "ls", "-l", "--list"):
        display_paths(manager.list_paths(), script_name=display_name)
        return 0

    # Create (Add)
    if command == "add":
        return handle_add(manager, sub_args, display_name)

    # Update
    if command == "update":
        return handle_update(manager, sub_args, display_name)

    # Set (Create or Update)
    if command == "set":
        return handle_set(manager, sub_args, display_name)

    # Delete (Remove)
    if command in ("remove", "rm", "del", "delete"):
        return handle_remove(manager, sub_args, display_name)

    # Explicit Get
    if command == "get":
        if not sub_args:
            print(f"Usage: {color(f'{display_name} get <name>', YELLOW)}")
            return 1
        target_path = manager.resolve(sub_args[0])
        if target_path:
            print(target_path)
            return 0
        error_label = color("ERROR", BOLD + RED)
        print(f"{error_label}: '{sub_args[0]}' is not a known path")
        return 1

    # Default action: resolve given name as a path shortcut
    target_path = manager.resolve(argv[0])
    if target_path:
        print(target_path)
        return 0

    error_label = color("ERROR", BOLD + RED)
    hint = color(f"run '{display_name}' with no arguments to list available keys", YELLOW)
    print(f"{error_label}: '{argv[0]}' is not a known path ({hint})")
    return 1


def main() -> None:
    """Entrypoint for console script."""
    sys.exit(run())
