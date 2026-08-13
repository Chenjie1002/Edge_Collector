import { describe, expect, it } from "vitest";
import {
  FIXED_PROCESS_METRIC_NAMES,
  parseProcessMetricsResponseJson,
  parseQualityResponseJson
} from "../schema";

const fixedNames = [
  "accepted_event_count",
  "observed_accepted_event_rate",
  "accepted_unit_count",
  "quality_good_event_count",
  "quality_nok_event_count",
  "quality_denominator_event_count",
  "quality_rate",
  "station_cycle_time",
  "ideal_cycle_time",
  "line_accepted_event_count",
  "terminal_accepted_event_count",
  "performance",
  "availability",
  "full_oee"
] as const;

function qualityPayload(overrides: Record<string, unknown> = {}) {
  return {
    scope: {
      line_id: "LINE_001",
      station_id: "WS01",
      start_time: "2026-07-05T00:00:00Z",
      end_time: "2026-07-05T08:00:00Z"
    },
    counts: { ok: 1, nok: 1, denominator: 2 },
    quality_rate: 0.5,
    nok_code_distribution: { "100": 1 },
    data_sufficiency: "SUPPORTED",
    ...overrides
  };
}

type ProcessMetricFixture = {
  name: string;
  unit: string;
  counting_unit: string;
  status: string;
  reason: { code: string; detail: string };
  source: { authority: string; lineage: string; fallback: string };
  numeric_value_allowed: boolean;
  value?: unknown;
};

