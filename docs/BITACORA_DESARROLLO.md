# Bitacora de desarrollo

Evidencia inicial 2026-10-16; consolidacion documental 2026-10-17. No confundir con los logs de ejecucion del robot. Inicio/fin por tarea no instrumentados salvo evidencia indicada; duracion **NO_MEDIDO** donde no existe medicion. No se inventan minutos retrospectivos.

| Tarea | Inicio / fin | Duracion | Archivos / validacion | Resultado / pendientes |
|---|---|---|---|---|
| Leer prompt, caso, EP1 y proyecto | 2026-10-16 / 2026-10-16 | NO_MEDIDO | fuentes_extraidas, codigo/logs existentes | PDF llamado EP2 corresponde a otra asignatura; DOCX correcto pendiente |
| Inspeccionar Windows/MySQL/navegadores | misma fecha | NO_MEDIDO | ENTORNO, fuentes | MySQL activo, sin credenciales de negocio |
| Instalar dependencias aisladas | misma fecha | NO_MEDIDO | .venv-ep2, requirements | instaladas; no alterar entorno anterior |
| Validacion, conciliacion, Excel y auditoria | misma fecha | NO_MEDIDO | auxiliaries/, tests/test_core.py | pruebas sinteticas pasan |
| SQL y API propia | misma fecha | NO_MEDIDO | database/, api/, test_api.py | HTTP local real probado con memoria; MySQL pendiente |
| Primera prueba automatizada | evidencia pytest | 10.52 segundos | 34 casos primera corrida | 34 aprobados; no mide tiempo del robot |
| Demo sintetica | timestamps en output UUID | monotono en execution.json | Excel, JSON, logs | PARCIAL deliberado; no se navego con Selenium |
| Instalar Rocketbot a peticion del usuario | misma fecha | NO_MEDIDO | ZIP oficial y acceso directo | 2026 hash distinto, no ejecutado; 2025 hash verificado, Studio HTTP 200/licencia activa |
| Crear proyecto en Studio | 2026-10-16 10:11:39 local / misma fecha | NO_MEDIDO | studio_creacion.json, robot.db generado por aplicacion | base nativa real; montaje completo pendiente |
| Probar acceso TestFire | misma fecha | NO_MEDIDO | fallo requests SSLCertVerificationError | certificado vencido; no se desactivo verificacion |
| Diagramas e informe/presentacion | misma fecha | NO_MEDIDO | docs/diagramas, scripts generadores | revision visual documentada |
| Recibir pauta EP2 correcta | durante la sesion | NO_MEDIDO | pauta_ep2.txt y matriz | Contraste realizado; el pendiente inicial de fuente quedo resuelto |
| Ampliar cierre y reenvio | durante la sesion | NO_MEDIDO | bridge/database, test_bridge y test_outbox | Hash final del Excel recuperable tras fallo SQL inyectado |
| Demo nativa con controles y HTTP | 2026-10-16, tiempos UTC en execution.json | 11.206 s intervalo Audit | UUID e967c39e-3b8a-4df1-9d11-87dfcff8ac97 | PARCIAL; 3 validos/1 rechazo; HTTP y Excel probados; web/SQL pendientes |
| Pruebas locales ampliadas | evidencia pytest.xml | 11.25 s | 42 pruebas | 42 aprobadas; no acredita MySQL ni segunda PC |
| Consolidar entrega y exposicion | revision 2026-10-17 | NO_MEDIDO | informe/PPT/guion/paquete | Evidencia nativa incorporada; pendientes declarados |

Incidencias conservadas: primera lectura PDF fallo al imprimir Unicode (extraccion corregida); Mermaid CLI 12 ya no acepta -w/-H (se uso --size); un punto y coma en nota de secuencia produjo parseo fallido (corregido y renderizado); Firefox headless de inspeccion local cerro inesperadamente (se uso Chromium/Puppeteer para Studio). No presentar esos intentos como ejecuciones exitosas.

Incidencias posteriores: inicio de Studio detenido por dialogo opcional de drivers (resuelto al responder No); variables deben declararse antes de SetVar; runtime congelado sin zoneinfo (adaptador pytz); un ensayo nativo se interrumpio al cerrar el editor demasiado pronto y se conservo como INTERRUMPIDO. Ver DEMO_NATIVA_ROCKETBOT.md.
