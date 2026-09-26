"""Core path shortcut manager."""

from typing import Dict, Optional
from direct.config import load_paths


class PathManager:
    """Manages path aliases and directory resolutions."""

    def __init__(self, paths: Optional[Dict[str, str]] = None) -> None:
        """Initialize PathManager with custom paths or loaded from configuration."""
        self._paths: Dict[str, str] = paths if paths is not None else load_paths()

    @property
    def paths(self) -> Dict[str, str]:
        """Return the dictionary of configured paths."""
        return self._paths

    def resolve(self, name: str) -> Optional[str]:
        """Resolve a shortcut name to its directory path.

        Lookup is case-insensitive and trims surrounding whitespace.

        Args:
            name: The shortcut key to lookup.

        Returns:
            The resolved directory path string, or None if not found.
        """
        lookup = name.strip().lower()
        for key, path in self._paths.items():
            if key.lower() == lookup:
                return path
        return None

    def list_paths(self) -> Dict[str, str]:
        """Return a shallow copy of all registered paths."""
        return dict(self._paths)

    def exists(self, name: str) -> bool:
        """Check whether a shortcut key is defined."""
        return self.resolve(name) is not None
