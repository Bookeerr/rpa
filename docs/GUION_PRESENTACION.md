# Guion individual — 11 minutos previstos

Evaluacion anunciada: martes 20 de octubre de 2026. Ensayo real y aporte personal: completar por el estudiante. No atribuirse trabajo de otros ni inventar mediciones.

| Tiempo | Explicacion y demostracion |
|---|---|
| 0:00–1:00 | Problema y continuidad EP1: consulta, validacion y conciliacion. |
| 1:00–3:00 | Abrir MAIN, mostrar comandos web/For/IF/While/Try Catch y lanzar. Explicar recorder DOM, export y limite de aceptacion. |
| 3:00–5:00 | Mientras ejecuta, mostrar XPath y cabeceras reales, fecha con minutos, Decimal y ejemplo rechazado. |
| 5:00–7:00 | Mostrar maestro externo y metadata/hash; cinco clasificaciones. Explicar snapshot previo y MySQL pendiente autorizado. |
| 7:00–9:00 | GET/POST/GET, 201 nuevo/200 repetido/409 conflicto, UUID y acuse persistente. Mostrar evidencia de la corrida seleccionada si la demo sigue activa. |
| 9:00–11:00 | Abrir Excel de cinco hojas y auditoria; explicar SCAMPER, limites, segunda PC y siguientes mejoras. |

Evidencia seleccionada: 076648bf-3612-42b9-b915-d14cd7982d57. Ejecucion 076648bf-3612-42b9-b915-d14cd7982d57: 96 validos, 4 rechazados; clasificaciones {'SOLO_MASTER': 100, 'SOLO_WEB': 96}; 206.514 s. Rechazos por causa: {'Importe fuera de DECIMAL(18,2)': 4}. Para demo lenta o sitio caido, abrir el Excel y JSON de esa corrida; rotular evidencia guardada, no ejecucion en vivo. No hay video de respaldo acreditado.

## Evidencia adicional de la segunda PC

Mostrar docs/VALIDACION_SEGUNDA_PC.md: ejecucion 6d450ccd-3e4a-4c19-a03d-d0f3aa9bdcc4, DESKTOP-OFQ9QLA, 96 validos, 4 rechazados y 103,525 s. El host conserva el acuse y GET responde 200. La etiqueta SEGUNDA_PC en el JSON era estatica y ya esta superada; MySQL sigue pendiente. El Excel del cliente no fue inspeccionado aqui: usar el Excel local de referencia para mostrar sus cinco hojas. La presentacion actual tiene nueve diapositivas; dedicar un minuto a red y uno a HTTP, manteniendo unos 11 minutos previstos.

## Preguntas para la defensa

- ¿Por que Regex no basta? Valida forma; strptime rechaza dias imposibles y Decimal evita errores binarios en dinero.
- ¿Como evita duplicados HTTP? UUID estable, clave primaria y comparacion del mismo payload: 201 creado, 200 repetido, 409 diferente.
- ¿Que cambia respecto a EP1? Coordinacion visible en Rocketbot, fuente Excel independiente del run, clasificacion y servicio HTTP con evidencia.
- ¿Se probo MySQL? No, esta pendiente por indicacion del usuario. La pauta admite Excel o SQL; SQLite es almacenamiento de la API local y no prueba MySQL.
- ¿El recorder es oficial? No. Es un grabador DOM propio con eventos reales y replay nativo; su aceptacion por el docente queda pendiente.
- ¿Se obtuvo todo el historial? No, los 100 recientes visibles. Ampliar filtros por cuenta/periodo y origen contable es una mejora.
- ¿Cuanto tiempo ahorra? No hay muestra manual comparable; solo se informa duracion de la corrida medida.
- ¿Que hiciste personalmente? Responder solo tareas realmente realizadas y comprendidas; completar nombres y aporte antes de presentar.
