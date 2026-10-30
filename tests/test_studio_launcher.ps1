# Regresion del lanzador sin abrir ventanas ni ejecutar Rocketbot.
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
. (Join-Path $ProjectRoot 'scripts\rocketbot_path.ps1')
$TestFolder=Join-Path $ProjectRoot ('output\private\ruta prueba '+[Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $TestFolder -Force | Out-Null
$FakeExe=Join-Path $TestFolder 'rocketbot.exe'
Set-Content -LiteralPath $FakeExe -Value 'PRUEBA: este archivo nunca se ejecuta'
try {
    if ((Resolve-RocketbotExecutable -PreferredPath $FakeExe) -ne $FakeExe) { throw 'Ruta con espacios no resuelta' }
    function Get-Process { [pscustomobject]@{ Path=$FakeExe } }
    if ((Resolve-RocketbotExecutable) -ne $FakeExe) { throw 'No detecta la instalacion activa' }
    $Rejected=$false
    try { Resolve-RocketbotExecutable -PreferredPath (Join-Path $TestFolder 'ausente.exe') | Out-Null } catch { $Rejected=$true }
    if (-not $Rejected) { throw 'Se acepto una ruta inexistente' }
    function Invoke-WebRequest { [pscustomobject]@{ StatusCode=200 } }
    $OpenedUrls=New-Object 'System.Collections.Generic.List[string]'
    function Start-Process { param([string]$FilePath); $OpenedUrls.Add($FilePath) }
    & (Join-Path $ProjectRoot 'scripts\open_studio.ps1') -Robot MAIN_TESTFIRE_EP2 -RocketbotExe (Join-Path $TestFolder 'ausente.exe')
    if ($OpenedUrls.Count -ne 1 -or $OpenedUrls[0] -notlike 'http://localhost:5000/editor/#/edit/MAIN_TESTFIRE_EP2/db/*') {
        throw 'Studio abierto debe abrir el editor aunque la ruta de instalacion sea inexistente'
    }
    $Encoded=$OpenedUrls[0].Substring($OpenedUrls[0].IndexOf('/db/')+4)
    $Database=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Encoded))
    if ($Database -ne (Join-Path $ProjectRoot 'rocketbot\MAIN_TESTFIRE_EP2\robot.db')) { throw 'Base de datos equivocada' }
    Write-Output '5 comprobaciones PowerShell OK: ruta con espacios, proceso activo, ruta invalida, Studio abierto y base de datos.'
} finally {
    Remove-Item -LiteralPath $FakeExe -Force
    Remove-Item -LiteralPath $TestFolder
}
