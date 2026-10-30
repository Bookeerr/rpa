$ErrorActionPreference='Stop'
$Identity=[Security.Principal.WindowsIdentity]::GetCurrent()
if (-not ([Security.Principal.WindowsPrincipal]$Identity).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Windows exige permisos de administrador. Clic derecho en HABILITAR_RED.bat > Ejecutar como administrador.'
}
$ProjectRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $ProjectRoot
try {
    $PythonExe=Join-Path $ProjectRoot '.venv-ep2\Scripts\python.exe'
    $Target=& $PythonExe -c 'import json; from auxiliaries.config import load_config; from scripts.network_services import service_target; print(json.dumps(service_target(load_config(require_secrets=False))))'
    if ($LASTEXITCODE -ne 0) { throw 'Configuracion de red invalida.' }
    $Role,$ServerIP,$Port=($Target | ConvertFrom-Json)
    if ($Role -ne 'server') { throw 'Esta regla solo corresponde a la PC servidor.' }
    $Address=Get-NetIPAddress -AddressFamily IPv4 -IPAddress $ServerIP -ErrorAction Stop
    $Profile=Get-NetConnectionProfile -InterfaceIndex $Address.InterfaceIndex
    if ($Profile.NetworkCategory -ne 'Private') { throw 'La conexion debe ser una red privada de confianza.' }
    $RuleName='TestFire-EP2-API-LAN'
    # Solo actualiza la regla propia; no modifica reglas de otras aplicaciones.
    $OldRule=Get-NetFirewallRule -Name $RuleName -ErrorAction SilentlyContinue
    if ($OldRule) { $OldRule | Remove-NetFirewallRule }
    New-NetFirewallRule -Name $RuleName -DisplayName 'TestFire EP2 API LAN' -Direction Inbound -Action Allow `
        -Protocol TCP -LocalPort $Port -LocalAddress $ServerIP -RemoteAddress LocalSubnet `
        -InterfaceAlias $Address.InterfaceAlias -Profile Private -EdgeTraversalPolicy Block | Out-Null
    $Evidence=Join-Path $ProjectRoot 'output\private\firewall_red.json'
    @{ rule=$RuleName; ip=$ServerIP; port=$Port; profile='Private'; remote='LocalSubnet'; applied_at=(Get-Date).ToString('o') } |
        ConvertTo-Json | Set-Content -LiteralPath $Evidence -Encoding UTF8
    Write-Host "Regla habilitada para $ServerIP`:$Port en la red privada."
} finally { Pop-Location }
