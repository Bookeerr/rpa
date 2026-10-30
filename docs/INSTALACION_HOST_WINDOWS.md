# Host Windows y MySQL

Para la conexion actual de ambas PC mediante la API SQLite y maestro compartido, seguir [CONFIGURACION_SEGUNDA_PC.md](CONFIGURACION_SEGUNDA_PC.md). El procedimiento MySQL que sigue es una alternativa pendiente y no fue aplicado para conectar estos equipos.

Inspeccion real: servicio MySQL84 Running, cliente MySQL 8.4.9. No se proporcionaron credenciales SQL; no se cambiaron usuarios, contrasenas ni firewall del servidor existente. Esquema y permisos de negocio aun PENDIENTES de aplicar.

1. Reservar IP privada fija por DHCP y comprobar perfil de red Privado. Host encendido durante demo. Identificar su IPv4 mediante `Get-NetIPConfiguration`.
2. Usar MySQL Server como servicio. Si se instala en otra PC, usar instalador oficial MySQL y registrar version. Configurar bind-address con la IP LAN prevista; reiniciar servicio en una ventana acordada, pues puede tener otras bases.
3. Abrir cliente administrador de MySQL local. Aplicar `database/schema.sql` y `database/reference_data.sql` mediante comando `source` del cliente, usando ruta resuelta al proyecto. No importar en la base nativa de Rocketbot. Referencias son SINTETICAS.
4. Crear usuarios limitados por IP de cliente, sin `%` cuando se conocen IPs. No usar root en robot.

Ejemplo SQL **a adaptar** en consola administrativa (no ejecutado):

```sql
CREATE USER 'rpa_client'@'192.168.1.51' IDENTIFIED BY 'CAMBIAR_LOCALMENTE';
GRANT SELECT ON testfire_rpa.account_rules TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.executions TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.step_audit TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.transactions TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.reconciliation_results TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.api_calls TO 'rpa_client'@'192.168.1.51';
GRANT SELECT, INSERT, UPDATE ON testfire_rpa.artifacts TO 'rpa_client'@'192.168.1.51';
CREATE USER 'rpa_api'@'localhost' IDENTIFIED BY 'OTRA_CLAVE_LOCAL';
GRANT SELECT, INSERT ON testfire_rpa.api_receipts TO 'rpa_api'@'localhost';
```

La API debe iniciarse con DB_USER/DB_PASSWORD de rpa_api sobre variables de entorno del proceso. El cliente usa rpa_client. Para demo en el mismo equipo crear el usuario cliente tambien en localhost con esos privilegios. Las contrasenas se introducen localmente; nunca agregar al SQL versionado.

5. Firewall: regla entrante TCP 3306 solo perfil Private y RemoteAddress de clientes; 8000 solo clientes si se habilita API LAN. No abrir Internet ni reenviar puertos del router. Ejemplo PowerShell administrativo, despues de sustituir IPs:

```powershell
New-NetFirewallRule -DisplayName 'TestFire MySQL LAN' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 3306 -Profile Private -RemoteAddress 192.168.1.51
New-NetFirewallRule -DisplayName 'TestFire API LAN' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000 -Profile Private -RemoteAddress 192.168.1.51
```

6. Configurar `.env` en cada cliente. `API_BIND_HOST` solo corresponde al host API; usar su IP privada. `API_BASE_URL` en clientes apunta a esa IP. Token no se incluye en export.
7. `Test-NetConnection <IP_HOST> -Port 3306` solo comprueba TCP. Ejecutar `ejecutar_ep2.bat -Action check` para autenticacion, VERSION(), CURRENT_USER() y lectura de reglas. Consultas de `database/checks.sql` comprueban escrituras y tiempos.
8. Iniciar API con `-Action api`; probar GET/POST/GET desde cliente y confirmar api_receipts en SQL. Flask se usa para laboratorio; no se declara servidor de produccion ni servicio Windows instalado.

Si el host falla, el robot registra ERROR del paso y PARCIAL global; guarda cola y reporte local. La referencia SQL a un archivo no comparte el archivo. SMB/descarga autenticada estan fuera de esta entrega. VM opcional futura: aisla y permite snapshots, pero añade RAM, disco, red y configuracion; no es requisito inicial.
