# Recorder real y limite de aceptacion

Grabador DOM propio EP2 v1: fuente recorder/dom_recorder.js; lanzador scripts/record_dom.cjs. Captura eventos change/click isTrusted del navegador. El lanzador conduce la sesion; el recorder independiente escucha y exporta lo ocurrido. No es una lista de comandos escrita manualmente ni una grabacion de video.

Export original: recorder/dom_recording.json. Export ajustado nativo: recorder/native_recorded_commands.json. Ajustes: variables para usuario/clave desde captura; esperas por objeto agregadas en MAIN; XPath con atributos y comillas dobles. Los cuatro comandos exportados se usan realmente en el proyecto nativo. Evidencia de replay: studio_web_responses.json, captura studio_web.png y web_nativa_resumen.json.

Compatibilidad oficial: DesktopRecorder 2.1 inicio pero no capturo eventos OS en la sesion; el export vacio y la herramienta desechable se retiraron en la limpieza documentada en LIMPIEZA_ARCHIVOS.md. RocketbotRecorder Chrome 4.0.3 publicado en Market, descarga Web Store sin paquete disponible. No se afirma compatibilidad exitosa de esas opciones.

PENDIENTE: aceptacion por el docente del grabador alternativo, segun apartado 8 del prompt. El flujo real funciona; esta aceptacion academica no puede decidirla el robot.

Regrabar: configurar .env; establecer PUPPETEER_MODULE a Puppeteer instalado; ejecutar node scripts/record_dom.cjs y python scripts/build_native_web.py con Studio abierto. Ejecutar MAIN en Studio para verificar replay. No reemplazar esta evidencia con un video de pantalla.
