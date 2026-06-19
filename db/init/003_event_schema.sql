CREATE TABLE IF NOT EXISTS raw_plc_sample (
    id BIGSERIAL PRIMARY KEY,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    db_number INTEGER NOT NULL,
    read_start INTEGER NOT NULL,
    read_size INTEGER NOT NULL,
    raw_hex TEXT NOT NULL,
    decoded_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    sample_time TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_plc_sample_station_time
    ON raw_plc_sample (plc_id, station_id, sample_time DESC);

CREATE TABLE IF NOT EXISTS cycle_event (
    id BIGSERIAL PRIMARY KEY,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    plc_boot_id TEXT NOT NULL DEFAULT 'UNKNOWN',
    cycle_counter BIGINT NOT NULL,
    trace_key TEXT,
    pallet_id TEXT,
    dmc TEXT,
    child_dmc TEXT,
    label_code TEXT,
    final_product_id TEXT,
    part_id TEXT,
    plc_start_time TIMESTAMPTZ,
    plc_end_time TIMESTAMPTZ,
    edge_read_time TIMESTAMPTZ NOT NULL DEFAULT now(),
    edge_write_time TIMESTAMPTZ,
    cycle_time_ms INTEGER,
    wait_time_ms INTEGER,
    result TEXT NOT NULL DEFAULT 'UNKNOWN',
    nok_codes INTEGER[] NOT NULL DEFAULT ARRAY[]::INTEGER[],
    alarm_code INTEGER NOT NULL DEFAULT 0,
    downtime_type INTEGER NOT NULL DEFAULT 0,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    source TEXT NOT NULL DEFAULT 'PLC_S7',
    ack_status TEXT NOT NULL DEFAULT 'PENDING',
    retry_count INTEGER NOT NULL DEFAULT 0,
    raw_sample_id BIGINT REFERENCES raw_plc_sample(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_cycle_event_plc_station_counter
        UNIQUE (plc_id, station_id, plc_boot_id, cycle_counter),
    CONSTRAINT ck_cycle_event_ack_status
        CHECK (ack_status IN ('PENDING', 'ACK_OK', 'ACK_WRITE_FAILED'))
);

CREATE INDEX IF NOT EXISTS idx_cycle_event_line_station_end_time
    ON cycle_event (line_id, station_id, plc_end_time DESC);

CREATE INDEX IF NOT EXISTS idx_cycle_event_trace_key
    ON cycle_event (trace_key);

CREATE INDEX IF NOT EXISTS idx_cycle_event_label_code
    ON cycle_event (label_code);

CREATE INDEX IF NOT EXISTS idx_cycle_event_ack_status
    ON cycle_event (ack_status);

CREATE TABLE IF NOT EXISTS quality_event (
    id BIGSERIAL PRIMARY KEY,
    cycle_event_id BIGINT REFERENCES cycle_event(id) ON DELETE CASCADE,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    dmc TEXT,
    label_code TEXT,
    result TEXT NOT NULL,
    nok_codes INTEGER[] NOT NULL DEFAULT ARRAY[]::INTEGER[],
    nok_source TEXT NOT NULL DEFAULT 'PLC',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_quality_event_station_time
    ON quality_event (plc_id, station_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_quality_event_result_time
    ON quality_event (result, created_at DESC);

CREATE TABLE IF NOT EXISTS collector_runtime_status (
    id BIGSERIAL PRIMARY KEY,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    collector_state TEXT NOT NULL DEFAULT 'STARTING',
    plc_connection_state TEXT NOT NULL DEFAULT 'UNKNOWN',
    station_status TEXT NOT NULL DEFAULT 'UNKNOWN',
    payload_ready BOOLEAN NOT NULL DEFAULT FALSE,
    read_done BOOLEAN NOT NULL DEFAULT FALSE,
    last_cycle_counter BIGINT,
    last_success_time TIMESTAMPTZ,
    last_error_code TEXT,
    last_error_message TEXT,
    plc_boot_id TEXT,
    ack_timeout BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_collector_runtime_status_station
        UNIQUE (plc_id, station_id)
);

CREATE INDEX IF NOT EXISTS idx_collector_runtime_status_updated
    ON collector_runtime_status (updated_at DESC);

CREATE TABLE IF NOT EXISTS collector_error_log (
    id BIGSERIAL PRIMARY KEY,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT,
    error_type TEXT NOT NULL,
    error_message TEXT NOT NULL,
    plc_boot_id TEXT,
    cycle_counter BIGINT,
    raw_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_collector_error_log_time
    ON collector_error_log (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_collector_error_log_type_time
    ON collector_error_log (error_type, created_at DESC);

CREATE TABLE IF NOT EXISTS data_gap_event (
    id BIGSERIAL PRIMARY KEY,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    start_cycle_counter BIGINT,
    end_cycle_counter BIGINT,
    last_label_code TEXT,
    current_label_code TEXT,
    missing_count INTEGER NOT NULL DEFAULT 0,
    reason TEXT NOT NULL,
    operator_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_data_gap_event_station_time
    ON data_gap_event (plc_id, station_id, created_at DESC);
