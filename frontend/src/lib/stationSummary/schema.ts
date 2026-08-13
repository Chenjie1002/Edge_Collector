export const FIXED_PROCESS_METRIC_NAMES = [
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

export type FixedProcessMetricName = (typeof FIXED_PROCESS_METRIC_NAMES)[number];
export type QualityDataSufficiency = "SUPPORTED" | "PARTIAL" | "UNAVAILABLE";
export type ProcessMetricStatus = "SUPPORTED" | "PARTIAL" | "UNAVAILABLE" | "UNSUPPORTED";
export type ProcessTopStatus = ProcessMetricStatus;

type Scope = {
  line_id: string;
  station_id: string;
};

export type QualityResponse = {
  scope: Scope & { start_time: string; end_time: string };
  counts: { ok: number; nok: number; denominator: number };
  quality_rate: number | null;
  nok_code_distribution: Record<string, number>;
  data_sufficiency: QualityDataSufficiency;
};

export type ProcessMetric = {
  name: FixedProcessMetricName;
  unit: string;
  counting_unit: "event-count" | "unit-count" | "unavailable";
  status: ProcessMetricStatus;
  reason: { code: string; detail: string };
  source: { authority: "production_accepted_station_event_fact" | "not-accepted"; lineage: string; fallback: "none" };
  numeric_value_allowed: boolean;
  value?: number;
};

export type ProcessMetricsResponse = {
  contract_version: "P1-G3-PROCESS-KPI-1.0";
  scope: Scope & { aggregation: "station" };
  window: { from: string; to: string; interval: "[from,to)"; duration_seconds: number };
  status: ProcessTopStatus;
  reason: { code: string; detail: string };
  source: {
    authority: "production_accepted_station_event_fact";
    identity: "fact_key";
    config_window_state: "SINGLE_RESOLVED" | "MIXED" | "UNRESOLVED";
    fallback: "none";
  };
  metrics: ProcessMetric[];
};

const QUALITY_DATA_SUFFICIENCY = new Set<QualityDataSufficiency>(["SUPPORTED", "PARTIAL", "UNAVAILABLE"]);
const PROCESS_STATUS = new Set<ProcessMetricStatus>(["SUPPORTED", "PARTIAL", "UNAVAILABLE", "UNSUPPORTED"]);
const CONFIG_WINDOW_STATES = new Set<ProcessMetricsResponse["source"]["config_window_state"]>(["SINGLE_RESOLVED", "MIXED", "UNRESOLVED"]);
const REASON_CODES = new Set([
  "ACCEPTED_FACT_QUERY_OK",
  "CALENDAR_WINDOW_EVENT_RATE",
  "EMPTY_ACCEPTED_WINDOW",
  "QUALITY_PREDECESSOR_SEMANTICS",
  "QUALITY_NOK_DETAIL_INCOMPLETE",
  "QUALITY_DENOMINATOR_EMPTY",
  "UNIT_COUNTING_AUTHORITY_NOT_ACCEPTED",
  "FACT_IDENTITY_MISSING",
  "FACT_IDENTITY_DUPLICATE_OR_CONFLICT",
  "CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING",
  "HISTORICAL_CONFIG_AUTHORITY_MISSING",
  "MIXED_HISTORICAL_CONFIG_WINDOW",
  "LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED",
  "HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE",
  "PERFORMANCE_AUTHORITIES_NOT_ACCEPTED",
  "AVAILABILITY_AUTHORITIES_NOT_ACCEPTED",
  "FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED",
  "ACCEPTED_FACT_SOURCE_UNAVAILABLE",
  "ACCEPTED_FACT_QUERY_FAILED",
  "AUTHORITY_RESOLUTION_FAILED",
  "INVALID_REQUEST",
  "METHOD_NOT_ALLOWED",
  "BODY_NOT_ALLOWED"
]);

const METRIC_CONTRACT: Record<FixedProcessMetricName, { unit: string; counting_unit: ProcessMetric["counting_unit"] }> = {
  accepted_event_count: { unit: "events", counting_unit: "event-count" },
  observed_accepted_event_rate: { unit: "events_per_second", counting_unit: "event-count" },
  accepted_unit_count: { unit: "units", counting_unit: "unit-count" },
  quality_good_event_count: { unit: "events", counting_unit: "event-count" },
  quality_nok_event_count: { unit: "events", counting_unit: "event-count" },
  quality_denominator_event_count: { unit: "events", counting_unit: "event-count" },
  quality_rate: { unit: "ratio", counting_unit: "unavailable" },
  station_cycle_time: { unit: "seconds", counting_unit: "unavailable" },
  ideal_cycle_time: { unit: "seconds", counting_unit: "unavailable" },
  line_accepted_event_count: { unit: "events", counting_unit: "unavailable" },
  terminal_accepted_event_count: { unit: "events", counting_unit: "unavailable" },
  performance: { unit: "ratio", counting_unit: "unavailable" },
  availability: { unit: "ratio", counting_unit: "unavailable" },
  full_oee: { unit: "ratio", counting_unit: "unavailable" }
};

function assertPlainObject(value: unknown, label: string): asserts value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new Error(`${label} must be an object`);
}

