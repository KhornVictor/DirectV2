"""Interactive terminal menu for Direct shortcut manager."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from direct.colors import color, BOLD, CYAN, DIM, GREEN, RED, YELLOW
from direct.manager import PathManager


def get_caller_cwd() -> str:
    """Return working directory from DIRECT_CALLER_DIR or fallback to cwd."""
    if caller_dir := os.getenv("DIRECT_CALLER_DIR"):
        return str(Path(caller_dir).resolve())
    return str(Path.cwd().resolve())


def get_indexed_paths(paths: Dict[str, str]) -> List[Tuple[int, str, str]]:
    """Return paths as a sorted list of (index, key, path) tuples."""
    sorted_items = sorted(paths.items(), key=lambda item: item[0].lower())
    return [(i, k, v) for i, (k, v) in enumerate(sorted_items, start=1)]


def print_table(indexed: List[Tuple[int, str, str]]) -> None:
    """Print the formatted list of shortcuts."""
    print(f"\n{color('Available paths', BOLD + CYAN)}:")
    if not indexed:
        print(f"  {color('(No paths configured)', DIM)}")
        return

    key_width = max(len(key) for _, key, _ in indexed)
    for index, key, value in indexed:
        number = color(str(index).rjust(2), DIM)
        key_label = color(key.ljust(key_width), GREEN)
        arrow = color("->", DIM)
        print(f"  {number}. {key_label} {arrow} {value}")


def find_by_number_or_name(
    user_input: str, indexed: List[Tuple[int, str, str]]
) -> Optional[Tuple[str, str]]:
    """Match user input against index numbers or key names."""
    cleaned = user_input.strip()
    if not cleaned:
        return None

    # Check if numeric index
    if cleaned.isdigit():
        idx = int(cleaned)
        for num, key, path in indexed:
            if num == idx:
                return key, path
        return None

    # Check if shortcut key name (case-insensitive)
    lookup = cleaned.lower()
    for _, key, path in indexed:
        if key.lower() == lookup:
            return key, path
    return None


def do_add(manager: PathManager, indexed: List[Tuple[int, str, str]]) -> None:
    """Interactively add a new shortcut."""
    print(f"\n{color('--- Add New Shortcut ---', BOLD + CYAN)}")
    try:
        name = input(f"{color('Enter shortcut name', BOLD)} (or 'q' to cancel): ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if not name or name.lower() in ("q", "quit", "exit"):
        print("Cancelled.")
        return

    # Check if shortcut name already exists
    existing = find_by_number_or_name(name, indexed)
    if existing:
        key, existing_path = existing
        try:
            confirm = input(
                f"Shortcut '{key}' already exists ({existing_path}). Overwrite? [y/N]: "
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return
        if confirm not in ("y", "yes"):
            print("Cancelled.")
            return

    cwd_str = get_caller_cwd()
    try:
        path_input = input(
            f"{color('Enter directory path', BOLD)} [Enter for current: {cwd_str}]: "
        ).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    target_path = str(Path(path_input).expanduser().resolve()) if path_input else cwd_str

    manager.set(name, target_path)
    print(f"{color('SUCCESS', BOLD + GREEN)}: Saved shortcut '{name}' -> '{target_path}'")
    if not Path(target_path).exists():
        print(f"{color('WARNING', BOLD + YELLOW)}: Directory '{target_path}' does not currently exist on disk.")

    try:
        input(color("\nPress Enter to continue...", DIM))
    except (KeyboardInterrupt, EOFError):
        pass


def do_update(manager: PathManager, indexed: List[Tuple[int, str, str]]) -> None:
    """Interactively update an existing shortcut."""
    if not indexed:
        print(f"\n{color('No shortcuts available to update.', YELLOW)}")
        try:
            input(color("Press Enter to continue...", DIM))
        except (KeyboardInterrupt, EOFError):
            pass
        return

    print(f"\n{color('--- Update Shortcut ---', BOLD + CYAN)}")
    try:
        target = input(
            f"{color('Enter number or shortcut name to update', BOLD)} (or 'q' to cancel): "
        ).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if not target or target.lower() in ("q", "quit", "exit"):
        print("Cancelled.")
        return

    match = find_by_number_or_name(target, indexed)
    if not match:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut '{target}' not found.")
        try:
            input(color("Press Enter to continue...", DIM))
        except (KeyboardInterrupt, EOFError):
            pass
        return

    key, old_path = match
    print(f"Selected: {color(key, GREEN)} (currently: {old_path})")

    cwd_str = get_caller_cwd()
    try:
        new_path_input = input(
            f"{color('Enter new path', BOLD)} [Enter to keep, '.' for cwd]: "
        ).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if not new_path_input:
        print("No changes made.")
        return

    new_path = cwd_str if new_path_input == "." else str(Path(new_path_input).expanduser().resolve())
    manager.update(key, new_path)
    print(f"{color('SUCCESS', BOLD + GREEN)}: Updated shortcut '{key}' -> '{new_path}'")
    if not Path(new_path).exists():
        print(f"{color('WARNING', BOLD + YELLOW)}: Directory '{new_path}' does not currently exist on disk.")

    try:
        input(color("\nPress Enter to continue...", DIM))
    except (KeyboardInterrupt, EOFError):
        pass


def do_delete(manager: PathManager, indexed: List[Tuple[int, str, str]]) -> None:
    """Interactively delete an existing shortcut."""
    if not indexed:
        print(f"\n{color('No shortcuts available to delete.', YELLOW)}")
        try:
            input(color("Press Enter to continue...", DIM))
        except (KeyboardInterrupt, EOFError):
            pass
        return

    print(f"\n{color('--- Delete Shortcut ---', BOLD + CYAN)}")
    try:
        target = input(
            f"{color('Enter number or shortcut name to delete', BOLD)} (or 'q' to cancel): "
        ).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if not target or target.lower() in ("q", "quit", "exit"):
        print("Cancelled.")
        return

    match = find_by_number_or_name(target, indexed)
    if not match:
        print(f"{color('ERROR', BOLD + RED)}: Shortcut '{target}' not found.")
        try:
            input(color("Press Enter to continue...", DIM))
        except (KeyboardInterrupt, EOFError):
            pass
        return

    key, old_path = match
    try:
        confirm = input(
            f"Are you sure you want to delete {color(key, GREEN)} ({old_path})? [y/N]: "
        ).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    if confirm in ("y", "yes"):
        manager.remove(key)
        print(f"{color('SUCCESS', BOLD + GREEN)}: Deleted shortcut '{key}'")
    else:
        print("Deletion cancelled.")

    try:
        input(color("\nPress Enter to continue...", DIM))
    except (KeyboardInterrupt, EOFError):
        pass


def interactive_menu(manager: PathManager, script_name: str = "direct") -> Optional[str]:
    """Run the interactive CRUD menu loop.

    Returns:
        Optional[str]: Target directory path if selected by user, or None if exited.
    """
    while True:
        indexed = get_indexed_paths(manager.list_paths())
        print_table(indexed)

        count = len(indexed)
        range_hint = f"1-{count}" if count > 1 else ("1" if count == 1 else "")
        select_hint = f"[{range_hint}] Select path | " if range_hint else ""

        print(f"\n{color('Actions:', BOLD)}")
        print(f"  {select_hint}[a] Add | [u] Update | [d] Delete | [q] Quit")

        try:
            choice = input(f"\n{color('Choice', CYAN)}> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None

        if not choice or choice.lower() in ("q", "quit", "exit"):
            return None

        lowered = choice.lower()
        if lowered in ("a", "add"):
            do_add(manager, indexed)
        elif lowered in ("u", "update", "edit"):
            do_update(manager, indexed)
        elif lowered in ("d", "del", "delete", "rm", "remove"):
            do_delete(manager, indexed)
        else:
            match = find_by_number_or_name(choice, indexed)
            if match:
                _, path = match
                return path
            print(f"{color('ERROR', BOLD + RED)}: '{choice}' is not a valid action or shortcut.")
            try:
                input(color("Press Enter to continue...", DIM))
            except (KeyboardInterrupt, EOFError):
                pass
