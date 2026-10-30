# Compartido por el preparador y el lanzador. No lee logs ni licencias.
function Resolve-RocketbotExecutable {
    param([string]$PreferredPath='', [switch]$ChooseIfMissing)
    if ($PreferredPath) {
        if (Test-Path -LiteralPath $PreferredPath -PathType Leaf) {
            return (Resolve-Path -LiteralPath $PreferredPath).Path
        }
        throw 'La ruta de Rocketbot indicada no existe.'
    }
    $Candidates=@()
    # La instalacion activa tiene prioridad sobre una ruta de una version antigua.
    foreach ($Process in @(Get-Process -Name 'rocketbot' -ErrorAction SilentlyContinue)) {
        try { if ($Process.Path) { $Candidates += $Process.Path } } catch { }
    }
    $Candidates += $env:ROCKETBOT_EXE
    $Candidates += [Environment]::GetEnvironmentVariable('ROCKETBOT_EXE','User')
    $Candidates += [Environment]::GetEnvironmentVariable('ROCKETBOT_EXE','Machine')
    $Command=Get-Command 'rocketbot.exe' -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($Command) { $Candidates += $Command.Source }
    if ($env:LOCALAPPDATA) {
        $Candidates += Join-Path $env:LOCALAPPDATA 'Programs\Rocketbot\2025.07.01\Rocketbot\rocketbot.exe'
    }
    foreach ($Candidate in $Candidates) {
        if ($Candidate -and (Test-Path -LiteralPath $Candidate -PathType Leaf)) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    if ($ChooseIfMissing) {
        Add-Type -AssemblyName System.Windows.Forms
        $Picker=New-Object System.Windows.Forms.OpenFileDialog
        try {
            $Picker.Title='Seleccionar rocketbot.exe instalado en ESTA PC'
            $Picker.Filter='Rocketbot (rocketbot.exe)|rocketbot.exe'
            $Picker.CheckFileExists=$true
            if ($Picker.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
                $Selected=$Picker.FileName
                if ([IO.Path]::GetFileName($Selected) -ine 'rocketbot.exe') { throw 'Seleccionar rocketbot.exe.' }
                [Environment]::SetEnvironmentVariable('ROCKETBOT_EXE',$Selected,'User')
                $env:ROCKETBOT_EXE=$Selected
                return $Selected
            }
        } finally { $Picker.Dispose() }
    }
    throw 'No se encontro Rocketbot. Abrirlo manualmente y reintentar, o configurar ROCKETBOT_EXE con su ruta completa.'
}
