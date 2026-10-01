function direct {
    param([string]$name)

    $directScript = "C:\Tool\Direct\main.py"
    if (-not (Test-Path $directScript)) {
        Write-Host "❌ Script not found: $directScript" -ForegroundColor Yellow
        return
    }

    # If no argument: open interactive menu (List, Select, Add, Update, Remove)
    if ([string]::IsNullOrWhiteSpace($name)) {
        $jumpFile = "$env:TEMP\direct_jump.txt"
        $env:DIRECT_JUMP_FILE = $jumpFile
        python $directScript
        if (Test-Path -LiteralPath $jumpFile) {
            $target = (Get-Content -LiteralPath $jumpFile -Raw -ErrorAction SilentlyContinue)
            Remove-Item -LiteralPath $jumpFile -Force -ErrorAction SilentlyContinue
            if ($target) {
                $target = $target.Trim()
                if ($target -and (Test-Path -LiteralPath $target)) {
                    Set-Location -LiteralPath $target
                }
            }
        }
        Remove-Item Env:DIRECT_JUMP_FILE -ErrorAction SilentlyContinue
        return
    }

    # Shortcut jump: direct <name>
    $path = python $directScript $name
    $path = ($path | Select-Object -First 1).Trim()

    if ($LASTEXITCODE -eq 0 -and $path -and (Test-Path -LiteralPath $path)) {
        Set-Location -LiteralPath $path
    }
    else {
        Write-Host "❌ Invalid path name"
    }
}
