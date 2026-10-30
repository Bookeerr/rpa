# Selectores comprobados — TestFire, 18/10/2026

| Accion | Selector |
|---|---|
| Usuario | //*[@id="uid"] |
| Clave | //*[@id="passw"] |
| Login | //input[@name="btnSubmit"] |
| Transacciones | //a[@href="/bank/transaction.jsp"] |
| Tabla | //table[@id="_ctl0__ctl0_Content_Main_MyTransactions"] |

Esperas por presencia de objetos con limite de 30 segundos; navegacion y extraccion ejecutadas nativamente por Rocketbot. Cabeceras y filas originales en output del UUID seleccionado. La fecha real es YYYY-MM-DD HH:MM: usar testfire_minute, no asumir segundos. Una fila totalmente vacia es maquetacion; una fila no vacia mal estructurada falla. La vista ofrece los 100 mas recientes, no todo el historial.

HTTPS fallo por certificado. HTTP se usa solo para la cuenta publica de demostracion, como excepcion local documentada; no se desactivo TLS global ni se ingresaron cuentas privadas.
