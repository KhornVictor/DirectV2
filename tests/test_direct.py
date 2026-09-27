"""Unit tests for Direct shortcut manager including CRUD and interactive operations."""

import tempfile
from pathlib import Path
import pytest
from direct.colors import color, BOLD
from direct.config import load_paths, save_paths
from direct.manager import PathManager
from direct.interactive import (
    get_indexed_paths,
    find_by_number_or_name,
    interactive_menu,
)
from direct.cli import run


def test_colors_styling():
    formatted = color("test", BOLD)
    assert "test" in formatted


def test_manager_resolution():
    sample_paths = {
        "work": "C:\\Work",
        "home": "C:\\Users\\User",
    }
    manager = PathManager(paths=sample_paths)

    # Exact match
    assert manager.resolve("work") == "C:\\Work"
    # Case insensitive
    assert manager.resolve("WORK") == "C:\\Work"
    assert manager.resolve("  home  ") == "C:\\Users\\User"
    # Not found
    assert manager.resolve("unknown") is None


def test_manager_crud_operations():
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        manager = PathManager(paths={}, config_path=config_path)

        # 1. Add
        manager.add("test_key", "C:\\TestDir")
        assert manager.resolve("test_key") == "C:\\TestDir"
        assert manager.exists("TEST_KEY") is True

        # Prevent duplicate add without overwrite
        with pytest.raises(ValueError):
            manager.add("test_key", "C:\\DifferentDir")

        # 2. Update
        manager.update("TEST_KEY", "C:\\UpdatedDir")
        assert manager.resolve("test_key") == "C:\\UpdatedDir"

        # Update non-existent raises KeyError
        with pytest.raises(KeyError):
            manager.update("non_existent", "C:\\Path")

        # 3. Set (create or update)
        manager.set("new_key", "C:\\NewDir")
        assert manager.resolve("new_key") == "C:\\NewDir"
        manager.set("test_key", "C:\\OverwrittenDir")
        assert manager.resolve("test_key") == "C:\\OverwrittenDir"

        # 4. Remove
        old = manager.remove("test_key")
        assert old == "C:\\OverwrittenDir"
        assert manager.resolve("test_key") is None

        # Remove non-existent raises KeyError
        with pytest.raises(KeyError):
            manager.remove("test_key")


def test_config_save_and_reload():
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        paths_to_save = {
            "alpha": "C:\\Alpha\\Dir",
            "beta": "C:\\Beta\\Dir",
        }
        save_paths(paths_to_save, config_file=config_path)

        assert config_path.is_file()
        content = config_path.read_text(encoding="utf-8")
        assert "[paths]" in content
        assert "alpha = 'C:\\Alpha\\Dir'" in content

        import os
        os.environ["DIRECT_CONFIG"] = str(config_path)
        try:
            loaded_custom = load_paths()
            assert loaded_custom["alpha"] == "C:\\Alpha\\Dir"
            assert loaded_custom["beta"] == "C:\\Beta\\Dir"
        finally:
            del os.environ["DIRECT_CONFIG"]


def test_cli_add_and_remove(monkeypatch, capsys):
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        monkeypatch.setenv("DIRECT_CONFIG", str(config_path))

        # Add with explicit path
        exit_code = run(["add", "my_app", "C:\\Apps\\MyApp"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out
        assert "my_app" in captured.out

        # Resolve newly added
        exit_code = run(["my_app"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "C:\\Apps\\MyApp" in captured.out

        # Update
        exit_code = run(["update", "my_app", "C:\\Apps\\MyApp2"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out

        # Check updated
        exit_code = run(["my_app"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "C:\\Apps\\MyApp2" in captured.out

        # Remove
        exit_code = run(["rm", "my_app"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out

        # Verify removal
        exit_code = run(["my_app"])
        assert exit_code == 1


def test_cli_add_defaults_to_cwd(monkeypatch, capsys):
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        monkeypatch.setenv("DIRECT_CONFIG", str(config_path))

        exit_code = run(["add", "here"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out

        # Should resolve to current working directory
        exit_code = run(["here"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert str(Path.cwd().resolve()) in captured.out


def test_cli_help(capsys):
    exit_code = run(["help"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Direct - Directory Shortcut & Navigation Tool" in captured.out
    assert "Usage:" in captured.out


def test_cli_list(capsys):
    exit_code = run(["ls"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Available paths" in captured.out


def test_interactive_helpers():
    sample_paths = {
        "zeta": "C:\\Zeta",
        "alpha": "C:\\Alpha",
    }
    indexed = get_indexed_paths(sample_paths)
    assert indexed[0][1] == "alpha"
    assert indexed[1][1] == "zeta"

    # Match by number
    match_num = find_by_number_or_name("1", indexed)
    assert match_num == ("alpha", "C:\\Alpha")

    # Match by name (case-insensitive)
    match_name = find_by_number_or_name("ZETA", indexed)
    assert match_name == ("zeta", "C:\\Zeta")

    assert find_by_number_or_name("99", indexed) is None
    assert find_by_number_or_name("", indexed) is None


def test_interactive_menu_selection(monkeypatch):
    sample_paths = {"test": "C:\\TestPath"}
    manager = PathManager(paths=sample_paths)

    # Simulate entering "1" to select first item
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    selected = interactive_menu(manager)
    assert selected == "C:\\TestPath"


def test_interactive_menu_add_update_delete(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        manager = PathManager(paths={}, config_path=config_path)

        # 1. Add shortcut 'proj' -> 'C:\MyProj'
        # Choice: 'a' -> name: 'proj' -> path: 'C:\MyProj' -> Enter continue -> 'q' quit
        add_inputs = iter(["a", "proj", "C:\\MyProj", "", "q"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(add_inputs))
        interactive_menu(manager)
        assert manager.resolve("proj") == "C:\\MyProj"

        # 2. Update shortcut 'proj' -> 'C:\MyProjV2'
        # Choice: 'u' -> target: '1' -> new_path: 'C:\MyProjV2' -> Enter continue -> 'q' quit
        update_inputs = iter(["u", "1", "C:\\MyProjV2", "", "q"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(update_inputs))
        interactive_menu(manager)
        assert manager.resolve("proj") == "C:\\MyProjV2"

        # 3. Delete shortcut 'proj'
        # Choice: 'd' -> target: '1' -> confirm: 'y' -> Enter continue -> 'q' quit
        delete_inputs = iter(["d", "1", "y", "", "q"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(delete_inputs))
        interactive_menu(manager)
        assert manager.resolve("proj") is None
