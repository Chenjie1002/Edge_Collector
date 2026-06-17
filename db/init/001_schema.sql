CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT PRIMARY KEY,
    machine_name TEXT NOT NULL,
    line_name TEXT NOT NULL,
    plc_name TEXT,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS production_snapshot (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    machine_id TEXT NOT NULL REFERENCES machines(machine_id),
    running BOOLEAN NOT NULL,
    auto_mode BOOLEAN NOT NULL,
    product_type TEXT,
    shift_id TEXT,
    cycle_counter BIGINT NOT NULL,
    good_count BIGINT NOT NULL,
    ng_count BIGINT NOT NULL,
    total_count BIGINT NOT NULL,
    cycle_time_ms INTEGER,
    alarm_active BOOLEAN NOT NULL,
    alarm_code INTEGER NOT NULL DEFAULT 0,
    stop_reason_code INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_production_snapshot_machine_ts
    ON production_snapshot (machine_id, ts DESC);

CREATE TABLE IF NOT EXISTS production_events (
    event_id UUID PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    machine_id TEXT NOT NULL REFERENCES machines(machine_id),
    event_type TEXT NOT NULL,
    event_code INTEGER,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_production_events_machine_ts
    ON production_events (machine_id, ts DESC);

CREATE INDEX IF NOT EXISTS idx_production_events_type_ts
    ON production_events (event_type, ts DESC);

CREATE TABLE IF NOT EXISTS alarm_events (
    alarm_event_id UUID PRIMARY KEY,
    machine_id TEXT NOT NULL REFERENCES machines(machine_id),
    alarm_code INTEGER NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    status TEXT NOT NULL DEFAULT 'open',
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_alarm_events_machine_started
    ON alarm_events (machine_id, started_at DESC);

CREATE TABLE IF NOT EXISTS stop_events (
    stop_event_id UUID PRIMARY KEY,
    machine_id TEXT NOT NULL REFERENCES machines(machine_id),
    stop_reason_code INTEGER NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    status TEXT NOT NULL DEFAULT 'open',
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_stop_events_machine_started
    ON stop_events (machine_id, started_at DESC);

CREATE TABLE IF NOT EXISTS sync_outbox (
    id BIGSERIAL PRIMARY KEY,
    source_table TEXT NOT NULL,
    source_id TEXT NOT NULL,
    target_table TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    retry_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    synced_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_sync_outbox_status_id
    ON sync_outbox (status, id);

