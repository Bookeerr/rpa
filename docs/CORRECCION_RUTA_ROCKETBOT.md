# Correccion del lanzador para la segunda PC

El cliente informo descarga autenticada y verificada del maestro. La conexion con el host funciona; falta completar la ejecucion del robot en la segunda PC.

El error de `open_studio.ps1` ocurria porque se comprobaba una ruta fija de Rocketbot antes de comprobar si Studio ya estaba abierto. El lanzador ahora abre el robot en el Studio disponible sin exigir esa ruta. Si Studio esta cerrado, busca el ejecutable activo, la variable ROCKETBOT_EXE, PATH y la ruta original. Si no lo encuentra, ofrece seleccionar `rocketbot.exe` y guarda la ruta para ese usuario de Windows.

## Aplicar en D:\TestFire_CLIENTE

1. Mantener Rocketbot abierto en la segunda PC.
2. Extraer `Correccion_Rocketbot_CLIENTE.zip` directamente dentro de `D:\TestFire_CLIENTE`, reemplazando los archivos de `scripts`. No extraer dentro de `scripts` ni crear otra carpeta intermedia. El ZIP no contiene `.env`, tokens ni bases de datos.
3. Ejecutar `PREPARAR_OTRA_PC.bat` para completar las dependencias del runtime. Si aparece un selector, elegir el `rocketbot.exe` de esa instalacion. Una ruta de ejemplo de otro equipo no sirve.
4. Abrir `INICIAR_EP2.bat`; debe mostrar MAIN_TESTFIRE_EP2 en Studio. Ejecutar Run y revisar la carpeta de salida de esa corrida.

El log tambien contiene `No license file`. Este parche no modifica ni activa licencias. Comprobar en Studio el estado de activacion de esa PC; si solicita licencia, completar la activacion legitima antes de ejecutar. Ese texto por si solo no confirma el estado final de la licencia. El aviso WNDPROC fue seguido por la carga de Studio segun el log recibido; verificar por separado si impide alguna accion.

Los logs pueden incluir tokens de licencia. Compartir solo el error y ocultar la seccion `License Token`.
