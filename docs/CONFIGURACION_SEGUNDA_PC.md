# Dos PC con Rocketbot y datos compartidos

**Validacion completada:** la ejecucion real `6d450ccd-3e4a-4c19-a03d-d0f3aa9bdcc4` de **DESKTOP-OFQ9QLA** informa cierre web/Excel/API y su resumen fue confirmado en el servidor mediante SQLite y GET HTTP 200. Ver [VALIDACION_SEGUNDA_PC.md](VALIDACION_SEGUNDA_PC.md). Las notas de preparacion siguientes conservan el historial; la etiqueta estatica SEGUNDA_PC del cierre antiguo ya no representa el estado de esta comprobacion.

Si el primer comando muestra `No module named 'dotenv'`, aplicar [CORRECCION_DEPENDENCIAS_ROCKETBOT.md](CORRECCION_DEPENDENCIAS_ROCKETBOT.md). Las dependencias Python puras ahora viajan dentro del proyecto y requieren reiniciar Rocketbot tras aplicar el parche.

Actualizacion del cliente: el usuario confirmo `API compartida lista; maestro descargado y verificado`. La conexion autenticada y la descarga ya se comprobaron desde la segunda PC por su reporte. Se corrigio la deteccion de Rocketbot instalado en otra ruta; aplicar [CORRECCION_RUTA_ROCKETBOT.md](CORRECCION_RUTA_ROCKETBOT.md). La ejecucion completa y la activacion del runtime siguen pendientes de comprobar.

Segunda PC indicada por el usuario: **DESKTPO-OFQ9QLA**, IPv4 **192.168.1.96**. Detectada como vecino alcanzable en Wi-Fi desde el host; no respondio a ping. El usuario confirmo Python y Rocketbot instalados, respuesta HTTP 401 desde el navegador y, posteriormente, descarga autenticada del maestro desde el lanzador.

Configuracion preparada el 19 de octubre de 2026. Host: **DESKTOP-HNO1Q0F**, Wi-Fi privado, IPv4 **192.168.1.91/24**. Ambas PC ejecutan su propio Rocketbot. La segunda PC todavia debe comprobarse desde su Windows; una prueba en este host no acredita el segundo equipo.

Estado comprobado en el host: API iniciada, firewall aplicado con elevacion de Windows, 57 pruebas automatizadas aprobadas y descarga autenticada desde una copia temporal del cliente con SHA-256 coincidente. Evidencia local en `output/private/verificacion_red.json` y `output/private/firewall_red.json`. No se ha iniciado sesion ni ejecutado Rocketbot remotamente en la segunda PC.

## Que se comparte

| Elemento | Ubicacion y funcionamiento |
|---|---|
| API | `http://192.168.1.91:18081`, en el host |
| Resumenes de ambas PC | `output/api_local/receipts.db` del host, SQLite mediante HTTP autenticado |
| Maestro Excel | El host publica el archivo de `MASTER_EXCEL_PATH`; el cliente descarga una copia antes de abrir Studio |
| Reportes Excel detallados | `output/<UUID>/` de cada PC; no se suben al servidor |
| Robot editable | Copia independiente de `rocketbot/MAIN_TESTFIRE_EP2/robot.db` en cada PC |
| MySQL | Sigue pendiente; esta conexion no prueba integracion MySQL |

Cada resumen contiene el UUID y el hostname real. SQLite solo se abre dentro del servidor: no se comparte su archivo por SMB. El maestro se descarga con token, se comprueban SHA-256, estructura y periodo, y luego se reemplaza atomicamente la copia del cliente. Si falla la conexion o la validacion, el lanzador se detiene y conserva el maestro anterior. No inicia una API local alternativa.

## 1. En esta PC, servidor

1. La regla de firewall ya fue aplicada en este host. Para recrearla, abrir **HABILITAR_RED.bat con clic derecho > Ejecutar como administrador**. Windows exige elevacion para modificar el firewall. El script habilita exclusivamente TCP 18081 en la IP del host, interfaz correspondiente, perfil Privado y subred local. No abre Rocketbot 5000 ni MySQL 3306.
2. Abrir `INICIAR_EP2.bat`. Esto inicia la API en segundo plano y abre Rocketbot. Si Studio estaba cerrado, atender su dialogo de drivers y volver a abrir el lanzador cuando este listo.
3. Mantener esta PC encendida y conectada al Wi-Fi durante el trabajo de ambas. Tras reiniciar Windows, volver a abrir el lanzador: no se ha instalado un servicio de inicio automatico.
4. Copiar al otro equipo **`output/private/TestFire_CLIENTE_PRIVADO.zip`**, preferentemente mediante un pendrive. Contiene el token compartido y la configuracion del cliente; es una copia privada de trabajo, no el ZIP para entregar al docente ni para publicar. No contiene credenciales SQL del host ni entornos virtuales/licencias de Rocketbot.

La API usa HTTP en una red local de confianza para este laboratorio; el token no cifra el trafico. No publicar el puerto en Internet. MySQL tiene su guia separada en `INSTALACION_HOST_WINDOWS.md`.

## 2. En la segunda PC

