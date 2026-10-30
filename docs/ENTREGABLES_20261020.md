# Entregables EP2 - 20 de octubre de 2026

Paquete para entrega: `entrega/TestFire_EP2_20261020.zip`. Incluye el proyecto y los documentos siguientes. No entregar el ZIP CLIENTE_PRIVADO: contiene credenciales para la conexion de trabajo.

| Entregable | Ubicacion dentro del proyecto |
|---|---|
| Informe tecnico PDF | docs/entrega/Informe_Tecnico_EP2.pdf |
| Fuente editable del informe | docs/INFORME_TECNICO_EP2.md |
| Presentacion editable, nueve diapositivas | docs/entrega/Presentacion_EP2.pptx |
| Presentacion PDF de respaldo | docs/entrega/Presentacion_EP2.pdf |
| Guion individual, unos 11 minutos previstos | docs/GUION_PRESENTACION.md |
| Robot principal editable y export oficial con hijos | rocketbot/MAIN_TESTFIRE_EP2/robot.db y EXPORT_TESTFIRE_EP2.db |
| Excel de referencia ejecutado en el host | output/076648bf-3612-42b9-b915-d14cd7982d57/Reporte_TestFire_20261018_084434_076648bf-3612-42b9-b915-d14cd7982d57.xlsx |
| Evidencia de la segunda PC y acuse del host | docs/VALIDACION_SEGUNDA_PC.md y docs/evidencias/segunda_pc_*.json |
| Guia completa, configuracion y ejecucion | GUIA_COMPLETA_PROYECTO.md y docs/CONFIGURACION_SEGUNDA_PC.md |
| Grabacion DOM, comandos generados y capturas | recorder/ y docs/evidencias/ |
| SQL preparado, pruebas y diagramas | database/, tests/ y docs/diagramas/ |

El ZIP conserva la estructura que necesita el robot: no entregar solo los .db si se espera ejecutarlo. Incluye dependencias puras dotenv/pytz con sus licencias; excluye entornos virtuales, .env, tokens de trabajo y el paquete privado del cliente. Para instalar en una PC nueva se debe configurar su propio .env.

Antes de subir: completar nombres de integrantes y expositor en el informe y la presentacion. No se inventaron nombres ni aportes personales. La presentacion PDF se genera en paralelo; no es un render exportado de PowerPoint.

Alcance acreditado: flujo web/Excel/API en el host y ejecucion desde segunda PC con acuse central comprobado. MySQL y aceptacion docente del grabador DOM alternativo siguen pendientes. No se acredita simultaneidad de ambos robots ni inspeccion directa del Excel de la segunda PC. La configuracion del punto de acceso del telefono queda pendiente de la nueva IP; la prueba acreditada fue en la red anterior.
