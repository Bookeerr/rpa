# Limpieza reversible de archivos ? 18/10/2026

La revision automatica rechazo el borrado directo con el mensaje general ?blocked by policy?, sin un motivo adicional. Se adopto una alternativa reversible: trasladar los archivos obsoletos y caches a `.limpieza_respaldo/20261018/`, conservando sus rutas relativas. No se ejecutaron borrados ni se libero espacio en disco.

Se apartaron **55 archivos**, **8,198,997 bytes** (7.82 MiB), de las carpetas de trabajo. El respaldo queda excluido del paquete de entrega y de Git.

| Ruta anterior | Motivo | Archivos | Bytes |
|---|---|---|---|
| `entrega/TestFire_EP2_AVANCE_20261017.zip` | Entrega anterior reemplazada por version vigente | 1 | 5984220 |
| `docs/entrega/Informe_Tecnico_EP2_AVANCE.pdf` | Entrega anterior reemplazada por version vigente | 1 | 1096170 |
| `docs/entrega/Presentacion_EP2_AVANCE.pdf` | Entrega anterior reemplazada por version vigente | 1 | 69095 |
| `docs/entrega/Presentacion_EP2_AVANCE.pptx` | Entrega anterior reemplazada por version vigente | 1 | 108649 |
| `scripts/studio_inspect.cjs` | Inspeccion desechable; formatos y export ya comprobados | 1 | 1049 |
| `scripts/studio_inspect_export.cjs` | Inspeccion desechable; formatos y export ya comprobados | 1 | 768 |
| `scripts/studio_inspect_form.cjs` | Inspeccion desechable; formatos y export ya comprobados | 1 | 1367 |
| `scripts/record_native_desktop.cjs` | Intento DesktopRecorder sin acciones capturadas; alternativa DOM conservada | 1 | 3003 |
| `recorder/desktop_controls.json` | Intento DesktopRecorder sin acciones capturadas; alternativa DOM conservada | 1 | 2 |
| `docs/evidencias/recorder_browser.png` | Intento DesktopRecorder sin acciones capturadas; alternativa DOM conservada | 1 | 100684 |
| `docs/evidencias/revision_pdf.png` | Vista de revision anterior reemplazada | 1 | 548340 |
| `.pytest_cache` | Cache regenerable | 4 | 3362 |
| `auxiliaries/__pycache__` | Cache regenerable | 12 | 66605 |
| `api/__pycache__` | Cache regenerable | 3 | 12925 |
| `scripts/__pycache__` | Cache regenerable | 14 | 70793 |
| `tests/__pycache__` | Cache regenerable | 11 | 131965 |

## Conservado

Se conservaron .env, .venv, .venv-ep2, .vscode, los originales EP1, las fuentes docentes extraidas, los archivos abiertos de consulta, los proyectos/export nativos y todas las corridas de output. No se retiraron los acuses de output/api_local/receipts.db ni los logs del servicio activo.

El intento fallido con DesktopRecorder respondio al inicio pero no registro acciones OS. Su export vacio, herramienta desechable y captura se trasladaron al respaldo. La captura DOM funcional, su export y el replay nativo permanecen en las carpetas activas.

## Recuperacion

Para recuperar un archivo, buscar su ruta relativa dentro de .limpieza_respaldo/20261018 y copiarlo a su ubicacion anterior. Comprobar primero si existe una version nueva en destino; no sobrescribirla sin revisar. Las caches no requieren restauracion: Python y pytest pueden generarlas nuevamente.

## Documentacion y paquete

GUIA_COMPLETA_PROYECTO.md describe la ejecucion y la responsabilidad de cada archivo. README la enlaza y package_delivery.py la incluye en el ZIP. Se actualizaron las referencias a las herramientas retiradas y la descripcion vigente de los robots.

El manifiesto estructurado del traslado esta en evidencias/limpieza_archivos.json. Las verificaciones de cierre se detallan debajo.

## Verificacion de cierre

- 45 pruebas existentes aprobadas en 14,07 segundos, sin generar caches nuevas.
- Enlaces locales de la guia, README y documentacion modificada comprobados.
- Sintaxis de los generadores modificados comprobada.
- Las 16 rutas trasladadas existen en el respaldo y quedaron fuera de las carpetas activas.
- ZIP reconstruido con la guia, registro de limpieza y evidencia vigente; CRC y hashes verificados.
- Auxiliares ejecutados desde el ZIP extraido en ruta con espacios y otro directorio de trabajo: cinco hojas Excel verificadas. Alcance local; no es una prueba de otra PC ni una nueva corrida web.

No se modifico el codigo funcional del robot ni los valores de .env en esta limpieza. El respaldo ocupa el mismo espacio que los archivos trasladados y no se incluye en el ZIP.
