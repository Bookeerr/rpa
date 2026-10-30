> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.

# Revision de entregables · 2026-10-17

Informe final de avance: **10 paginas** (cuerpo A4 y anexos vectoriales ampliados). Presentacion: **8 diapositivas** en PPTX y PDF paralelo. Los diagramas se mantienen editables en Mermaid y exportados a SVG, PDF y PNG.

## Revision realizada

- Se abrieron las vistas renderizadas de todas las paginas y diapositivas; se revisaron ademas arquitectura, modelo SQL, demo nativa y resumen de exposicion a mayor escala.
- Se detectaron etiquetas demasiado pequeñas al encajar diagramas completos en A4. El informe ahora conserva los anexos en paginas ampliadas, con texto de diagrama escalado a un minimo de 10 puntos; los pies usan 9 puntos. Usar vista al ancho para los diagramas verticales y archivos individuales para imprimir.
- Se detectaron recortes en el PDF inicial generado por Mermaid CLI. Se corrigio la exportacion usando el viewBox natural del SVG en Chromium; el informe conserva la pagina completa para no recortar recuadros/sombras. Se volvieron a revisar los limites, incluidos TestFire y MySQL en arquitectura.
- El resumen de la presentacion se redujo a cuatro etapas legibles. El detalle de decisiones, ciclos y fallos permanece en el flujo completo y los anexos.
- No hay paginas vacias ni texto fuera de los limites del PDF. El PPTX tiene ocho diapositivas, notas del expositor y formas dentro del lienzo. Resultados estructurados en `docs/evidencias/revision_documentos.json`.
- El ER contiene las ocho tablas reales y cinco FKs desde executions. No conecta ficticiamente account_rules o api_receipts con ejecuciones.
- Se descomprimio el ZIP en una carpeta temporal con espacios y se ejecuto la demo de auxiliares desde otro directorio: genero Excel de cinco hojas y las cuatro clasificaciones esperadas. Evidencia en `docs/evidencias/portabilidad_paquete.json`. Se incorporo luego esa acta al paquete, sin cambiar el codigo probado. CRC y hashes se verifican de nuevo al empaquetar.

## Alcance de esta comprobacion

El PDF de presentacion se genera del mismo contenido fuente que el PPTX. **No es una exportacion de PowerPoint.** El renderizado del PPTX dentro de PowerPoint/LibreOffice y el ensayo oral siguen pendientes; no se atribuye esa verificacion a python-pptx. El Excel se abrio con openpyxl y se verificaron cinco hojas, tipos y ausencia de formulas; apertura en Excel de escritorio pendiente.

Las capturas y respuestas de Studio pertenecen a DEMO_LOCAL_EP2, con datos sinteticos. No acreditan recorder, login web ni MySQL. La evidencia nativa y su alcance se detallan por separado.

## Reproducir

1. `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/render_diagrams.ps1`.
2. `.venv-ep2/Scripts/python.exe -m scripts.build_documents`.
3. `.venv-ep2/Scripts/python.exe -m scripts.review_documents` y revisar las imagenes en `docs/evidencias/revision/`.
4. `.venv-ep2/Scripts/python.exe -m scripts.package_delivery` para reconstruir el ZIP y verificar CRC/SHA-256.

La imagen `docs/evidencias/revision_pdf.png` se conserva solo como revision historica inicial y no se incluye en el paquete final. La revision vigente usa la carpeta `revision/` y el JSON anterior.
