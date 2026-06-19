BEGIN;

ALTER TABLE cycle_event
    DROP CONSTRAINT IF EXISTS ck_cycle_event_ack_status;

ALTER TABLE cycle_event
    ADD CONSTRAINT ck_cycle_event_ack_status
    CHECK (ack_status IN ('PENDING', 'ACK_OK', 'ACK_WRITE_FAILED'));

ALTER TABLE collector_runtime_status
    ADD COLUMN IF NOT EXISTS plc_boot_id TEXT,
    ADD COLUMN IF NOT EXISTS ack_timeout BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE collector_error_log
    ADD COLUMN IF NOT EXISTS plc_boot_id TEXT;

CREATE INDEX IF NOT EXISTS idx_collector_error_log_type_time
    ON collector_error_log (error_type, created_at DESC);

COMMIT;
