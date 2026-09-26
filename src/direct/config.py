"""Configuration loader for Direct path shortcuts."""

import os
import tomllib
from pathlib import Path
from typing import Dict

# Fallback default paths if configuration file is not found
DEFAULT_PATHS: Dict[str, str] = {
    "me": r"C:\Desktop\Me",
    "techno": r"C:\Desktop\Student Online (SO)\Techno\I3-GIC-A\Semester2",
    "env": r"C:\Desktop\Student Online (SO)\Code",
    "duck": r"C:\Desktop\Rubber Duck",
    "mock": r"C:\Desktop\Student Online (SO)\Mock Exam",
    "rdtc": r"C:\Desktop\Student Online (SO)\RDTC\aero-service",
    "config": r"C:\Users\Khorn Victor\.config",
    "etec": r"C:\xampp\htdocs\ETEC",
    "camcycber": r"C:\Desktop\Student Online (SO)\Camcycber",
    "stj": r"C:\Desktop\Student Online (SO)\Techno\other\STJ",
    "autohotkey": r"C:\Users\Khorn Victor\OneDrive\Documents\AutoHotkey",
    "obsidian": r"C:\Desktop\Obsidean",
    "tool": r"C:\Tool",
    "drive": r"C:\Desktop\Drive",
}


def get_config_path() -> Path:
    """Resolve the location of the path.toml configuration file.

    Priority:
    1. DIRECT_CONFIG environment variable
    2. Repository root (parent of src/)
    3. Current working directory
    4. User home configuration directory (~/.config/direct/path.toml)
    """
    if env_path := os.getenv("DIRECT_CONFIG"):
        custom_path = Path(env_path).resolve()
        if custom_path.is_file():
            return custom_path

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
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
            paths = data.get("paths", {})
            if isinstance(paths, dict) and paths:
                return {str(k): str(v) for k, v in paths.items()}
    except Exception:
        # Fall back to defaults on parse or read errors
        pass

    return DEFAULT_PATHS.copy()
