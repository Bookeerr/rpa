param([string]$Robot='DEMO_LOCAL_EP2',[string]$RocketbotExe='')
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
$Database=Join-Path $ProjectRoot 'rocketbot\MAIN_TESTFIRE_EP2\robot.db'
if (-not (Test-Path -LiteralPath $Database -PathType Leaf)) { throw 'Falta la base del robot. Conservar la estructura completa del proyecto.' }
$IsReady=$false
try { $IsReady=(Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/' -TimeoutSec 3).StatusCode -eq 200 } catch { }
if (-not $IsReady) {
    . (Join-Path $PSScriptRoot 'rocketbot_path.ps1')
    $RocketbotExe=Resolve-RocketbotExecutable -PreferredPath $RocketbotExe -ChooseIfMissing
    Start-Process -FilePath $RocketbotExe -WorkingDirectory (Split-Path -Parent $RocketbotExe) -WindowStyle Hidden
    Write-Host 'Studio se esta iniciando. Si aparece la pregunta de drivers, responderla. Volver a abrir este lanzador cuando Studio este listo.'
    exit 0
}
$Encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Database))
Start-Process ('http://localhost:5000/editor/#/edit/'+[Uri]::EscapeDataString($Robot)+'/db/'+$Encoded)
