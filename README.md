# Direct

A lightweight, fast directory navigation and shortcut bookmark manager for Windows and cross-platform terminals.

---

## Features

- **CRUD Operations**: Create, read, update, and remove path shortcuts directly from your terminal.
- **Auto Current-Directory**: Simply run `direct add <name>` to bookmark your current folder.
- **External Configuration**: Automatically synchronizes with [`path.toml`](file:///C:/Tool/Direct/path.toml).
- **Case-Insensitive Resolution**: Jump to shortcuts regardless of capitalization (e.g. `direct me`, `direct ME`, `direct Me`).
- **ANSI Color Output**: Formatted overview with automatic TTY and `NO_COLOR` detection.
- **Multiple Entry Points**: Run as a CLI command (`direct`), module (`python -m direct`), or standalone (`python main.py`).

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
│       ├── cli.py             # CLI parser, formatting, and CRUD handlers
│       ├── colors.py          # ANSI colors and styling helpers
│       ├── config.py          # TOML configuration loader and saver
│       └── manager.py         # PathManager domain logic (CRUD & resolve)
└── tests/
    └── test_direct.py         # Unit tests (pytest)
```

---

## Terminal Commands (CRUD)

| Operation | Command | Description |
|---|---|---|
| **Create** | `direct add <name> [path]` | Add a new shortcut (defaults to current working directory if path is omitted) |
| **Set** | `direct set <name> [path]` | Create or overwrite a shortcut (defaults to current directory) |
| **Read (List)** | `direct` or `direct ls` | Display formatted list of all registered shortcuts |
| **Read (Get)** | `direct <name>` | Output target directory path (for terminal navigation / jumping) |
| **Update** | `direct update <name> <path>` | Update an existing shortcut to a new path |
| **Delete** | `direct rm <name>` | Remove a shortcut (`aliases: remove, del, delete`) |
| **Help** | `direct help` | Show usage commands and examples |

### Examples

```powershell
# 1. Add current working directory as 'myproject'
cd C:\Projects\MyProject
direct add myproject

# 2. Add an explicit path
direct add work C:\Company\Repository

# 3. Update existing shortcut
direct update work C:\Company\NewRepository

# 4. Remove a shortcut
direct rm myproject

# 5. Resolve path
direct work
# Output: C:\Company\NewRepository
```

---

## Configuration (`path.toml`)

Direct automatically updates [`path.toml`](file:///C:/Tool/Direct/path.toml) whenever you add, update, or remove shortcuts:

```toml
[paths]
config = 'C:\Users\Khorn Victor\.config'
me = 'C:\Desktop\Me'
tool = 'C:\Tool'
```

### Configuration Priority
1. `DIRECT_CONFIG` environment variable.
2. Root [`path.toml`](file:///C:/Tool/Direct/path.toml).
3. Current working directory `path.toml`.
4. User config directory: `~/.config/direct/path.toml`.

---

## PowerShell Jump Integration

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

```powershell
uv run pytest
```
