param(
    [ValidateSet("compile", "lint")]
    [string]$Mode = "compile"
)

$ErrorActionPreference = "Stop"

$RenpyExe = "C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe"
$ProjectRoot = "C:\Users\blank\Documents\RenPy_Projects\Tractir"

if (-not (Test-Path -LiteralPath $RenpyExe)) {
    throw "Ren'Py executable not found: $RenpyExe"
}

if (-not (Test-Path -LiteralPath $ProjectRoot)) {
    throw "Project root not found: $ProjectRoot"
}

Push-Location -LiteralPath $ProjectRoot
try {
    & $RenpyExe . $Mode
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
