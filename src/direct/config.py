"""Configuration loader and saver for Direct path shortcuts."""

import os
import tomllib
from pathlib import Path
from typing import Dict, Optional

# Fallback default paths if configuration file is not found
DEFAULT_PATHS: Dict[str, str] = {}


def get_config_path() -> Path:
    """Resolve the location of the path.toml configuration file.

    Priority:
    1. DIRECT_CONFIG environment variable
    2. Repository root (parent of src/)
    3. Current working directory
    4. User home configuration directory (~/.config/direct/path.toml)
    """
    if env_path := os.getenv("DIRECT_CONFIG"):
        return Path(env_path).resolve()

    # Check project root directory relative to this file: src/direct/config.py -> ../../path.toml
    repo_config = Path(__file__).resolve().parent.parent.parent / "path.toml"
    if repo_config.is_file():
        return repo_config

    cwd_config = Path.cwd() / "path.toml"
    if cwd_config.is_file():
        return cwd_config

    user_config = Path.home() / ".config" / "direct" / "path.toml"
    if user_config.is_file():
        return user_config

    return repo_config


def load_paths() -> Dict[str, str]:
    """Load path shortcuts from the configuration file.

    Returns:
        Dict[str, str]: Mapping of shortcut names to file system paths.
    """
    config_file = get_config_path()
    if not config_file.is_file():
        return DEFAULT_PATHS.copy()

    try:
        with open(config_file, "rb") as file:
            data = tomllib.load(file)
            paths = data.get("paths", {})
            if isinstance(paths, dict) and paths:
                return {str(k): str(v) for k, v in paths.items()} # type: ignore
    except Exception:
        pass

    return DEFAULT_PATHS.copy()


def save_paths(paths: Dict[str, str], config_file: Optional[Path] = None) -> Path:
    """Save path shortcuts dictionary to path.toml configuration file.

    Args:
        paths: Mapping of shortcut names to file system paths.
        config_file: Optional target configuration file path.

    Returns:
        Path: The path to the saved configuration file.
    """
    if config_file is None:
        config_file = get_config_path()

    config_file.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Direct - Path Shortcuts Configuration",
        "# Use single quotes for Windows paths to avoid backslash escaping issues.",
        "",
        "[paths]",
    ]
    for key, val in sorted(paths.items(), key=lambda item: item[0].lower()):
        escaped_val = str(val).replace("'", "\\'")
        lines.append(f"{key} = '{escaped_val}'")
    lines.append("")

    config_file.write_text("\n".join(lines), encoding="utf-8")
    return config_file