function assertExactKeys(value: Record<string, unknown>, label: string, required: readonly string[], optional: readonly string[] = []) {
  const allowed = new Set([...required, ...optional]);
  for (const key of Object.keys(value)) {
    if (!allowed.has(key)) throw new Error(`forbidden ${label} key: ${key}`);
  }
  for (const key of required) {
    if (!Object.prototype.hasOwnProperty.call(value, key)) throw new Error(`missing required ${label} key: ${key}`);
  }
}

function stringValue(value: unknown, field: string): string {
  if (typeof value !== "string") throw new Error(`invalid ${field}`);
  return value;
}

function enumValue<T extends string>(value: unknown, field: string, allowed: Set<T>): T {
  if (typeof value !== "string" || !allowed.has(value as T)) throw new Error(`invalid ${field}`);
  return value as T;
}

function safeNonNegativeInteger(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0) throw new Error(`invalid ${field}`);
  return value;
}

function finiteNumber(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) throw new Error(`invalid ${field}`);
  return value;
}

function canonicalUtc(value: unknown, field: string): string {
  const timestamp = stringValue(value, field);
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$/.test(timestamp)) throw new Error(`invalid ${field}`);
  const parsed = Date.parse(timestamp);
  if (!Number.isFinite(parsed) || new Date(parsed).toISOString().replace(/\.000Z$/, "Z") !== timestamp.replace(/\.000Z$/, "Z")) {
    throw new Error(`invalid ${field}`);
  }
  return timestamp;
}

function reasonValue(value: unknown, field: string): { code: string; detail: string } {
  assertPlainObject(value, field);
  assertExactKeys(value, field, ["code", "detail"]);
  const code = stringValue(value.code, `${field}.code`);
  if (!REASON_CODES.has(code)) throw new Error(`invalid ${field}.code`);
  return { code, detail: stringValue(value.detail, `${field}.detail`) };
}

function qualityScope(value: unknown): QualityResponse["scope"] {
  assertPlainObject(value, "quality scope");
  assertExactKeys(value, "quality scope", ["line_id", "station_id", "start_time", "end_time"]);
  return {
    line_id: stringValue(value.line_id, "quality scope.line_id"),
    station_id: stringValue(value.station_id, "quality scope.station_id"),
    start_time: canonicalUtc(value.start_time, "quality scope.start_time"),
    end_time: canonicalUtc(value.end_time, "quality scope.end_time")
  };
}

export function parseQualityResponse(value: unknown): QualityResponse {
  assertPlainObject(value, "Quality response");
  assertExactKeys(value, "Quality response", ["scope", "counts", "quality_rate", "nok_code_distribution", "data_sufficiency"]);
  const scope = qualityScope(value.scope);
  assertPlainObject(value.counts, "Quality counts");
  assertExactKeys(value.counts, "Quality counts", ["ok", "nok", "denominator"]);
  const counts = {
    ok: safeNonNegativeInteger(value.counts.ok, "Quality counts.ok"),
    nok: safeNonNegativeInteger(value.counts.nok, "Quality counts.nok"),
    denominator: safeNonNegativeInteger(value.counts.denominator, "Quality counts.denominator")
  };
  if (counts.denominator !== counts.ok + counts.nok) throw new Error("invalid Quality counts cross-field relationship");

  const qualityRate = value.quality_rate === null ? null : finiteNumber(value.quality_rate, "quality_rate");
  if (qualityRate !== null && (qualityRate < 0 || qualityRate > 1)) throw new Error("invalid quality_rate");
  if (counts.denominator === 0 && qualityRate !== null) throw new Error("invalid empty Quality rate");

  assertPlainObject(value.nok_code_distribution, "nok_code_distribution");
  const distribution: Record<string, number> = {};
  for (const [key, item] of Object.entries(value.nok_code_distribution)) {
    distribution[key] = safeNonNegativeInteger(item, `nok_code_distribution.${key}`);
  }

  const dataSufficiency = enumValue(value.data_sufficiency, "data_sufficiency", QUALITY_DATA_SUFFICIENCY);
  if (counts.denominator === 0 && dataSufficiency !== "UNAVAILABLE") throw new Error("invalid empty Quality sufficiency");
  return { scope, counts, quality_rate: qualityRate, nok_code_distribution: distribution, data_sufficiency: dataSufficiency };
}

