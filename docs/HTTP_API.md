# Contrato de API propia

Implementado en `api/app.py`, Flask. No pertenece a TestFire. Ejecucion: `ejecutar_ep2.bat -Action api`. Requiere token configurado y MySQL con esquema. Solo escucha loopback por defecto; LAN se habilita explicitamente en host.

Todos los endpoints requieren `Authorization: Bearer <API_TOKEN>`; no guardar valor en evidencia. POST usa Content-Type application/json. Maximo 16 KiB. Error de almacenamiento -> 503 sin detalles secretos.

| Metodo/ruta | Respuesta |
|---|---|
| GET /health | 200 `{status:ok,storage:mysql}` tras SELECT real; 503 si falla |
| POST /executions | 201 nuevo; 200 mismo UUID y mismo JSON; 409 mismo UUID con distinto JSON; 400 campos invalidos |
| GET /executions/{execution_id} | 200 resumen persistido; 404 ausente; 400 UUID invalido |

Campos exactos POST: execution_id UUID, equipo texto, estado_proceso `CONCILIACION_COMPLETADA`, movimientos_validos entero >=0, movimientos_rechazados entero >=0, discrepancias entero >=0, duracion_hasta_envio_ms entero >=0. Se rechazan booleanos como conteos. El hash se calcula del JSON canonico. PK + recuperacion de clave duplicada protege concurrencia.

En Studio: congelar payload una vez, GET health, POST, GET id; validar estado **y** estructura. Comparar todo el GET final con el payload congelado. `auxiliaries/http_client.py` hace una sola peticion, timeout configurable, sin redirects, y escribe request/response redactados y evento por intento. IF/While del robot decide reintentar solo conexion/timeout/502/503/504, maximo 1+MAX_RETRIES (3 por defecto). No reintentar 400/401/404/409/500 automaticamente. El POST repetido lleva el mismo UUID y payload, nunca vuelve a calcular duracion para un reintento.

Pruebas `tests/test_api.py`: HTTP real por loopback con almacen **en memoria de prueba**, POST duplicado/concurrente, 401/400/404/409/500 y timeout. Pruebas del cliente inyectan tambien no JSON y conexion rechazada. No acreditan persistencia MySQL.

Adicionalmente, DEMO_LOCAL_EP2 coordino GET/POST/GET y POST repetido desde comandos reales de Rocketbot: estados 200/201/200/200; ver DEMO_NATIVA_ROCKETBOT.md. Para repetir sin SQL, `ejecutar_ep2.bat -Action api-demo` inicia exclusivamente memoria en 127.0.0.1:18080 con identificador de demo publico. No se activa por fallo de MySQL ni reemplaza `-Action api`. Es efimera y no debe usarse para datos reales.

GET consulta; POST crea/acuse; PUT reemplazaria un recurso completo; PATCH modificaria parte; DELETE eliminaria. Los tres ultimos no se implementan porque el alcance no los necesita. El resumen pre-cierre es inmutable; para publicar cierre definitivo se requeriria otro contrato idempotente, no se reutiliza el POST con payload diferente.

API HTTP sin TLS restringida a laboratorio privado. Para salir de esa red se requiere terminacion HTTPS. No se habilito exposicion publica ni firewall amplio.
