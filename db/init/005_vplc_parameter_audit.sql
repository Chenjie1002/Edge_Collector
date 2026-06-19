CREATE TABLE IF NOT EXISTS vplc_parameter_change_log (
    change_id UUID PRIMARY KEY,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    plc_boot_id TEXT,
    station_id TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    old_value JSONB,
    new_value JSONB,
    source TEXT NOT NULL,
    actor TEXT NOT NULL,
    client_ip TEXT,
    request_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    profile TEXT NOT NULL,
    accepted BOOLEAN NOT NULL,
    rejection_reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_vplc_parameter_change_time
    ON vplc_parameter_change_log (changed_at DESC);

CREATE INDEX IF NOT EXISTS idx_vplc_parameter_change_station
    ON vplc_parameter_change_log (station_id, changed_at DESC);

CREATE TABLE IF NOT EXISTS vplc_parameter_snapshot (
    snapshot_id UUID PRIMARY KEY,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    snapshot_type TEXT NOT NULL,
    plc_boot_id TEXT,
    profile TEXT NOT NULL,
    cycle_scale DOUBLE PRECISION NOT NULL,
    config_source TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_vplc_parameter_snapshot_time
    ON vplc_parameter_snapshot (captured_at DESC);
