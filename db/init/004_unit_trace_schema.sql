ALTER TABLE cycle_event
    ADD COLUMN IF NOT EXISTS unit_id TEXT,
    ADD COLUMN IF NOT EXISTS route_step INTEGER,
    ADD COLUMN IF NOT EXISTS route_state TEXT,
    ADD COLUMN IF NOT EXISTS process_status TEXT,
    ADD COLUMN IF NOT EXISTS skip_reason TEXT,
    ADD COLUMN IF NOT EXISTS defect_origin_station TEXT,
    ADD COLUMN IF NOT EXISTS defect_code INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS final_label_code TEXT,
    ADD COLUMN IF NOT EXISTS reject_id TEXT;

CREATE INDEX IF NOT EXISTS idx_cycle_event_unit_id
    ON cycle_event (unit_id);

CREATE INDEX IF NOT EXISTS idx_cycle_event_process_status
    ON cycle_event (process_status);

CREATE INDEX IF NOT EXISTS idx_cycle_event_reject_id
    ON cycle_event (reject_id);

CREATE TABLE IF NOT EXISTS production_unit (
    unit_id TEXT PRIMARY KEY,
    line_id TEXT NOT NULL,
    plc_id TEXT NOT NULL,
    child_dmc TEXT,
    final_label_code TEXT,
    reject_id TEXT,
    current_station_id TEXT,
    current_route_step INTEGER,
    current_state TEXT NOT NULL DEFAULT 'CREATED',
    final_result TEXT,
    disposition TEXT,
    defect_origin_station TEXT,
    defect_code INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_production_unit_state_updated
    ON production_unit (current_state, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_production_unit_final_label
    ON production_unit (final_label_code);

CREATE INDEX IF NOT EXISTS idx_production_unit_reject_id
    ON production_unit (reject_id);

CREATE TABLE IF NOT EXISTS station_event (
    id BIGSERIAL PRIMARY KEY,
    cycle_event_id BIGINT REFERENCES cycle_event(id) ON DELETE CASCADE,
    unit_id TEXT NOT NULL,
    plc_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    route_step INTEGER,
    process_status TEXT NOT NULL,
    result TEXT NOT NULL,
    skip_reason TEXT,
    defect_origin_station TEXT,
    defect_code INTEGER NOT NULL DEFAULT 0,
    nok_codes INTEGER[] NOT NULL DEFAULT ARRAY[]::INTEGER[],
    station_dmc TEXT,
    child_dmc TEXT,
    final_label_code TEXT,
    reject_id TEXT,
    plc_start_time TIMESTAMPTZ,
    plc_end_time TIMESTAMPTZ,
    cycle_time_ms INTEGER,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    raw_sample_id BIGINT REFERENCES raw_plc_sample(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_station_event_cycle_event UNIQUE (cycle_event_id)
);

CREATE INDEX IF NOT EXISTS idx_station_event_unit_route
    ON station_event (unit_id, route_step, plc_end_time);

CREATE INDEX IF NOT EXISTS idx_station_event_station_time
    ON station_event (station_id, plc_end_time DESC);

CREATE TABLE IF NOT EXISTS unit_state_history (
    id BIGSERIAL PRIMARY KEY,
    unit_id TEXT NOT NULL,
    station_event_id BIGINT REFERENCES station_event(id) ON DELETE CASCADE,
    state TEXT NOT NULL,
    station_id TEXT,
    route_step INTEGER,
    note TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_unit_state_history_unit_time
    ON unit_state_history (unit_id, created_at);
