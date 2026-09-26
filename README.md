# Direct

A lightweight, fast directory navigation and shortcut bookmark manager for Windows and cross-platform terminals.

---

## Features

- **Modular Architecture**: Clean separation between configuration, path resolution, styling, and CLI presentation.
- **External Configuration**: Manage your shortcuts easily in [`path.toml`](file:///C:/Tool/Direct/path.toml) without touching code.
- **Case-Insensitive Resolution**: Jump to shortcuts regardless of capitalization (e.g. `direct me`, `direct ME`, `direct Me`).
- **ANSI Color Output**: Formatted numbered overview with automatic TTY and `NO_COLOR` detection.
- **Multiple Entry Points**: Run as an installed console script (`direct`), via python module (`python -m direct`), or standalone (`python main.py`).

---

## Project Structure

```
Direct/
├── path.toml                  # Path shortcuts configuration
├── pyproject.toml             # Project metadata, dependencies, and CLI script entrypoint
├── README.md                  # Project documentation
├── main.py                    # Root entrypoint (backward-compatible)
├── src/
│   └── direct/
│       ├── __init__.py        # Package exports
│       ├── __main__.py        # Entrypoint for `python -m direct`
│       ├── cli.py             # CLI parser, formatting, and user interaction
│       ├── colors.py          # ANSI colors and styling helpers
│       ├── config.py          # TOML configuration loader and path fallback
│       └── manager.py         # PathManager domain logic (lookup, resolve, list)
└── tests/
    └── test_direct.py         # Unit tests (pytest)
```

---

## Configuration (`path.toml`)

Add or edit your path shortcuts in [`path.toml`](file:///C:/Tool/Direct/path.toml). Use single quotes for Windows paths to avoid backslash escaping:

```toml
[paths]
me = 'C:\Desktop\Me'
tool = 'C:\Tool'
config = 'C:\Users\Khorn Victor\.config'
```

### Configuration Priority
Direct searches for the configuration file in this order:
1. `DIRECT_CONFIG` environment variable.
2. Root [`path.toml`](file:///C:/Tool/Direct/path.toml).
3. Current working directory `path.toml`.
4. User config directory: `~/.config/direct/path.toml`.

---

## Usage

### 1. List all available shortcuts
```powershell
direct
# or
python main.py
```

### 2. Resolve a path shortcut
```powershell
direct me
# Output: C:\Desktop\Me
```

### 3. PowerShell Jump Integration
Add this function to your PowerShell `$PROFILE` (run `notepad $PROFILE`):

```powershell
function go($name) {
    if (-not $name) {
        direct
        return
    }
    $target = direct $name
    if ($LASTEXITCODE -eq 0 -and (Test-Path $target)) {
        Set-Location $target
    }
}
```

Now you can quickly jump anywhere from any terminal:
```powershell
go me
go tool
go config
```

---

## Development & Testing

Install dependencies and run tests:

```powershell
uv sync
uv run pytest
```