function processSource(value: unknown, field: string): ProcessMetric["source"] {
  assertPlainObject(value, field);
  assertExactKeys(value, field, ["authority", "lineage", "fallback"]);
  const authority = enumValue(value.authority, `${field}.authority`, new Set(["production_accepted_station_event_fact", "not-accepted"] as const));
  const fallback = stringValue(value.fallback, `${field}.fallback`);
  if (fallback !== "none") throw new Error(`invalid ${field}.fallback`);
  return { authority, lineage: stringValue(value.lineage, `${field}.lineage`), fallback: "none" };
}

function metricStatusFor(name: FixedProcessMetricName, value: unknown): ProcessMetricStatus {
  const status = enumValue(value, `metric ${name}.status`, PROCESS_STATUS);
  if (name === "accepted_unit_count" || name === "line_accepted_event_count" || name === "terminal_accepted_event_count" || name === "performance" || name === "availability" || name === "full_oee") {
    if (status !== "UNSUPPORTED") throw new Error(`invalid metric ${name}.status`);
  }
  if (name === "station_cycle_time" || name === "ideal_cycle_time") {
    if (status !== "PARTIAL") throw new Error(`invalid metric ${name}.status`);
  }
  return status;
}

function processMetric(value: unknown): ProcessMetric {
  assertPlainObject(value, "Process metric");
  const name = enumValue(value.name, "metric.name", new Set(FIXED_PROCESS_METRIC_NAMES));
  const contract = METRIC_CONTRACT[name];
  const numericValueAllowed = value.numeric_value_allowed;
  if (typeof numericValueAllowed !== "boolean") throw new Error(`invalid metric ${name}.numeric_value_allowed`);
  assertExactKeys(value, `metric ${name}`, ["name", "unit", "counting_unit", "status", "reason", "source", "numeric_value_allowed"], numericValueAllowed ? ["value"] : []);
  if (stringValue(value.unit, `metric ${name}.unit`) !== contract.unit) throw new Error(`invalid metric ${name}.unit`);
  if (stringValue(value.counting_unit, `metric ${name}.counting_unit`) !== contract.counting_unit) throw new Error(`invalid metric ${name}.counting_unit`);
  const status = metricStatusFor(name, value.status);
  const reason = reasonValue(value.reason, `metric ${name}.reason`);
  const source = processSource(value.source, `metric ${name}.source`);
  if (numericValueAllowed) {
    if (!Object.prototype.hasOwnProperty.call(value, "value")) throw new Error(`missing metric ${name}.value`);
    if (status !== "SUPPORTED" && !(name === "quality_rate" && status === "PARTIAL")) throw new Error(`invalid numeric metric ${name}.status`);
    if (source.authority !== "production_accepted_station_event_fact") throw new Error(`invalid numeric metric ${name}.source`);
    return { name, unit: contract.unit, counting_unit: contract.counting_unit, status, reason, source, numeric_value_allowed: true, value: finiteNumber(value.value, `metric ${name}.value`) };
  }
  if (Object.prototype.hasOwnProperty.call(value, "value")) throw new Error(`forbidden metric ${name}.value`);
  if (status === "SUPPORTED") throw new Error(`supported metric ${name} must carry a numeric value`);
  if ((status === "UNSUPPORTED" || status === "PARTIAL") && source.authority !== "not-accepted" && name !== "quality_rate") {
    throw new Error(`invalid non-numeric metric ${name}.source`);
  }
  return { name, unit: contract.unit, counting_unit: contract.counting_unit, status, reason, source, numeric_value_allowed: false };
}

