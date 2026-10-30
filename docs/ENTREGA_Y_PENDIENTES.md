# Entrega revisada — 18/10/2026

Abrir INICIAR_EP2.bat y pulsar Run en MAIN_TESTFIRE_EP2. Mantener Studio abierto hasta finalizar. API local persistente loopback 18081 iniciada por el lanzador. Reporte comprobado: output/076648bf-3612-42b9-b915-d14cd7982d57/Reporte_TestFire_20261018_084434_076648bf-3612-42b9-b915-d14cd7982d57.xlsx.

Ejecucion 076648bf-3612-42b9-b915-d14cd7982d57: 96 validos, 4 rechazados; clasificaciones {'SOLO_MASTER': 100, 'SOLO_WEB': 96}; 206.514 s. Rechazos por causa: {'Importe fuera de DECIMAL(18,2)': 4}.

Paquete entrega/TestFire_EP2_20261018.zip: incluye proyecto nativo, codigo, dependencias declaradas, recorder, informe PDF, PPT/PDF, guion, diagramas, pruebas y corrida seleccionada. Excluye .env, licencias, entornos virtuales, originales EP1 y fuentes docentes. MANIFEST_SHA256.json verifica cada archivo.

Para otro equipo: instalar Rocketbot, abrir robot.db con Studio, instalar requirements-dev-ep2.txt en .venv-ep2; configurar .env local: cuenta publica TestFire, TESTFIRE_URL=http://demo.testfire.net/, MASTER_EXCEL_PATH=data/master_snapshot_testfire.xlsx, API_BASE_URL=http://127.0.0.1:18081 y API_TOKEN aleatorio compartido entre robot y API. Mantener periodo de octubre 2026 o actualizar maestro/periodo conjuntamente. DB_PASSWORD puede seguir REEMPLAZAR en este modo; no se abre conexion MySQL. Instalar dotenv/openpyxl/requests/pymysql y fallback pytz en Python de Rocketbot segun ENTORNO.md. La prueba de otra PC sigue pendiente.

Export oficial: rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db contiene MAIN_TESTFIRE_EP2 y los hijos WEB_LOGIN y EXTRACT_TRANSACTIONS. Se reabrieron los tres mediante Studio y se verificaron variables vacias. Conservar la carpeta relativa indicada. Inventario y procedimiento en NATIVO_MAIN_VERIFICADO.md.

Pendientes: MySQL por instruccion del usuario; validacion real en segunda PC; aceptacion docente del grabador DOM alternativo; ensayo oral y aporte personal del expositor; video de respaldo si lo exige el docente. El PPTX es editable y el PDF paralelo fue generado desde el mismo contenido, no exportado desde PowerPoint. Revisar PPT en el equipo de exposicion.

El maestro es snapshot previo, no fuente contable independiente; la vista son 100 recientes. Estos limites no deben omitirse durante la defensa. La nota depende de la evaluacion docente, especialmente la presentacion individual (80% del ET).
