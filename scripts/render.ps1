param(
    [ValidateSet('all', 'html', 'epub')]
    [string]$Format = 'all',
    [switch]$Preview
)
$ErrorActionPreference = 'Stop'
$bookRoot = Split-Path -Parent $PSScriptRoot
$portableQuarto = Join-Path $bookRoot '.tools/bin/quarto.exe'
if (Test-Path -LiteralPath $portableQuarto) {
    $quartoExe = $portableQuarto
} else {
    $quartoCommand = Get-Command quarto -ErrorAction SilentlyContinue
    if (-not $quartoCommand) {
        throw 'Install Quarto from https://quarto.org/docs/get-started/ or supply .tools/bin/quarto.exe.'
    }
    $quartoExe = $quartoCommand.Source
}
Push-Location $bookRoot
try {
    if ($Preview) {
        & $quartoExe preview
        if ($LASTEXITCODE -ne 0) { throw 'Quarto preview failed.' }
    } else {
        & $quartoExe render --to $Format --no-clean
        if ($LASTEXITCODE -ne 0) { throw "Quarto $Format render failed." }
    }
} finally {
    Pop-Location
}
