-- MySQL 8.4. No modifica la base nativa de Rocketbot.
CREATE DATABASE IF NOT EXISTS testfire_rpa CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE testfire_rpa;
CREATE TABLE IF NOT EXISTS executions (
 execution_id CHAR(36) PRIMARY KEY,
 hostname VARCHAR(255) NOT NULL, os_user VARCHAR(255) NOT NULL,
 robot_version VARCHAR(40) NOT NULL, config_hash CHAR(64) NOT NULL,
 started_at DATETIME(6) NOT NULL, ended_at DATETIME(6), duration_ms DECIMAL(16,3),
 status ENUM('EN_CURSO','OK','PARCIAL','ERROR','INTERRUMPIDO') NOT NULL,
 summary JSON NOT NULL, INDEX ix_execution_host_start(hostname, started_at)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS account_rules (
 account VARCHAR(32) PRIMARY KEY, enabled BOOLEAN NOT NULL,
 tolerance DECIMAL(18,2) NOT NULL DEFAULT 0.00, version VARCHAR(40) NOT NULL,
 CHECK (tolerance >= 0)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS step_audit (
 event_id CHAR(36) PRIMARY KEY, execution_id CHAR(36) NOT NULL,
 step_id VARCHAR(64) NOT NULL, step_order INT NOT NULL, attempt INT NOT NULL,
 started_at DATETIME(6) NOT NULL, ended_at DATETIME(6) NOT NULL,
 duration_ms DECIMAL(16,3) NOT NULL,
 status ENUM('OK','ERROR','ADVERTENCIA','OMITIDO') NOT NULL,
 detail TEXT NOT NULL, evidence TEXT,
 FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
 INDEX ix_step_execution(execution_id, step_order), CHECK (duration_ms >= 0)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS transactions (
 extraction_id CHAR(36) PRIMARY KEY, execution_id CHAR(36) NOT NULL,
 account VARCHAR(32) NOT NULL, row_index INT NOT NULL,
 transaction_date DATE NOT NULL, description_norm TEXT NOT NULL,
 amount DECIMAL(18,2) NOT NULL, currency VARCHAR(8), balance DECIMAL(18,2),
 web_id VARCHAR(128), source_url TEXT, raw_data JSON NOT NULL,
 FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
 UNIQUE KEY uq_extraction(execution_id, account, row_index),
 INDEX ix_movement(account, transaction_date, web_id)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS reconciliation_results (
 result_id CHAR(36) PRIMARY KEY, execution_id CHAR(36) NOT NULL,
 status ENUM('CONCILIADO','SOLO_WEB','SOLO_MASTER','DISCREPANCIA','AMBIGUO') NOT NULL,
 web_ref JSON, master_ref JSON, detail JSON NOT NULL,
 FOREIGN KEY (execution_id) REFERENCES executions(execution_id),
 INDEX ix_reconciliation(execution_id,status)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS api_calls (
 call_id CHAR(36) PRIMARY KEY, execution_id CHAR(36) NOT NULL,
 method VARCHAR(8) NOT NULL, endpoint TEXT NOT NULL, attempt INT NOT NULL,
 duration_ms DECIMAL(16,3) NOT NULL, http_status INT, error VARCHAR(255),
 request_ref TEXT, response_ref TEXT,
 FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS artifacts (
 artifact_id CHAR(36) PRIMARY KEY, execution_id CHAR(36) NOT NULL,
 hostname VARCHAR(255) NOT NULL, relative_path VARCHAR(512) NOT NULL,
 kind VARCHAR(32) NOT NULL, sha256 CHAR(64) NOT NULL,
 availability ENUM('LOCAL','SHARED') NOT NULL,
 FOREIGN KEY (execution_id) REFERENCES executions(execution_id)
) ENGINE=InnoDB;
-- Servicio API: acuse del resumen ANTERIOR al cierre, independiente de executions.
CREATE TABLE IF NOT EXISTS api_receipts (
 execution_id CHAR(36) PRIMARY KEY, payload_hash CHAR(64) NOT NULL,
 payload JSON NOT NULL, received_at DATETIME(6) NOT NULL DEFAULT (UTC_TIMESTAMP(6))
) ENGINE=InnoDB;
