$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $ProjectRoot
try {
    if (-not (Test-Path -LiteralPath '.env')) { throw 'Extraer el paquete PRIVADO del host, que contiene la configuracion del cliente.' }
    $PythonExe=Join-Path $ProjectRoot '.venv-ep2\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $PythonExe)) {
        if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 -m venv (Join-Path $ProjectRoot '.venv-ep2') }
        elseif (Get-Command python -ErrorAction SilentlyContinue) { & python -m venv (Join-Path $ProjectRoot '.venv-ep2') }
        else { throw 'Instalar Python 3.13 y volver a ejecutar este archivo.' }
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno. Instalar Python 3.13 y reintentar.' }
    }
    & $PythonExe -c "import sys; assert sys.version_info >= (3,11), 'Se requiere Python 3.11 o superior (probado con 3.13)'"
    if ($LASTEXITCODE -ne 0) { throw 'Version de Python incompatible.' }
    & $PythonExe -m pip install -r requirements-ep2.txt
    if ($LASTEXITCODE -ne 0) { throw 'Fallo instalando dependencias.' }
    & $PythonExe -m scripts.package_runtime_dependencies
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron preparar las dependencias portables de Rocketbot.' }
    & $PythonExe -c "from auxiliaries.config import load_config; assert load_config(require_secrets=False).get('API_ROLE') == 'client', 'Este preparador requiere la configuracion del cliente'"
    if ($LASTEXITCODE -ne 0) { throw 'Usar el paquete privado del cliente en la segunda PC.' }
    & $PythonExe -m scripts.start_local_services
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo conectar al servidor; revisar IP, token y firewall.' }
    . (Join-Path $PSScriptRoot 'rocketbot_path.ps1')
    $RocketbotExe=Resolve-RocketbotExecutable -ChooseIfMissing
    Write-Host 'Dependencias incluidas dentro del proyecto. Reiniciar Rocketbot si estaba abierto durante la preparacion.'
    Write-Host 'Cliente preparado. Abrir INICIAR_EP2.bat y ejecutar MAIN_TESTFIRE_EP2 en Studio.'
    Write-Host 'Los resumenes quedan en el servidor; el Excel de resultados queda en esta PC.'
} finally { Pop-Location }
