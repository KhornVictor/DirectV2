$script:DirectRoot = "C:\Tool\Direct"
$script:DirectPy   = Join-Path $script:DirectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $script:DirectPy)) {
    $script:DirectPy = "python.exe"
}
$script:DirectMain = Join-Path $script:DirectRoot "main.py"
$script:DirectToml = Join-Path $script:DirectRoot "path.toml"

function direct {
    <#
    .SYNOPSIS
        Directory navigation, shortcut manager, and jumper.
    #>
    [CmdletBinding()]
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    if (-not (Test-Path $script:DirectMain)) {
        Write-Host "ERROR: Direct entrypoint not found at: $script:DirectMain" -ForegroundColor Red
        return
    }

    # Temporary file used for cross-process directory jump communication
    $tempFile = [System.IO.Path]::GetTempFileName()

    try {
        $env:DIRECT_JUMP_FILE = $tempFile

        if ($Arguments -and $Arguments.Count -gt 0) {
            & $script:DirectPy $script:DirectMain @Arguments
        } else {
            & $script:DirectPy $script:DirectMain
        }

        # If python wrote a target path to the jump file, change location
        if (Test-Path -LiteralPath $tempFile) {
            $targetPath = Get-Content -LiteralPath $tempFile -Raw -ErrorAction SilentlyContinue
            if ($targetPath) {
                $targetPath = $targetPath.Trim()
                if ($targetPath -and (Test-Path -LiteralPath $targetPath)) {
                    Set-Location -LiteralPath $targetPath
                }
            }
        }
    }
    finally {
        # Always clean up temp file and environment variable
        Remove-Item -LiteralPath $tempFile -Force -ErrorAction SilentlyContinue
        Remove-Item Env:DIRECT_JUMP_FILE -ErrorAction SilentlyContinue
    }
}

# --- Aliases ---
Set-Alias -Name d  -Value direct -Description "Shortcut for direct" -Scope Global -ErrorAction SilentlyContinue
Set-Alias -Name go -Value direct -Description "Shortcut for direct" -Scope Global -ErrorAction SilentlyContinue

# --- Tab Completion ---
Register-ArgumentCompleter -CommandName @('direct', 'go', 'd') -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

    $subcommands = @('add', 'set', 'update', 'rm', 'remove', 'del', 'delete', 'ls', 'list', 'menu', 'help')

    # Parse shortcut keys from path.toml fast without spawning Python
    $shortcuts = @()
    if (Test-Path -LiteralPath $script:DirectToml) {
        $shortcuts = Get-Content -LiteralPath $script:DirectToml |
            Where-Object { $_ -match '^\s*([a-zA-Z0-9_\-]+)\s*=' } |
            ForEach-Object { $matches[1] }
    }

    $tokens = $commandAst.Tokens
    if ($tokens.Count -le 2) {
        # Completing first argument: suggest shortcuts and subcommands
        @($shortcuts + $subcommands) |
            Where-Object { $_ -like "$wordToComplete*" } |
            ForEach-Object {
                [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
            }
    }
    elseif ($tokens.Count -eq 3 -and $tokens[1].Value -in @('rm', 'remove', 'del', 'delete', 'update', 'set')) {
        # Completing second argument: suggest existing shortcuts
        $shortcuts |
            Where-Object { $_ -like "$wordToComplete*" } |
            ForEach-Object {
                [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
            }
    }
}

# --- Profile Installer Helper ---
function Install-DirectProfile {
    <#
    .SYNOPSIS
        Automatically adds Direct to your PowerShell $PROFILE.
    #>
    [CmdletBinding()]
    param()

    $profilePath = $PROFILE
    $profileDir  = Split-Path -Parent $profilePath

    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    if (-not (Test-Path $profilePath)) {
        New-Item -ItemType File -Path $profilePath -Force | Out-Null
    }

    $profileContent = Get-Content -LiteralPath $profilePath -Raw -ErrorAction SilentlyContinue
    $loaderLine = ". `"$script:DirectRoot\profile.ps1`""

    if ($profileContent -match [regex]::Escape($loaderLine)) {
        Write-Host "Direct is already configured in your profile: $profilePath" -ForegroundColor Yellow
        return
    }

    $addition = @"

# --- Direct: Directory Navigation & Bookmark Manager ---
if (Test-Path "$script:DirectRoot\profile.ps1") {
    . "$script:DirectRoot\profile.ps1"
}
"@
    Add-Content -LiteralPath $profilePath -Value $addition
    Write-Host "SUCCESS: Added Direct integration to $profilePath" -ForegroundColor Green
    Write-Host "Restart your terminal or run: . `$PROFILE" -ForegroundColor Cyan
}
