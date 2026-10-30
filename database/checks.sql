USE testfire_rpa;
SELECT execution_id,hostname,started_at,ended_at,status FROM executions ORDER BY started_at DESC;
SELECT execution_id,step_order,step_id,attempt,status,duration_ms FROM step_audit ORDER BY execution_id,step_order;
SELECT step_id,COUNT(*) attempts,AVG(duration_ms) avg_ms,MAX(duration_ms) max_ms FROM step_audit GROUP BY step_id;
SELECT * FROM step_audit WHERE status='ERROR';
SELECT execution_id,status,COUNT(*) rows_count FROM reconciliation_results GROUP BY execution_id,status;
SELECT execution_id,account,row_index,COUNT(*) duplicates FROM transactions GROUP BY execution_id,account,row_index HAVING COUNT(*)>1;
SELECT execution_id,hostname,started_at FROM executions WHERE status='EN_CURSO';
SELECT execution_id,payload_hash,received_at FROM api_receipts;
