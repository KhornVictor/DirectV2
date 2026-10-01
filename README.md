# Direct 🚀

A lightweight, fast directory navigation and shortcut bookmark manager for Windows and PowerShell terminals.

Jump instantly to any project directory, or launch an interactive terminal menu to browse, add, update, and remove paths.

---

## 📋 What is Direct?

Direct replaces long `cd` navigation paths with short, memorable aliases.

- **Instant Directory Jump**: Type `direct <name>` (e.g., `direct me`, `direct tool`) to jump directly to any configured folder.
- **Interactive Terminal Menu**: Type `direct` with no arguments to view all bookmarks with options to:
  - Jump to a path by number or name
  - **Add** a new path shortcut (defaults to your current directory if omitted)
  - **Update** existing destination folders
  - **Remove** shortcuts
- **TOML Configuration**: All shortcuts are automatically synchronized with [`path.toml`](path.toml).
- **PowerShell Tab Completion**: Type `direct` and press `Tab` to auto-complete configured shortcut names.
- **Zero Overhead**: Direct Python execution ensures sub-second jumps.

---

## ⚙️ Requirements

Before installing, ensure you have:

- **Operating System**: Windows 10 or Windows 11
- **Shell**: PowerShell 5.1 (Built-in Windows PowerShell) or PowerShell 7+ (pwsh)
- **Python**: Python 3.11 or higher ([python.org](https://www.python.org)) added to your `PATH`
- **Git**: Git for Windows ([git-scm.com](https://git-scm.com)) added to your `PATH`

---

## 📥 Installation

### Option 1: Quick Install (Recommended)

Run the following command in PowerShell:

```powershell
irm https://raw.githubusercontent.com/KhornVictor/Direct/main/install.ps1 | iex
```

This clones the repository into `C:\Tool\Direct` and sets up the Python virtual environment.

---

### Option 2: Manual Clone

```powershell
# 1. Create target directory and clone
git clone https://github.com/KhornVictor/Direct.git C:\Tool\Direct

# 2. Setup Python environment
python -m venv C:\Tool\Direct\.venv
```

---

## 🔧 Configure Your PowerShell Profile

To make the `direct` command available in all your terminal sessions, add the profile loader to your `$PROFILE`:

1. Open your PowerShell profile in Notepad:

   ```powershell
   notepad $PROFILE
   ```

2. Paste this block at the end of the file:

   ```powershell
   # --- Direct: Directory Navigation & Bookmark Manager ---
   if (Test-Path "C:\Tool\Direct\profile.ps1") {
       . "C:\Tool\Direct\profile.ps1"
   }
   ```

3. Save the file and reload your profile:

   ```powershell
   . $PROFILE
   ```

---

## 💻 Usage

### 1. Interactive Menu

Run `direct` without arguments:

```powershell
direct
```

Output:

```text
Available paths:
   1. config     -> C:\Users\User\.config
   2. me         -> C:\Desktop\Me
   3. projects   -> C:\Desktop\Projects
   4. tool       -> C:\Tool

Actions:
  [1-4] Select path | [a] Add | [u] Update | [d] Delete | [q] Quit

Choice> 
```

- **Select path**: Type the number (e.g. `2`) or name (`me`) and press Enter to navigate to that directory.
- **`a` (Add)**: Prompts for shortcut name and target path (press Enter to bookmark your current folder).
- **`u` (Update)**: Select an existing shortcut to change its destination path.
- **`d` (Delete)**: Select a shortcut to remove it (with confirmation).
- **`q` (Quit)**: Exit the menu without changing directory.

---

### 2. Direct Jump

Jump directly to any bookmarked path by name:

```powershell
direct me
direct tool
direct projects
```

---

### 3. Tab Completion

Type `direct` followed by the first letter of a shortcut and press `Tab`:

```powershell
direct m<Tab>    # Autocompletes to 'direct me'
```

---

## 📁 Configuration File (`path.toml`)

All shortcuts are stored in [`path.toml`](path.toml). You can edit them via the interactive menu or directly in the file:

```toml
[paths]
config = 'C:\Users\User\.config'
me = 'C:\Desktop\Me'
tool = 'C:\Tool'
```

---

## 📄 License

This project is licensed under the [MIT License](license) - free for everyone to use, modify, and distribute.
