> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.

# Entorno comprobado el 2026-10-16

Windows, Python externo 3.13.14 en `.venv-ep2`; runtime real de Rocketbot 3.13.5 (64 bits), obtenido al ejecutar un comando en Studio. Son entornos distintos. MySQL84 estaba Running, cliente 8.4.9; autenticacion y despliegue de `testfire_rpa` PENDIENTES por decision expresa del usuario. Firefox 157.0.1, Chrome 155.0.8059.82, Edge 155.0.4283.45.

Rocketbot 2025.07.01 se instalo en `%LOCALAPPDATA%/Programs/Rocketbot/2025.07.01/Rocketbot`. Esta ruta externa se descubre por equipo y puede reemplazarse con ROCKETBOT_EXE. Se creo el acceso directo de escritorio Rocketbot Studio EP2. El manifiesto identifica build `2025.07.01_qa`. Servicios: web 1.7.4, logic 1.5.0, scripts 1.9.0, system 1.4.0.

## Descarga e integridad

ZIP oficial 2025.07.01: MD5 calculado y publicado `9f0e2c18051b020d71387821f3abdf82`, coincidentes. La descarga 2026.04.07 tenia MD5 calculado `a4566ce454457fedc5dcfe21b3c5d2ab`, distinto al publicado `153fd4432f30564ecd16b146dcfaac31`; no se ejecuto. Los ZIP permanecen fuera del proyecto. MD5 se uso para cotejar el dato publicado, no como firma digital.

## Studio y dependencias

Se verificaron HTTP 200 en localhost:5000, editor y ejecucion real de Python. El endpoint de licencia informo licencia activa de desarrollo hasta 2026-11-15, una ejecucion simultanea. No se incluye token, serial ni licencia en la entrega. No se comprobo runner de produccion.

Durante el reinicio, Studio quedo esperando el dialogo `Update browser drivers`. Se selecciono No a la actualizacion opcional; luego volvio a escuchar en 127.0.0.1:5000. Un proceso vivo sin ese puerto no acredita que Studio este listo. Se observo tambien un error WNDPROC de notificacion; no impidio abrir el editor despues de responder el dialogo.

El humo real encontro openpyxl, pymysql, requests y tzdata; faltaba dotenv. Se instalo python-dotenv 1.2.4 en la ubicacion soportada `_internal/modules/libs`. El runtime congelado carece de `zoneinfo`; se agrego un adaptador con pytz y se actualizo solo ese paquete puro a 2026.5. No se copio el site-packages completo del entorno externo. Para otra PC, repetir importaciones y ejecucion sintetica; no basta la version declarada.

## Limites actualizados al 18/10/2026

HTTPS TestFire sigue fallando por certificado. Se ejecuto el sitio HTTP exclusivamente con su cuenta publica de demostracion; Chrome y comandos web nativos funcionaron. Firefox fallo por una ruta Documents resuelta incorrectamente por el modulo instalado. Grabador DOM propio y export oficial padre/hijos ejecutados; aceptacion docente de recorder alternativo y segunda PC pendientes. API local SQLite en loopback 18081, MySQL sin credenciales por instruccion del usuario. Detalle vigente en ESTADO_ACTUAL.md y NATIVO_MAIN_VERIFICADO.md.
