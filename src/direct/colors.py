"""ANSI terminal color and style utilities."""

import os
import sys

# ANSI colors (disabled when stdout is not a TTY or NO_COLOR is set)
USE_COLOR: bool = sys.stdout.isatty() and os.getenv("NO_COLOR") is None

RESET: str = "\033[0m"
BOLD: str = "\033[1m"
DIM: str = "\033[2m"
RED: str = "\033[31m"
GREEN: str = "\033[32m"
YELLOW: str = "\033[33m"
CYAN: str = "\033[36m"


def color(text: str, style: str) -> str:
    """Format text with ANSI style if color output is enabled."""
    if USE_COLOR:
        return f"{style}{text}{RESET}"
    return text