function processScope(value: unknown): ProcessMetricsResponse["scope"] {
  assertPlainObject(value, "Process scope");
  assertExactKeys(value, "Process scope", ["line_id", "station_id", "aggregation"]);
  if (value.aggregation !== "station") throw new Error("invalid Process scope.aggregation");
  return { line_id: stringValue(value.line_id, "Process scope.line_id"), station_id: stringValue(value.station_id, "Process scope.station_id"), aggregation: "station" };
}

function processWindow(value: unknown): ProcessMetricsResponse["window"] {
  assertPlainObject(value, "Process window");
  assertExactKeys(value, "Process window", ["from", "to", "interval", "duration_seconds"]);
  const from = canonicalUtc(value.from, "Process window.from");
  const to = canonicalUtc(value.to, "Process window.to");
  if (value.interval !== "[from,to)") throw new Error("invalid Process window.interval");
  const duration = finiteNumber(value.duration_seconds, "Process window.duration_seconds");
  if (duration <= 0 || Date.parse(to) - Date.parse(from) !== duration * 1000) throw new Error("invalid Process window duration");
  return { from, to, interval: "[from,to)", duration_seconds: duration };
}

function processSourceTop(value: unknown): ProcessMetricsResponse["source"] {
  assertPlainObject(value, "Process source");
  assertExactKeys(value, "Process source", ["authority", "identity", "config_window_state", "fallback"]);
  if (value.authority !== "production_accepted_station_event_fact" || value.identity !== "fact_key" || value.fallback !== "none") throw new Error("invalid Process source");
  return {
    authority: "production_accepted_station_event_fact",
    identity: "fact_key",
    config_window_state: enumValue(value.config_window_state, "Process source.config_window_state", CONFIG_WINDOW_STATES),
    fallback: "none"
  };
}

export function parseProcessMetricsResponse(value: unknown): ProcessMetricsResponse {
  assertPlainObject(value, "Process Metrics response");
  assertExactKeys(value, "Process Metrics response", ["contract_version", "scope", "window", "status", "reason", "source", "metrics"]);
  if (value.contract_version !== "P1-G3-PROCESS-KPI-1.0") throw new Error("invalid Process contract_version");
  const scope = processScope(value.scope);
  const window = processWindow(value.window);
  const status = enumValue(value.status, "Process status", PROCESS_STATUS);
  const reason = reasonValue(value.reason, "Process reason");
  const source = processSourceTop(value.source);
  if (!Array.isArray(value.metrics) || value.metrics.length !== FIXED_PROCESS_METRIC_NAMES.length) throw new Error("invalid Process metrics length");
  const seen = new Set<string>();
  const metrics = value.metrics.map((item) => {
    const parsed = processMetric(item);
    if (seen.has(parsed.name)) throw new Error("duplicate Process metric name");
    seen.add(parsed.name);
    return parsed;
  });
  if (seen.size !== FIXED_PROCESS_METRIC_NAMES.length || FIXED_PROCESS_METRIC_NAMES.some((name) => !seen.has(name))) throw new Error("missing Process metric name");
  if (status === "UNAVAILABLE" && metrics.some((metric) => metric.numeric_value_allowed)) throw new Error("unavailable Process response has numeric value");
  if (status === "UNSUPPORTED" && metrics.some((metric) => metric.numeric_value_allowed || metric.status !== "UNSUPPORTED")) throw new Error("invalid unsupported Process response");
  if (status === "SUPPORTED" && metrics.some((metric) => metric.status !== "SUPPORTED")) throw new Error("invalid supported Process response");
  return { contract_version: "P1-G3-PROCESS-KPI-1.0", scope, window, status, reason, source, metrics };
}

function parseJson(rawText: string): unknown {
  try {
    return JSON.parse(rawText) as unknown;
  } catch {
    throw new Error("malformed station summary response");
  }
}

export function parseQualityResponseJson(rawText: string): QualityResponse {
  return parseQualityResponse(parseJson(rawText));
}

export function parseProcessMetricsResponseJson(rawText: string): ProcessMetricsResponse {
  return parseProcessMetricsResponse(parseJson(rawText));
}
