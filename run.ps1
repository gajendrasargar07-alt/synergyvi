param(
    [switch]$Setup,
    [switch]$Train,
    [switch]$SkipQuantum,
    [switch]$Test
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$pythonPath = Join-Path $venvPath "Scripts\\python.exe"

if ($Setup -or -not (Test-Path $pythonPath)) {
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if (-not $launcher) {
        throw "Python 3.11+ is required. Install it from python.org, then run .\\run.ps1 -Setup."
    }
    & py -3 -m venv $venvPath
    & $pythonPath -m pip install --upgrade pip
    & $pythonPath -m pip install -r (Join-Path $projectRoot "requirements.txt")
}

if ($Train) {
    $trainArgs = @("-m", "integration.pipeline")
    if ($SkipQuantum) { $trainArgs += "--skip-quantum" }
    & $pythonPath @trainArgs
}

if ($Test) {
    & $pythonPath -m pytest tests -q
}

if (-not $Train -and -not $Test) {
    & $pythonPath -m streamlit run (Join-Path $projectRoot "dashboard\\app.py")
}