const processMetricMatrix: readonly ProcessMetricFixture[] = [
  {
    name: "accepted_event_count",
    unit: "events",
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "ACCEPTED_FACT_QUERY_OK", detail: "two accepted station-result facts selected" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value: 2
  },
  {
    name: "observed_accepted_event_rate",
    unit: "events_per_second",
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "CALENDAR_WINDOW_EVENT_RATE", detail: "two accepted events divided by the fixed eight-hour calendar window" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key+calendar_window", fallback: "none" },
    numeric_value_allowed: true,
    value: 2 / 28800
  },
  {
    name: "accepted_unit_count",
    unit: "units",
    counting_unit: "unit-count",
    status: "UNSUPPORTED",
    reason: { code: "UNIT_COUNTING_AUTHORITY_NOT_ACCEPTED", detail: "accepted station-result to unit identity authority is not established" },
    source: { authority: "not-accepted", lineage: "accepted unit identity authority", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "quality_good_event_count",
    unit: "events",
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "QUALITY_PREDECESSOR_SEMANTICS", detail: "one accepted ok station-result fact" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value: 1
  },
  {
    name: "quality_nok_event_count",
    unit: "events",
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "QUALITY_PREDECESSOR_SEMANTICS", detail: "one accepted nok station-result fact with complete NOK detail" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value: 1
  },
  {
    name: "quality_denominator_event_count",
    unit: "events",
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "QUALITY_PREDECESSOR_SEMANTICS", detail: "one ok plus one nok accepted fact forms the Quality denominator" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value: 2
  },
  {
    name: "quality_rate",
    unit: "ratio",
    counting_unit: "unavailable",
    status: "SUPPORTED",
    reason: { code: "QUALITY_PREDECESSOR_SEMANTICS", detail: "one good event divided by the two-event Quality denominator" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value: 0.5
  },
  {
    name: "station_cycle_time",
    unit: "seconds",
    counting_unit: "unavailable",
    status: "PARTIAL",
    reason: { code: "CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING", detail: "cycle-instance start and complete pairing authority is not accepted" },
    source: { authority: "not-accepted", lineage: "cycle-instance start/complete pairing key", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "ideal_cycle_time",
    unit: "seconds",
    counting_unit: "unavailable",
    status: "PARTIAL",
    reason: { code: "HISTORICAL_CONFIG_AUTHORITY_MISSING", detail: "historical config hash, version, and profile authority is unresolved" },
    source: { authority: "not-accepted", lineage: "historical config_hash+config_version+profile", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "line_accepted_event_count",
    unit: "events",
    counting_unit: "unavailable",
    status: "UNSUPPORTED",
    reason: { code: "LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED", detail: "station-scoped facts do not establish accepted line output authority" },
    source: { authority: "not-accepted", lineage: "accepted line-output authority", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "terminal_accepted_event_count",
    unit: "events",
    counting_unit: "unavailable",
    status: "UNSUPPORTED",
    reason: { code: "HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE", detail: "historical terminal resolution is not accepted for this station scope" },
    source: { authority: "not-accepted", lineage: "historical terminal resolution", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "performance",
    unit: "ratio",
    counting_unit: "unavailable",
    status: "UNSUPPORTED",
    reason: { code: "PERFORMANCE_AUTHORITIES_NOT_ACCEPTED", detail: "historical ideal cycle time and authoritative operating time are not accepted" },
    source: { authority: "not-accepted", lineage: "historical ideal CT+authoritative operating/run-time", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "availability",
    unit: "ratio",
    counting_unit: "unavailable",
    status: "UNSUPPORTED",
    reason: { code: "AVAILABILITY_AUTHORITIES_NOT_ACCEPTED", detail: "planned time, downtime, and run-stop timeline authority are not accepted" },
    source: { authority: "not-accepted", lineage: "planned time+downtime+run/stop timeline", fallback: "none" },
    numeric_value_allowed: false
  },
  {
    name: "full_oee",
    unit: "ratio",
    counting_unit: "unavailable",
    status: "UNSUPPORTED",
    reason: { code: "FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED", detail: "accepted Quality, Performance, and Availability components are incomplete" },
    source: { authority: "not-accepted", lineage: "accepted Quality+Performance+Availability components", fallback: "none" },
    numeric_value_allowed: false
  }
];

function cloneProcessMetricMatrix(): ProcessMetricFixture[] {
  return processMetricMatrix.map((entry) => ({
    ...entry,
    reason: { ...entry.reason },
    source: { ...entry.source }
  }));
}

function processPayload(overrides: Record<string, unknown> = {}) {
  return {
    contract_version: "P1-G3-PROCESS-KPI-1.0",
    scope: { line_id: "LINE_001", station_id: "WS01", aggregation: "station" },
    window: {
      from: "2026-07-05T00:00:00Z",
      to: "2026-07-05T08:00:00Z",
      interval: "[from,to)",
      duration_seconds: 28800
    },
    status: "PARTIAL",
    reason: { code: "ACCEPTED_FACT_QUERY_OK", detail: "accepted facts selected" },
    source: {
      authority: "production_accepted_station_event_fact",
      identity: "fact_key",
      config_window_state: "UNRESOLVED",
      fallback: "none"
    },
    metrics: cloneProcessMetricMatrix(),
    ...overrides
  };
}

describe("station summary strict schemas", () => {
  it("parses Quality counts and rejects cross-field inconsistency", () => {
    const parsed = parseQualityResponseJson(JSON.stringify(qualityPayload()));
    expect(parsed.counts.denominator).toBe(2);
    expect(parsed.data_sufficiency).toBe("SUPPORTED");
    expect(() => parseQualityResponseJson(JSON.stringify(qualityPayload({ counts: { ok: 1, nok: 1, denominator: 3 } })))).toThrow();
    expect(() => parseQualityResponseJson(JSON.stringify({ ...qualityPayload(), extra: true }))).toThrow();
  });

  it("parses the complete fixed Process Metrics matrix and rejects missing or duplicate metric keys", () => {
    const parsed = parseProcessMetricsResponseJson(JSON.stringify(processPayload()));
    expect(FIXED_PROCESS_METRIC_NAMES).toEqual(fixedNames);
    expect(parsed.metrics.map((item) => item.name)).toEqual(fixedNames);
    expect(parsed.metrics.find((item) => item.name === "full_oee")?.value).toBeUndefined();

    expect(() => parseProcessMetricsResponseJson(JSON.stringify(processPayload({ metrics: cloneProcessMetricMatrix().slice(0, -1) })))).toThrow();
    const duplicateMetrics = cloneProcessMetricMatrix();
    duplicateMetrics[duplicateMetrics.length - 1] = {
      ...duplicateMetrics[duplicateMetrics.length - 3],
      reason: { ...duplicateMetrics[duplicateMetrics.length - 3].reason },
      source: { ...duplicateMetrics[duplicateMetrics.length - 3].source }
    };
    expect(() => parseProcessMetricsResponseJson(JSON.stringify(processPayload({ metrics: duplicateMetrics })))).toThrow();
  });

  it("fails closed when a no-value metric carries null or a fallback source", () => {
    const metrics = cloneProcessMetricMatrix();
    const fullOee = metrics.find((item) => item.name === "full_oee");
    if (!fullOee) throw new Error("fixture missing full_oee");
    fullOee.value = null;
    expect(() => parseProcessMetricsResponseJson(JSON.stringify(processPayload({ metrics })))).toThrow();

    const fallbackMetrics = cloneProcessMetricMatrix();
    const performance = fallbackMetrics.find((item) => item.name === "performance");
    if (!performance) throw new Error("fixture missing performance");
    performance.source.fallback = "legacy";
    expect(() => parseProcessMetricsResponseJson(JSON.stringify(processPayload({ metrics: fallbackMetrics })))).toThrow();
  });
});
