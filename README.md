# Direct

A lightweight, fast directory navigation and shortcut bookmark manager for Windows and cross-platform terminals.

---

## Features

- **Interactive Terminal Menu**: Type `direct` to open the interactive list where you can select, add, update, and delete shortcuts in real time.
- **Fast CLI CRUD**: Create, read, update, and remove path shortcuts directly from terminal commands or inside the menu.
- **Auto Current-Directory**: Simply add a shortcut name to bookmark your current folder without typing the full path.
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
│       ├── cli.py             # CLI parser and command routing
│       ├── colors.py          # ANSI colors and styling helpers
│       ├── config.py          # TOML configuration loader and saver
│       ├── interactive.py     # Interactive terminal menu (list, select, add, edit, delete)
│       └── manager.py         # PathManager domain logic (CRUD & resolve)
└── tests/
    └── test_direct.py         # Unit tests (pytest)
```

---

## Interactive Menu

Simply run `direct` with no arguments in your terminal to open the interactive menu:

```
Available paths:
   1. autohotkey -> C:\Users\Khorn Victor\OneDrive\Documents\AutoHotkey
   2. camcycber  -> C:\Desktop\Student Online (SO)\Camcycber
   3. config     -> C:\Users\Khorn Victor\.config
   4. drive      -> C:\Desktop\Drive
   5. duck       -> C:\Desktop\Rubber Duck
   6. env        -> C:\Desktop\Student Online (SO)\Code
   7. etec       -> C:\xampp\htdocs\ETEC
   8. me         -> C:\Desktop\Me
   9. mock       -> C:\Desktop\Student Online (SO)\Mock Exam
  10. obsidian   -> C:\Desktop\Obsidean
  11. rdtc       -> C:\Desktop\Student Online (SO)\RDTC\aero-service
  12. stj        -> C:\Desktop\Student Online (SO)\Techno\other\STJ
  13. techno     -> C:\Desktop\Student Online (SO)\Techno\I3-GIC-A\Semester2
  14. tool       -> C:\Tool

Actions:
  [1-14] Select path | [a] Add | [u] Update | [d] Delete | [q] Quit

Choice> 
```

- **Select a path**: Enter `1`-`14` or shortcut name (e.g. `me`) to output the path.
- **Add**: Type `a` to add a new shortcut (defaults to current directory if path is omitted).
- **Update**: Type `u` and pick the number/name to update the destination directory.
- **Delete**: Type `d` and pick the number/name to remove a shortcut with confirmation.
- **Quit**: Type `q` or press Enter to exit.

---

## Terminal Commands (Direct CLI)

You can also run commands directly without opening the interactive menu:

| Operation | Command | Description |
|---|---|---|
| **Interactive Menu** | `direct` or `direct menu` | Open interactive CRUD menu |
| **Create** | `direct add <name> [path]` | Add a new shortcut (defaults to cwd if omitted) |
| **Set** | `direct set <name> [path]` | Create or overwrite a shortcut (defaults to cwd) |
| **Read (List)** | `direct ls` or `direct list` | Print static list without opening menu |
| **Read (Get)** | `direct <name>` | Output target path directly (for `cd` / navigation) |
| **Update** | `direct update <name> <path>` | Update an existing shortcut path |
| **Delete** | `direct rm <name>` | Remove a shortcut (`aliases: remove, del, delete`) |
| **Help** | `direct help` | Show usage commands and examples |

### CLI Examples

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

# 5. Jump to shortcut
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

---

## PowerShell Jump Integration

Add this function to your PowerShell `$PROFILE` (run `notepad $PROFILE`):

```powershell
function go($name) {
    if (-not $name) {
        $target = direct
        if ($LASTEXITCODE -eq 0 -and $target -and (Test-Path $target)) {
            Set-Location $target
        }
        return
    }
    $target = direct $name
    if ($LASTEXITCODE -eq 0 -and (Test-Path $target)) {
        Set-Location $target
    }
}
```

Now you can:
- Type `go` to open the interactive menu and select a path or manage your shortcuts.
- Type `go me` to jump immediately to `me`.

---

## Development & Testing

```powershell
uv run pytest
```
