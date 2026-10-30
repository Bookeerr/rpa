param([ValidateSet('setup','test','demo','api','api-demo','check','replay')][string]$Action='check', [string]$ExecutionId='')
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
$PythonExe=Join-Path $ProjectRoot '.venv-ep2\Scripts\python.exe'
Push-Location -LiteralPath $ProjectRoot
try {
    if ($Action -eq 'setup') {
        if (-not (Test-Path -LiteralPath $PythonExe)) { & python -m venv (Join-Path $ProjectRoot '.venv-ep2'); if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear venv' } }
        & $PythonExe -m pip install -r requirements-dev-ep2.txt
        if ($LASTEXITCODE -ne 0) { throw 'Fallo instalando dependencias' }
        & $PythonExe -m scripts.demo --create-data
    } elseif (-not (Test-Path -LiteralPath $PythonExe)) { throw 'Ejecutar primero -Action setup' }
    elseif ($Action -eq 'test') { & $PythonExe -m pytest tests -q --junitxml=docs/evidencias/pytest.xml }
    elseif ($Action -eq 'demo') { & $PythonExe -m scripts.demo }
    elseif ($Action -eq 'api') { & $PythonExe -m api.app }
    elseif ($Action -eq 'api-demo') { & $PythonExe -m scripts.api_demo }
    elseif ($Action -eq 'check') { & $PythonExe -m scripts.check_environment }
    elseif ($Action -eq 'replay') { & $PythonExe -m scripts.check_environment --replay $ExecutionId }
    if ($LASTEXITCODE -ne 0) { throw "La accion $Action fallo (codigo $LASTEXITCODE)" }
} finally { Pop-Location }
