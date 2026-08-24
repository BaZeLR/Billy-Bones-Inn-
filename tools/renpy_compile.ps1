param(
    [ValidateSet("compile", "lint")]
    [string]$Mode = "compile"
)

$ErrorActionPreference = "Stop"

$RenpySdk = "C:\Users\blank\renpy\renpy-8.5.2-sdk"
$RenpyPython = Join-Path $RenpySdk "lib\py3-windows-x86_64\python.exe"
$RenpyScript = Join-Path $RenpySdk "renpy.py"
$ProjectRoot = "C:\Users\blank\Documents\RenPy_Projects\Tractir"

if (-not (Test-Path -LiteralPath $RenpyPython)) {
    throw "Ren'Py Python runtime not found: $RenpyPython"
}

if (-not (Test-Path -LiteralPath $RenpyScript)) {
    throw "Ren'Py launcher script not found: $RenpyScript"
}

if (-not (Test-Path -LiteralPath $ProjectRoot)) {
    throw "Project root not found: $ProjectRoot"
}

Push-Location -LiteralPath $ProjectRoot
try {
    & $RenpyPython $RenpyScript . $Mode
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
