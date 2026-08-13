import { describe, expect, it, vi } from "vitest";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../acceptedStationEvents/apiOrigin";
import { fetchStationSummary } from "../apiClient";
import { FIXED_PROCESS_METRIC_NAMES, parseProcessMetricsResponseJson } from "../schema";

const query = {
  lineId: "LINE_001",
  stationId: "WS01",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z"
};

const quality = {
  scope: { line_id: "LINE_001", station_id: "WS01", start_time: query.startTime, end_time: query.endTime },
  counts: { ok: 1, nok: 1, denominator: 2 },
  quality_rate: 0.5,
  nok_code_distribution: { "100": 1 },
  data_sufficiency: "SUPPORTED"
};

const metricNames = [
  "accepted_event_count", "observed_accepted_event_rate", "accepted_unit_count",
  "quality_good_event_count", "quality_nok_event_count", "quality_denominator_event_count",
  "quality_rate", "station_cycle_time", "ideal_cycle_time", "line_accepted_event_count",
  "terminal_accepted_event_count", "performance", "availability", "full_oee"
 ] as const;

const processMetrics = [
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

const process = {
  contract_version: "P1-G3-PROCESS-KPI-1.0",
  scope: { line_id: "LINE_001", station_id: "WS01", aggregation: "station" },
  window: { from: query.startTime, to: query.endTime, interval: "[from,to)", duration_seconds: 28800 },
  status: "PARTIAL",
  reason: { code: "ACCEPTED_FACT_QUERY_OK", detail: "fixture" },
  source: { authority: "production_accepted_station_event_fact", identity: "fact_key", config_window_state: "UNRESOLVED", fallback: "none" },
  metrics: processMetrics
};

function origin() {
  const result = resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: "https://accepted-api.example",
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production"
  });
  if (!result.ok) throw new Error("origin fixture must resolve");
  return result.origin;
}

function response(status: number, body: unknown, rawText?: string) {
  const text = vi.fn().mockResolvedValue(rawText ?? JSON.stringify(body));
  return {
    response: { ok: status >= 200 && status < 300, status, text } as unknown as Response,
    text
  };
}

describe("station summary api client", () => {
  it("uses only the trusted Quality and Process Metrics GET routes with no-store credential-free requests", async () => {
    const qualityResponse = response(200, quality);
    const processResponse = response(200, process);
    const fetchMock = vi.fn((input: RequestInfo | URL, _options?: RequestInit) => {
      const path = new URL(String(input)).pathname;
      return Promise.resolve(path.endsWith("/quality") ? qualityResponse.response : processResponse.response);
    });

    const result = await fetchStationSummary(query, origin(), fetchMock);

    const parsedProcess = parseProcessMetricsResponseJson(JSON.stringify(process));
    expect(FIXED_PROCESS_METRIC_NAMES).toEqual(metricNames);
    expect(parsedProcess.metrics.map((item) => item.name)).toEqual(FIXED_PROCESS_METRIC_NAMES);
    expect(result.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls.map(([input]) => new URL(String(input)).pathname).sort()).toEqual([
      "/api/v2/process-metrics",
      "/api/v2/production/quality"
    ]);
    for (const [, options] of fetchMock.mock.calls) {
      expect(options).toEqual({ method: "GET", cache: "no-store", credentials: "omit", redirect: "error" });
    }
    expect(qualityResponse.text).toHaveBeenCalledTimes(1);
    expect(processResponse.text).toHaveBeenCalledTimes(1);
  });

  it("keeps one source unavailable while preserving the other source as an independent success", async () => {
    const processResponse = response(200, process);
    const fetchMock = vi.fn((input: RequestInfo | URL, _options?: RequestInit) => {
      const path = new URL(String(input)).pathname;
      return Promise.resolve(path.endsWith("/quality") ? response(503, {}).response : processResponse.response);
    });

    const result = await fetchStationSummary(query, origin(), fetchMock);

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.quality).toEqual({ ok: false, kind: "unavailable", message: "Quality source unavailable." });
      expect(result.processMetrics.ok).toBe(true);
    }
  });

  it("maps a malformed 2xx body to MALFORMED without a legacy or fallback request", async () => {
    const processResponse = response(200, process);
    const fetchMock = vi.fn((input: RequestInfo | URL, _options?: RequestInit) => {
      const path = new URL(String(input)).pathname;
      return Promise.resolve(path.endsWith("/quality") ? response(200, { scope: {} }).response : processResponse.response);
    });

    const result = await fetchStationSummary(query, origin(), fetchMock);

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.quality).toEqual({ ok: false, kind: "malformed", message: "Quality response was malformed." });
      expect(result.processMetrics.ok).toBe(true);
    }
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls.every(([input]) => !String(input).match(/legacy|trace|raw|diagnostic|yaml/i))).toBe(true);
  });

  it("fails closed before either request when the query is invalid", async () => {
    const fetchMock = vi.fn();
    const result = await fetchStationSummary({ ...query, stationId: " " }, origin(), fetchMock);

    expect(result).toEqual({ ok: false, kind: "invalid-query", message: "station_id is required" });
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
