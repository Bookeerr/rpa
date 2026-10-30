USE testfire_rpa;
-- SINTETICO: revisar cuentas reales antes de usar en Studio.
INSERT INTO account_rules(account,enabled,tolerance,version)
VALUES ('800003',TRUE,0.00,'SINTETICO-1'),('800011',FALSE,0.00,'SINTETICO-1')
ON DUPLICATE KEY UPDATE account=account;
