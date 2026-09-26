"""Direct - Fast directory navigation and path shortcut manager."""

__version__ = "0.1.0"

from direct.colors import color
from direct.config import get_config_path, load_paths
from direct.manager import PathManager

__all__ = [
    "PathManager",
    "color",
    "get_config_path",
    "load_paths",
    "__version__",
]
