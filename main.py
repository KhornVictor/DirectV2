"""Entry point for Direct shortcut manager."""

import sys
from pathlib import Path

# Add src/ to sys.path so the module can run directly without installation
_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from direct.cli import main

if __name__ == "__main__":
    main()
