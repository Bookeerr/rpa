# Validacion de filas

Implementacion: `auxiliaries/validation.py`. En Studio: S05, comando `Ejecutar Python` por fila; el bloque **IF** usa `valid` para agregar a Movimientos o Rechazados.

| Regla | Patron / conversion | Acepta | Rechaza |
|---|---|---|---|
| Fecha ISO | `^\d{4}-\d{2}-\d{2}$` + strptime | 2026-10-01 | 2026-02-30, 01/10/2026 |
| Fecha candidata TestFire | `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{1,6})?$` + strptime | 2026-10-01 12:05:00.0 | meses/dias imposibles |
| Importe US | `^(?P<sign>-)?\$?(?P<number>(?:\d{1,3}(?:,\d{3})+|\d+)\.\d{2})$` | -25.00, $1,234.56 | 1.234,56; 12,34.56; vacio |
| UUID | `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$` + UUID | UUID generado | texto arbitrario |
| Reporte | `^Reporte_TestFire_\d{8}_\d{6}_[0-9a-fA-F-]{36}\.xlsx$` | nombre generado con UUID | nombre sin UUID |

Los parentesis externos del importe son negativos y se eliminan antes del Regex; `(-1.00)` se rechaza por doble signo. Se conserva `Decimal`, no float, en calculos; Excel representa numericamente el resultado y JSON conserva la cadena decimal exacta. No se convierten valores ambiguos a cero. La descripcion normaliza Unicode NFKC, espacios y mayusculas; se conserva el original en `raw`.

El formato fecha TestFire es candidato tomado del antecedente; la comprobacion del DOM autenticado actual esta pendiente por TLS/Studio. No se mezclan convenciones regionales automaticamente. El saldo y moneda se mantienen nulos cuando no hay evidencia.