1. Conectarse al mismo Wi-Fi. Presionar Windows + R, escribir `cmd` y ejecutar `hostname` e `ipconfig`. Anotar nombre e IPv4 del adaptador Wi-Fi.
2. Extraer completamente el ZIP privado en una carpeta propia, por ejemplo `Documentos\TestFire_CLIENTE`. No ejecutar archivos dentro del ZIP. No copiar `.venv-ep2` desde el host.
3. Tener Python 3.13 instalado (codigo requiere 3.11 o superior) y Rocketbot instalado y activado para ese equipo. La licencia de esta PC no se copia. Version de Rocketbot validada: 2025.07.01. Si esta en otra ruta, configurar la variable de entorno de usuario `ROCKETBOT_EXE` con la ruta completa de `rocketbot.exe`.
4. Ejecutar `PREPARAR_OTRA_PC.bat`. Crea su entorno Python, instala dependencias, verifica la API, descarga el maestro e incluye `dotenv` y `pytz` en `auxiliaries/_vendor` para que Rocketbot los encuentre. Reiniciar Rocketbot si estaba abierto. No instala ni activa Rocketbot.
5. Ejecutar `INICIAR_EP2.bat` y abrir **MAIN_TESTFIRE_EP2**. El robot y sus hijos ya estan en la base incluida; conservar la estructura completa del proyecto.
6. Pulsar Run. Al terminar, revisar `output/<UUID>/execution.json` y el Excel de esa ejecucion.

En la segunda PC, `.env` contiene `API_ROLE=client` y `API_BASE_URL=http://192.168.1.91:18081`. No cambiarlo a localhost: localhost siempre significa la PC donde se ejecuta el programa.

## 3. Comprobaciones reales

Desde PowerShell en el cliente:

```powershell
Test-NetConnection 192.168.1.91 -Port 18081
```

`TcpTestSucceeded=True` confirma el puerto. `PingSucceeded=False` por si solo no demuestra que la API falle. La comprobacion autenticada y la descarga se ejecutan con:

```powershell
.\.venv-ep2\Scripts\python.exe -m scripts.start_local_services
```

La evidencia de la descarga queda en `output/private/maestro_compartido.json`: comparar su hash con el maestro del host. Abrir `/health` directamente en el navegador sin token devuelve **401**; es lo esperado.

Ejecutar una corrida en cada equipo, conservar sus UUID distintos, nombres reales, Excel y evidencias HTTP POST/GET. Los dos resumenes deben poder consultarse en el mismo servidor mediante `/executions/<UUID>` usando el token local. No pegar tokens en el chat ni en capturas. La concurrencia de dos clientes simulados en tests no reemplaza estas corridas fisicas. Mientras falte esta evidencia, `SEGUNDA_PC` sigue pendiente en el cierre del robot.

## 4. Archivos que configuran la conexion

| Archivo | Responsabilidad |
|---|---|
| `.env` | Rol local/server/client, IP, puerto y token privado |
| `scripts/prepare_network.py` | Guarda respaldo privado del `.env`, configura el host y genera el ZIP privado del cliente |
| `HABILITAR_RED.bat` / `scripts/enable_lan.ps1` | Regla acotada del firewall; requiere administrador |
| `PREPARAR_OTRA_PC.bat` / `scripts/setup_network_client.ps1` | Dependencias y comprobacion inicial del cliente |
| `scripts/start_local_services.py` | Arranca API propia para host/local, o conecta al host si es cliente |
| `scripts/api_local.py` | API SQLite, ligada a loopback en modo local o a la IP privada en modo server |
| `scripts/network_services.py` | Valida IP/rol y descarga/verifica el maestro |
| `api/app.py` | Autenticacion y rutas `/health`, `/master`, `/executions` |
| `api/local_store.py` | Persistencia, transacciones e idempotencia de resumenes |
| `output/private/api.stderr.log` | Diagnostico del servidor |

## 5. Si no conecta o cambia la IP

- Comprobar que el host este encendido y su API iniciada, y que ambas PC usen el mismo Wi-Fi, sin una red de invitados con aislamiento entre clientes.
- Si falla TCP: ejecutar la regla del firewall como administrador en el host y verificar IP actual con `ipconfig`.
- Si TCP funciona pero aparece HTTP 401: el token debe coincidir en ambos `.env`. Reextraer la copia privada actual o corregirlo localmente.
- Si falla el maestro: cerrar el Excel del cliente, revisar que el periodo sea igual al del host y leer el error del lanzador.
- Si falta Rocketbot: instalarlo y activarlo en ese equipo. La comprobacion HTTP puede funcionar aunque aun no haya runtime.
- Si la IP del host cambia por DHCP: cerrar su API, ejecutar `python -m scripts.prepare_network --host NUEVA_IP` con el Python de `.venv-ep2`, volver a aplicar `HABILITAR_RED.bat` y distribuir la configuracion actualizada. Reservar `192.168.1.91` en el router evita cambios; no se modifico el router.

Para volver al modo local, configurar `API_ROLE=local`, `API_BASE_URL=http://127.0.0.1:18081`, `API_BIND_HOST=127.0.0.1`, `API_PORT=18081` y reiniciar la API propia. El respaldo anterior del `.env` queda en `output/private/env_antes_red_*.bak`. Un administrador puede quitar solamente esta regla con `Remove-NetFirewallRule -Name TestFire-EP2-API-LAN`.
