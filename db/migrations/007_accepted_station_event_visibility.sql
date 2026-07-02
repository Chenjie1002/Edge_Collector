BEGIN;

CREATE TABLE IF NOT EXISTS production_accepted_station_event_fact (
    id BIGSERIAL PRIMARY KEY,
    line_id TEXT NOT NULL,
    plc_id TEXT NOT NULL,
    station_id TEXT NOT NULL,
    station_type TEXT NOT NULL,
    profile_id TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    config_version TEXT NOT NULL,
    event_type TEXT NOT NULL,
    production_result TEXT,
    unit_id TEXT,
    dmc TEXT,
    cycle_counter BIGINT NOT NULL,
    source_event_id TEXT NOT NULL,
    event_ts TIMESTAMPTZ NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    fact_key TEXT NOT NULL,
    content_fingerprint TEXT NOT NULL,
    nok_code INTEGER,
    nok_origin TEXT,
    nok_detail_code INTEGER,
    nok_detail_source_event_id TEXT,
    nok_detail_evidence_fact_key TEXT,
    CONSTRAINT uq_production_accepted_station_event_fact_key UNIQUE (fact_key),
    CONSTRAINT uq_production_accepted_station_event_source
        UNIQUE (line_id, plc_id, station_id, config_hash, source_event_id, event_type),
    CONSTRAINT ck_production_accepted_station_event_type
        CHECK (event_type IN (
            'station_cycle_start',
            'station_cycle_complete',
            'station_result',
            'station_nok'
        )),
    CONSTRAINT ck_production_accepted_station_event_result
        CHECK (
            production_result IS NULL
            OR production_result IN ('ok', 'nok', 'skip', 'not_applicable')
        ),
    CONSTRAINT ck_production_accepted_station_result_authority
        CHECK (
            (event_type = 'station_result' AND production_result IS NOT NULL)
            OR (event_type <> 'station_result' AND production_result IS NULL)
        ),
    CONSTRAINT ck_production_accepted_station_result_nok_authority
        CHECK (
            (production_result = 'nok' AND nok_code IS NOT NULL AND nok_origin IS NOT NULL)
            OR (
                production_result IS DISTINCT FROM 'nok'
                AND event_type <> 'station_nok'
                AND nok_code IS NULL
                AND nok_origin IS NULL
            )
            OR event_type = 'station_nok'
        ),
    CONSTRAINT ck_production_accepted_station_nok_detail_authority
        CHECK (
            (
                event_type = 'station_nok'
                AND nok_code IS NOT NULL
                AND nok_origin IS NOT NULL
                AND nok_detail_code IS NOT NULL
                AND nok_detail_source_event_id IS NOT NULL
                AND nok_detail_evidence_fact_key IS NOT NULL
            )
            OR (
                event_type <> 'station_nok'
                AND nok_detail_code IS NULL
                AND nok_detail_source_event_id IS NULL
                AND nok_detail_evidence_fact_key IS NULL
            )
        )
);

CREATE INDEX IF NOT EXISTS idx_production_accepted_station_event_trace
    ON production_accepted_station_event_fact (line_id, plc_id, station_id, event_ts DESC);

CREATE INDEX IF NOT EXISTS idx_production_accepted_station_event_unit
    ON production_accepted_station_event_fact (unit_id, event_ts DESC)
    WHERE unit_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_production_accepted_station_event_dmc
    ON production_accepted_station_event_fact (dmc, event_ts DESC)
    WHERE dmc IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_production_accepted_station_event_station_result
    ON production_accepted_station_event_fact (station_id, production_result, accepted_at DESC)
    WHERE event_type = 'station_result';

CREATE INDEX IF NOT EXISTS idx_production_accepted_station_event_nok_detail
    ON production_accepted_station_event_fact (nok_detail_evidence_fact_key)
    WHERE event_type = 'station_nok';

COMMENT ON TABLE production_accepted_station_event_fact IS
    'Production-only landing surface for accepted station-event business facts. Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted. Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only. raw_payload/raw_hex is evidence, not a production fact. Decoded/source normalized payloads remain candidates until accepted. Non-accepted dispositions do not write defect detail. NOK/detail visibility must bind to accepted upstream business evidence. Non-accepted dispositions must not create rows here. Preserve exact boundary: no ACK/read_done mutation for the current non-accepted payload.';

COMMENT ON COLUMN production_accepted_station_event_fact.line_id IS 'production.line_id from immutable config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.plc_id IS 'production.plc_id from immutable config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.station_id IS 'production.station_id from immutable config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.station_type IS 'production.station_type from immutable config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.profile_id IS 'production.profile_id from immutable config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.config_hash IS 'production.config_hash used to bind historical config authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.config_version IS 'production.config_version used to bind historical config lineage.';
COMMENT ON COLUMN production_accepted_station_event_fact.event_type IS 'production.event_type for accepted production-visible station-event facts only.';
COMMENT ON COLUMN production_accepted_station_event_fact.production_result IS 'production.production_result from accepted station_result only; not adapter diagnostics.';
COMMENT ON COLUMN production_accepted_station_event_fact.unit_id IS 'production.unit_id.';
COMMENT ON COLUMN production_accepted_station_event_fact.dmc IS 'production.dmc.';
COMMENT ON COLUMN production_accepted_station_event_fact.cycle_counter IS 'production.cycle_counter from accepted business evidence.';
COMMENT ON COLUMN production_accepted_station_event_fact.source_event_id IS 'production.source_event_id from PLC/V-PLC/source stable identity.';
COMMENT ON COLUMN production_accepted_station_event_fact.event_ts IS 'production.event_ts, the source event time.';
COMMENT ON COLUMN production_accepted_station_event_fact.accepted_at IS 'production.accepted_at, the time the accepted decision becomes a production fact.';
COMMENT ON COLUMN production_accepted_station_event_fact.fact_key IS 'production.fact_key from shared canonical identity helpers.';
COMMENT ON COLUMN production_accepted_station_event_fact.content_fingerprint IS 'production.content_fingerprint from shared canonical fingerprint helpers.';
COMMENT ON COLUMN production_accepted_station_event_fact.nok_code IS 'production.nok_code; requires accepted upstream business evidence when visible.';
COMMENT ON COLUMN production_accepted_station_event_fact.nok_origin IS 'production.nok_origin; not diagnostic reason-code authority.';
COMMENT ON COLUMN production_accepted_station_event_fact.nok_detail_code IS 'production.nok_detail_code; non-accepted dispositions do not write defect detail.';
COMMENT ON COLUMN production_accepted_station_event_fact.nok_detail_source_event_id IS 'production.nok_detail_source_event_id; NOK/detail visibility must bind to accepted upstream business evidence.';
COMMENT ON COLUMN production_accepted_station_event_fact.nok_detail_evidence_fact_key IS 'production.nok_detail_evidence_fact_key; accepted upstream business evidence reference for detail visibility.';

COMMENT ON CONSTRAINT ck_production_accepted_station_event_type
    ON production_accepted_station_event_fact IS
    'Excludes diagnostic-only heartbeat and any non-accepted disposition category from production facts.';

COMMENT ON CONSTRAINT ck_production_accepted_station_result_nok_authority
    ON production_accepted_station_event_fact IS
    'NOK production outcome requires accepted business NOK evidence; adapter reason codes and raw/normalized comparison context are excluded.';

COMMENT ON CONSTRAINT ck_production_accepted_station_nok_detail_authority
    ON production_accepted_station_event_fact IS
    'Non-accepted dispositions do not write defect detail; NOK/detail visibility must bind to accepted upstream business evidence.';

COMMIT;
