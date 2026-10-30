# Bloques auxiliares para copiar a Execute Python

Estos fragmentos son codigo auxiliar, **no JSON importable**. Probar la persistencia del modulo entre comandos antes de ejecutar el robot completo. GetVar/SetVar son las funciones de Studio; no interpolar passwords en codigo Python.

Inicializacion (PROJECT_ROOT se elige al inicio):

```python
import sys
from pathlib import Path
root = Path(GetVar('PROJECT_ROOT')).resolve()
if not (root / 'auxiliaries' / 'bridge.py').is_file():
    raise ValueError('PROJECT_ROOT incorrecto')
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
from auxiliaries import bridge
result = bridge.initialize(str(root))
SetVar('execution_id', result['execution_id'])
SetVar('cfg', result['config'])
```

Inicio/fin de un paso (comandos distintos; cambiar step_id segun tabla):

```python
from auxiliaries import bridge
SetVar('evento', bridge.begin(GetVar('execution_id'), 'WEB_LOGIN', 1))
```

```python
from auxiliaries import bridge
bridge.end(GetVar('execution_id'), GetVar('evento'), 'OK')
```

Lectura SQL y Excel (dos comandos, cada uno con su auditoria):

```python
from auxiliaries import bridge
SetVar('reglas', bridge.read_rules(GetVar('execution_id')))
```

```python
from auxiliaries import bridge
SetVar('master', bridge.read_excel(GetVar('execution_id'), GetVar('cuentas_seleccionadas')))
```

Construir raw desde una fila cuyo encabezado se verifico. Este ejemplo solo sirve para el orden observado en EP1: ID, fecha/hora, cuenta, accion, importe. La condicion IF de cuenta y el For de filas quedan en Studio.

```python
fila = GetVar('fila')
SetVar('raw', {'web_id': fila[0] or None, 'date_raw': fila[1], 'account': fila[2],
              'description': fila[3], 'amount_raw': fila[4], 'currency': None,
              'balance': None, 'row_index': GetVar('indice'), 'source_url': GetVar('source_url')})
```

```python
from auxiliaries import bridge
SetVar('validacion', bridge.validate(GetVar('execution_id'), GetVar('raw'), 'testfire'))
```

IF `{validacion}['valid']` -> ejecutar bloque 1; ELSE -> bloque 2:

```python
from auxiliaries import bridge
bridge.append_valid(GetVar('execution_id'), GetVar('validacion')['row'])
```

```python
from auxiliaries import bridge
bridge.append_rejected(GetVar('execution_id'), GetVar('validacion'))
```

Conciliar, seguido de For e IF visibles:

```python
from auxiliaries import bridge
SetVar('pares', bridge.pairs(GetVar('execution_id')))
```

Dentro de For par: IF ambiguous; ELSE IF web is None; ELSE IF master is None; ELSE IF differences; ELSE. Cada rama asigna `clasificacion` mediante Asignar Variable y despues:

```python
from auxiliaries import bridge
bridge.append_result(GetVar('execution_id'), GetVar('par'), GetVar('clasificacion'))
```

Guardar snapshot, seguido de otro comando de sincronizacion:

```python
from auxiliaries import bridge
bridge.queue_bundle(GetVar('execution_id'))
```

```python
from auxiliaries import bridge
SetVar('reenviados', bridge.sync(GetVar('execution_id')))
```

HTTP: GET health, payload una sola vez, POST, GET id son cuatro comandos separados:

```python
from auxiliaries import bridge
SetVar('respuesta', bridge.http(GetVar('execution_id'), 'GET', '/health'))
```

```python
from auxiliaries import bridge
SetVar('payload', bridge.api_payload(GetVar('execution_id')))
```

```python
from auxiliaries import bridge
SetVar('respuesta', bridge.http(GetVar('execution_id'), 'POST', '/executions', GetVar('payload'), GetVar('intento')))
```

```python
from auxiliaries import bridge
SetVar('respuesta', bridge.http(GetVar('execution_id'), 'GET', '/executions/' + GetVar('execution_id')))
```

Solo dentro de IF respuesta.valid AND respuesta.body == payload:

```python
from auxiliaries import bridge
bridge.session(GetVar('execution_id'))['http_ok'] = True
```

Solo dentro de IF sesion_ok real se asigna web_ok=True de igual manera. No setear estas banderas para saltar verificaciones.

Exportacion:

```python
from auxiliaries import bridge
SetVar('reporte_rel', bridge.export_excel(GetVar('execution_id'), GetVar('estado_global')))
```

Tras cerrar navegador, terminar todos los eventos y reenviar cola:

```python
from auxiliaries import bridge
SetVar('resumen_final', bridge.finalize(GetVar('execution_id'), GetVar('estado_global')))
```

Mantener `error_original` antes de intentar captura. Ruta captura: `Path(PROJECT_ROOT) / 'output' / execution_id / 'capturas' / (evento + '.png')`; crear padre; pasar str(ruta) al comando Desktop. Registrar referencia relativa en auditoria. La captura debe excluir secretos y solo corresponde al equipo local.
