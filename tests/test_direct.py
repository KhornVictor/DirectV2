"""Unit tests for the Direct shortcut manager."""

import tempfile
from pathlib import Path
import pytest
from direct.colors import color, BOLD
from direct.config import load_paths
from direct.manager import PathManager
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


def test_manager_exists():
    manager = PathManager(paths={"code": "C:\\Code"})
    assert manager.exists("code") is True
    assert manager.exists("CODE") is True
    assert manager.exists("nonexistent") is False


def test_custom_toml_loading(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "path.toml"
        config_path.write_text(
            """
            [paths]
            custom = 'D:\\CustomProject'
            """,
            encoding="utf-8",
        )
        monkeypatch.setenv("DIRECT_CONFIG", str(config_path))
        paths = load_paths()
        assert paths.get("custom") == "D:\\CustomProject"


def test_cli_list_returns_zero(capsys):
    exit_code = run(argv=[])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Available paths" in captured.out


def test_cli_resolve_success(capsys):
    exit_code = run(argv=["me"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "C:\\Desktop\\Me" in captured.out


def test_cli_resolve_unknown(capsys):
    exit_code = run(argv=["nonexistent_xyz"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ERROR" in captured.out
