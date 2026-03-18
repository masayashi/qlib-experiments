param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    & $Python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt

Write-Host "Environment ready."
