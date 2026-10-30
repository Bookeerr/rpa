# Corregir No module named dotenv

La descarga del maestro funciona con el Python de `.venv-ep2`, pero el robot se ejecuta dentro del Python propio de Rocketbot. Instalar paquetes en el primero no los hace visibles en el segundo. El error ocurre al importar configuracion, antes del login.

La correccion incorpora `python-dotenv` y `pytz` dentro de `auxiliaries/_vendor`, con sus licencias y hashes. `auxiliaries/__init__.py` agrega esa carpeta a la ruta de importacion. No se agregan bibliotecas binarias del entorno virtual ni se necesita escribir en la instalacion de Rocketbot. El resto de los modulos del robot sigue usando las bibliotecas del runtime.

## Aplicar en la otra PC

1. Pulsar Stop. Cerrar Rocketbot completamente, incluida su consola o proceso; cerrar solo la pestana no reinicia el Python interno.
2. Extraer `Correccion_Dependencias_CLIENTE.zip` directamente dentro de `D:\TestFire_CLIENTE`, aceptando reemplazar archivos. Deben existir `D:\TestFire_CLIENTE\auxiliaries\_vendor\dotenv\__init__.py` y el nuevo `auxiliaries\__init__.py`.
3. Abrir `INICIAR_EP2.bat`. Si indica que Studio esta iniciandose, esperar y abrir nuevamente el lanzador.
4. Ejecutar MAIN_TESTFIRE_EP2 y comprobar que el primer comando ya no muestra el error de importacion. Conservar el resultado de esa nueva ejecucion.

El ZIP contiene las dependencias listas para usar; no necesita reinstalar Python ni modificar `.env`. Para reconstruirlas despues de instalar dependencias, ejecutar `.venv-ep2\Scripts\python.exe -m scripts.package_runtime_dependencies`. `PREPARAR_OTRA_PC.bat` ahora realiza ese paso automaticamente.

El parche no activa licencias ni acredita por si solo la corrida en la segunda PC. Si aparece otro error, compartir el comando y el mensaje ocultando tokens y contrasenas.
