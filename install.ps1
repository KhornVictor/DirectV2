<#
.SYNOPSIS
    Direct Installer - Lightweight Directory Navigation & Bookmark Manager
.DESCRIPTION
    Installs Direct by cloning the repository to C:\Tool\Direct and setting up the Python environment.
    Designed to be run directly or via Invoke-RestMethod:
        irm https://raw.githubusercontent.com/KhornVictor/DirectV2/main/install.ps1 | iex
#>

[CmdletBinding()]
param(
    [string]$InstallDir = "C:\Tool\Direct",
    [string]$RepoUrl    = "https://github.com/KhornVictor/DirectV2.git"
)

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 Installing Direct..." -ForegroundColor Cyan

# 1. Prerequisite checks
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Git is not installed or not in PATH. Please install Git first: https://git-scm.com" -ForegroundColor Red
    return
}

$pythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) {
    "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    "py"
} else {
    $null
}

if (-not $pythonCmd) {
    Write-Host "❌ Error: Python 3.11+ is not installed or not in PATH. Please install Python first: https://www.python.org" -ForegroundColor Red
    return
}

# 2. Prepare destination directory and clone repository
$parentDir = Split-Path -Parent $InstallDir
if (-not (Test-Path $parentDir)) {
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
}

if (Test-Path "$InstallDir\.git") {
    Write-Host "ℹ️  Direct repository already exists at $InstallDir. Updating..." -ForegroundColor Yellow
    try {
        git -C $InstallDir pull origin main
    } catch {
        Write-Host "⚠️ Warning: Failed to pull latest changes from remote. Using existing files." -ForegroundColor Yellow
    }
} elseif (Test-Path $InstallDir) {
    Write-Host "ℹ️  Target folder $InstallDir already exists." -ForegroundColor Yellow
} else {
    Write-Host "📦 Cloning Direct repository into $InstallDir..." -ForegroundColor Cyan
    git clone $RepoUrl $InstallDir
}

# 3. Setup Python virtual environment
Write-Host "🐍 Setting up Python environment..." -ForegroundColor Cyan
$venvPath = Join-Path $InstallDir ".venv"
if (-not (Test-Path $venvPath)) {
    & $pythonCmd -m venv $venvPath
    Write-Host "✓ Virtual environment created at $venvPath" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists at $venvPath" -ForegroundColor Green
}

# 4. Display profile configuration instructions (User adds it themselves)
Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "🎉 Direct has been installed successfully at: $InstallDir" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green

Write-Host "📌 NEXT STEP: Add Direct to your PowerShell profile:" -ForegroundColor Yellow
Write-Host "1. Open your profile in Notepad by running:" -ForegroundColor White
Write-Host "   notepad `$PROFILE`n" -ForegroundColor Cyan

Write-Host "2. Paste the following lines into your profile:" -ForegroundColor White
$profileSnippet = @"
# --- Direct: Directory Navigation & Bookmark Manager ---
if (Test-Path "$InstallDir\profile.ps1") {
    . "$InstallDir\profile.ps1"
}
"@
Write-Host $profileSnippet -ForegroundColor Magenta

Write-Host "`n3. Save the file and reload your terminal session by running:" -ForegroundColor White
Write-Host "   . `$PROFILE`n" -ForegroundColor Cyan

Write-Host "💡 Usage:" -ForegroundColor Yellow
Write-Host "   direct        # Open interactive menu (List, Jump, Add, Update, Remove)" -ForegroundColor White
Write-Host "   direct <name> # Jump directly to bookmark (e.g. direct me)`n" -ForegroundColor White
