# Configuracion

`.env.example` esta en la raiz y contiene solo placeholders. Crear `.env` local para flujo real. Usuario pidio dejar configuracion MySQL pendiente durante esta sesion; no se altero el servicio existente.

`requirements-ep2.lock.txt` registra el entorno externo usado en pruebas. No es una receta para sobreescribir el runtime de Rocketbot. Mantener sus dependencias separadas.

Rutas: PROJECT_ROOT absoluta solo en memoria; archivos internos relativos. MASTER_EXCEL_PATH admite excepcionalmente ruta externa (documentar por PC); OUTPUT_ROOT debe quedar dentro de raiz. Host/URL no son rutas de archivos. Timezone America/Santiago; fechas de auditoria UTC.
