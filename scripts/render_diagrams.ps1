param([string[]]$Names=@())
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $ProjectRoot
try {
    & (Join-Path $ProjectRoot '.venv-ep2\Scripts\python.exe') -m scripts.generate_er
    if ($LASTEXITCODE -ne 0) { throw 'Fallo generacion ER' }
    foreach ($Source in Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'docs\diagramas') -Filter '*.mmd') {
        if ($Names.Count -gt 0 -and $Source.BaseName -notin $Names) { continue }
        foreach ($Extension in @('svg','png')) {
            $Target=[System.IO.Path]::ChangeExtension($Source.FullName,$Extension)
            & npm.cmd exec --yes --package @mermaid-js/mermaid-cli@12.0.0 -- mmdc -i $Source.FullName -o $Target -b white --size 1800
            if ($LASTEXITCODE -ne 0) { throw "Fallo render $($Source.Name)" }
        }
    }
    $env:PUPPETEER_MODULE=(Get-ChildItem -LiteralPath (Join-Path $env:LOCALAPPDATA 'npm-cache\_npx') -Filter 'puppeteer' -Directory -Recurse -Depth 3 | Select-Object -First 1 -ExpandProperty FullName)
    & node (Join-Path $PSScriptRoot 'render_diagram_pdfs.cjs')
    if ($LASTEXITCODE -ne 0) { throw 'Fallo export PDF vectorial' }
} finally { Pop-Location }
