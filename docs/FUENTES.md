# Fuentes y limites de evidencia

Consulta: 2026-10-16 (America/Santiago).

## Documentos locales leidos

| Fuente | Uso y limite |
|---|---|
| PROMPT_CODEX_ROCKETBOT_TESTFIRE_EP2.md proporcionado | Especificacion solicitada; IL 2.1 a IL 2.5, alcance Rocketbot, 40%, fecha 20/10/2026 y exposicion 10–12 min. No reemplaza verificacion de pauta original. |
| CASO2-Demo TestFire.docx | Caso y opciones. Credenciales/selectores son ejemplos, no evidencia actual. Texto extraido en fuentes_extraidas/fuente_3.txt. |
| Evaluacion_Parcial_I_ATY1102_Encargo_estudiante.pdf | EP1, Selenium, control/ciclos, documentacion; fuente_2.txt. |
| PDD_TestFire.docx e Informe_Tecnico_TestFire.docx existentes | Antecedente real EP1; codigo y logs historicos inspeccionados; fuentes 4 y 5. |
| 1. EP2_Instrucciones y Pauta_Presentacion_Estudiante_2025.pdf en Descargas | **DESCARTADO como pauta RPA:** contenido AVY1103 Deep Learning. Fuente_1.txt conserva la evidencia de identificacion. |
| Instrucciones y Pauta Evaluacion parcial 2_Estudiante_2025.docx | **RECIBIDO Y LEIDO** durante la sesion. Texto: fuentes_extraidas/pauta_ep2.txt; confirma indicadores, 40%, 20/80 y 10–12 minutos especificos. |

La pauta EP2 original contiene 15 minutos/equipos de tres en texto general y 10–12 minutos individuales en instrucciones especificas. Se prepara 11 minutos; no se atribuye una aclaracion adicional al docente. La EP1 disponible tambien contiene referencia general a 15 minutos/equipos de tres.

## Rocketbot oficial

| Fuente | Verificacion |
|---|---|
| https://www.rocketbot.com/suite-rocketbot.html | Descargas Windows y hashes publicados. 2026.04.07 descargado: MD5 distinto; no ejecutado. 2025.07.01: hash coincidente; instalado. |
| https://docs.rocketbot.com/2018/09/09/abrir-rocketbot-studio/ | Inicio mediante ejecutable, sin flags inventados. |
| https://docs.rocketbot.com/2024/01/26/como-exportar-un-robot/ | Exportar desde padre; incluir modulos; no marcar produccion para conservar edicion. JSON individual no incluye proyecto completo. |
| https://docs.rocketbot.com/category/manual/web/ | Catalogo web. |
| https://docs.rocketbot.com/category/manual/webscraping/ | Esperar, texto, click, extraer tabla. |
| https://docs.rocketbot.com/2019/05/06/esperar-por-objeto/ | Retorna booleano; accion visible/presente/clickeable; tiempo maximo. |
| https://docs.rocketbot.com/2019/02/20/extraer-tabla/ | Tabla a array; comprobar codificacion/tipo antes de recorrer. |
| https://docs.rocketbot.com/2019/05/13/for/ | Iterable y variable por iteracion. |
| https://docs.rocketbot.com/2023/12/20/try-catch/ | Bloques de excepciones. |
| https://docs.rocketbot.com/2023/12/07/ejecutar-python/ | Python auxiliar y SetVar; comprobar entorno real antes de cargar librerias. |
| https://docs.rocketbot.com/2019/05/13/ejecuta-otro-script-rocketbot/ | Llamada a hijos y herencia; no duplicar variables del padre en hijos. |
| https://forum.rocketbot.com/question/execute-python/ | GetVar/SetVar, respuesta en foro del proveedor; complementar con catalogo instalado y prueba de humo. |
| https://market.rocketbot.com/module/RocketbotRecorder(Chrome) | Version publicada 4.0.3; no equivale a compatibilidad Chrome actual. |
| https://market.rocketbot.com/module/DesktopRecorder | Version publicada 2.1; alternativa por probar. |
| https://license.rocketbot.com/ | Activacion personal; no se solicito una licencia con datos inventados. |

Se usa ademas el catalogo `languages/command_list_tree_es.json` y `package.json` de la distribucion realmente instalada para registrar nombres/versiones. No se fabricaron archivos `.db` ni JSON supuestamente importables.

Fuentes oficiales adicionales consultadas el 2026-10-16: https://docs.rocketbot.com/category/suite/studio/?print=print-search (variables internas `%project_path%`, `%db_path%`, estructura nativa); https://docs.rocketbot.com/2023/06/29/como-actualizar-a-rocketbot-2023/ (ubicacion modules/libs; los detalles de Python de esa guia historica no sustituyen el runtime 3.13.5 medido). Plantillas actuales obtenidas de formularios reales y guardado por /addbot; captura, respuestas y DB real disponibles. Revision documental 2026-10-17.
