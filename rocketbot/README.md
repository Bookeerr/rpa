# Proyecto nativo vigente

`MAIN_TESTFIRE_EP2/robot.db` es el proyecto de trabajo real de Studio. Contiene MAIN_TESTFIRE_EP2, WEB_LOGIN, EXTRACT_TRANSACTIONS y DEMO_LOCAL_EP2. MAIN realiza el flujo web, Excel externo y API local; la demo sintetica sigue disponible para pruebas aisladas.

`MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db` es el export oficial editable con MAIN y sus dos hijos. Los tres se reabrieron en Studio y sus variables exportadas estan vacias. El inventario de 54 comandos esta en [NATIVO_MAIN_VERIFICADO.md](../docs/NATIVO_MAIN_VERIFICADO.md). No se acredita una segunda PC.

Para ejecutar, abrir [INICIAR_EP2.bat](../INICIAR_EP2.bat) en la raiz y pulsar Run. El lanzador dentro de esta carpeta abre MAIN en el editor, pero no prepara por si mismo la API local.

Mantener esta estructura: el robot obtiene la raiz desde `%project_path%` y dos niveles superiores. No mover solo la base a otra carpeta. Guia detallada: [GUIA_COMPLETA_PROYECTO.md](../GUIA_COMPLETA_PROYECTO.md).

Para una nueva exportacion, guardar MAIN y usar la exportacion de robots a DB en Studio, incluyendo sus hijos y en modo editable, sin produccion. Comprobar la lista de robots y las dependencias en la copia. Los comandos del export actual son nativos; los auxiliares Python y sus dependencias se entregan por separado dentro del proyecto.
