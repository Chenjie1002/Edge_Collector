export type LineSummaryReconciliationStatus = "PASS" | "FAIL";

export type LineSummaryTrendPoint = Readonly<{
  bucketStart: string;
  completed: number;
  ok: number;
  nok: number;
}>;

export type StationProductionTrendPoint = Readonly<{
  bucketStart: string;
  stationId: string;
  completed: number;
  ok: number;
  nok: number;
}>;

export type CycleTimeTrendPoint = Readonly<{
  bucketStart: string;
  stationId: string;
  averageCycleSeconds: number;
  samples: number;
}>;

export type StationActivityPoint = Readonly<{
  bucketStart: string;
  processed: number;
  skipped: number;
  newNok: number;
}>;

export type StationRecentRecord = Readonly<{
  unitId: string;
  result: string;
  processStatus: string;
  completedAt: string;
  cycleSeconds: number | null;
  defectCode: number | null;
}>;

export type LineSummaryStation = Readonly<{
  stationId: string;
  total: number;
  ok: number;
  nok: number;
  newNok: number;
  skipped: number;
  processed: number;
  reconciliationStatus: LineSummaryReconciliationStatus;
  evidenceCount: number;
  missingUnitCount: number;
  duplicateUnitCount: number;
  invalidRecordCount: number;
  resultCompatibility: string;
  averageCycleSeconds?: number | null;
  localNokRate?: number | null;
  activityTrend?: readonly StationActivityPoint[];
  nokCodes?: readonly Readonly<{ code: number; count: number }>[];
  recentRecords?: readonly StationRecentRecord[];
}>;

export type LineSummaryLine = Readonly<{
  lineId: string;
  name: string;
  stationCount: number;
  route: readonly string[];
  entryStationId: string;
  terminalStationId: string;
  activeProfile: string;
  collectorState: string;
  collectorConnectedStations: number;
  runtimeStatus: string;
  runtimeAuthority: string;
  mappingContentSha256: string | null;
  configVersion: string | null;
}>;

export type LineSummaryOverview = Readonly<{
  completedUnits: number;
  finalOk: number;
  finalNok: number;
  finalYield: number | null;
  ackPendingEvents: number;
  averageCycleSeconds: number | null;
  routeConservation: LineSummaryReconciliationStatus;
}>;

export type CollectorRuntimeStation = Readonly<{
  stationId: string;
  collectorState: string;
  plcConnectionState: string;
  stationStatus: string;
  updatedAt: string;
}>;

export type RecentCompletedUnit = Readonly<{
  unitId: string;
  result: string;
  completedAt: string;
  defectOriginStation: string | null;
  defectCode: number | null;
  labelCode: string | null;
  rejectId: string | null;
}>;

export type LineSummary = Readonly<{
  contractVersion: "production-line-summary/v1";
  scope: Readonly<{
    lineId: string;
    startTime: string;
    endTime: string;
    cohortBasis: "terminal_completed";
  }>;
  topology: Readonly<{
    entryStationId: string;
    terminalStationId: string;
    stations: readonly string[];
  }>;
  cohort: Readonly<{
    unitCount: number;
    reconciliationStatus: LineSummaryReconciliationStatus;
    errors: readonly string[];
  }>;
  stations: readonly LineSummaryStation[];
  line?: LineSummaryLine;
  overview?: LineSummaryOverview;
  trends?: Readonly<{
    production: readonly LineSummaryTrendPoint[];
    productionByStation?: readonly StationProductionTrendPoint[];
    cycleTime: readonly CycleTimeTrendPoint[];
  }>;
  quality?: Readonly<{
    nokAccumulation: readonly Readonly<{ stationId: string; count: number }>[];
    newNokByStation: readonly Readonly<{ stationId: string; count: number }>[];
    nokCodeDistribution: readonly Readonly<{ code: number; count: number }>[];
  }>;
  collectorRuntime?: readonly CollectorRuntimeStation[];
  recentCompletedUnits?: readonly RecentCompletedUnit[];
}>;

type JsonObject = Record<string, unknown>;

function isPlainObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function exactKeys(value: JsonObject, required: readonly string[], label: string, optional: readonly string[] = []): void {
  const allowed = new Set([...required, ...optional]);
  if (Object.keys(value).some((key) => !allowed.has(key)) || required.some((key) => !Object.prototype.hasOwnProperty.call(value, key))) {
    throw new Error(`invalid ${label}`);
  }
}

function nonBlankString(value: unknown, label: string): string {
  if (typeof value !== "string" || value.trim() === "") throw new Error(`invalid ${label}`);
  return value;
}

function nullableString(value: unknown, label: string): string | null {
  if (value === null) return null;
  return nonBlankString(value, label);
}

function nonNegativeSafeInteger(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0) throw new Error(`invalid ${label}`);
  return value;
}

function nonNegativeNumber(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0) throw new Error(`invalid ${label}`);
  return value;
}

function nullableNonNegativeNumber(value: unknown, label: string): number | null {
  if (value === null) return null;
  return nonNegativeNumber(value, label);
}

function nullablePositiveInteger(value: unknown, label: string): number | null {
  if (value === null) return null;
  const parsed = nonNegativeSafeInteger(value, label);
  if (parsed <= 0) throw new Error(`invalid ${label}`);
  return parsed;
}

function reconciliationStatus(value: unknown, label: string): LineSummaryReconciliationStatus {
  if (value !== "PASS" && value !== "FAIL") throw new Error(`invalid ${label}`);
  return value;
}

function parseCountSeries(value: unknown, label: string): readonly Readonly<{ stationId: string; count: number }>[] {
  if (!Array.isArray(value)) throw new Error(`invalid ${label}`);
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid ${label} ${index}`);
    exactKeys(entry, ["station_id", "count"], `${label} ${index}`);
    return {
      stationId: nonBlankString(entry.station_id, `${label} ${index}.station_id`),
      count: nonNegativeSafeInteger(entry.count, `${label} ${index}.count`),
    };
  });
}

function parseNokCodes(value: unknown, label: string): readonly Readonly<{ code: number; count: number }>[] {
  if (!Array.isArray(value)) throw new Error(`invalid ${label}`);
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid ${label} ${index}`);
    exactKeys(entry, ["code", "count"], `${label} ${index}`);
    return {
      code: nonNegativeSafeInteger(entry.code, `${label} ${index}.code`),
      count: nonNegativeSafeInteger(entry.count, `${label} ${index}.count`),
    };
  });
}

function parseStationActivity(value: unknown, label: string): readonly StationActivityPoint[] {
  if (!Array.isArray(value)) throw new Error(`invalid ${label}`);
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid ${label} ${index}`);
    exactKeys(entry, ["bucket_start", "processed", "skipped", "new_nok"], `${label} ${index}`);
    return {
      bucketStart: nonBlankString(entry.bucket_start, `${label} ${index}.bucket_start`),
      processed: nonNegativeSafeInteger(entry.processed, `${label} ${index}.processed`),
      skipped: nonNegativeSafeInteger(entry.skipped, `${label} ${index}.skipped`),
      newNok: nonNegativeSafeInteger(entry.new_nok, `${label} ${index}.new_nok`),
    };
  });
}

function parseStationRecent(value: unknown, label: string): readonly StationRecentRecord[] {
  if (!Array.isArray(value)) throw new Error(`invalid ${label}`);
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid ${label} ${index}`);
    exactKeys(entry, ["unit_id", "result", "process_status", "completed_at", "cycle_seconds", "defect_code"], `${label} ${index}`);
    return {
      unitId: nonBlankString(entry.unit_id, `${label} ${index}.unit_id`),
      result: nonBlankString(entry.result, `${label} ${index}.result`),
      processStatus: nonBlankString(entry.process_status, `${label} ${index}.process_status`),
      completedAt: nonBlankString(entry.completed_at, `${label} ${index}.completed_at`),
      cycleSeconds: nullableNonNegativeNumber(entry.cycle_seconds, `${label} ${index}.cycle_seconds`),
      defectCode: nullablePositiveInteger(entry.defect_code, `${label} ${index}.defect_code`),
    };
  });
}

function stationSummary(value: unknown, index: number): LineSummaryStation {
  if (!isPlainObject(value)) throw new Error(`invalid station summary ${index}`);
  exactKeys(
    value,
    [
      "station_id",
      "total",
      "ok",
      "nok",
      "new_nok",
      "skipped",
      "processed",
      "reconciliation_status",
      "evidence_count",
      "missing_unit_count",
      "duplicate_unit_count",
      "invalid_record_count",
      "result_compatibility",
    ],
    `station summary ${index}`,
    ["average_cycle_seconds", "local_nok_rate", "activity_trend", "nok_codes", "recent_records"],
  );
  const total = nonNegativeSafeInteger(value.total, `station summary ${index}.total`);
  const ok = nonNegativeSafeInteger(value.ok, `station summary ${index}.ok`);
  const nok = nonNegativeSafeInteger(value.nok, `station summary ${index}.nok`);
  const newNok = nonNegativeSafeInteger(value.new_nok, `station summary ${index}.new_nok`);
  const skipped = nonNegativeSafeInteger(value.skipped, `station summary ${index}.skipped`);
  const processed = nonNegativeSafeInteger(value.processed, `station summary ${index}.processed`);
  if (ok > total || nok > total || newNok > nok || skipped > total || processed > total) {
    throw new Error(`invalid station summary ${index} counts`);
  }
  const base: LineSummaryStation = {
    stationId: nonBlankString(value.station_id, `station summary ${index}.station_id`),
    total,
    ok,
    nok,
    newNok,
    skipped,
    processed,
    reconciliationStatus: reconciliationStatus(value.reconciliation_status, `station summary ${index}.reconciliation_status`),
    evidenceCount: nonNegativeSafeInteger(value.evidence_count, `station summary ${index}.evidence_count`),
    missingUnitCount: nonNegativeSafeInteger(value.missing_unit_count, `station summary ${index}.missing_unit_count`),
    duplicateUnitCount: nonNegativeSafeInteger(value.duplicate_unit_count, `station summary ${index}.duplicate_unit_count`),
    invalidRecordCount: nonNegativeSafeInteger(value.invalid_record_count, `station summary ${index}.invalid_record_count`),
    resultCompatibility: nonBlankString(value.result_compatibility, `station summary ${index}.result_compatibility`),
  };
  return {
    ...base,
    ...(Object.prototype.hasOwnProperty.call(value, "average_cycle_seconds")
      ? { averageCycleSeconds: nullableNonNegativeNumber(value.average_cycle_seconds, `station summary ${index}.average_cycle_seconds`) }
      : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "local_nok_rate")
      ? { localNokRate: nullableNonNegativeNumber(value.local_nok_rate, `station summary ${index}.local_nok_rate`) }
      : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "activity_trend")
      ? { activityTrend: parseStationActivity(value.activity_trend, `station summary ${index}.activity_trend`) }
      : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "nok_codes")
      ? { nokCodes: parseNokCodes(value.nok_codes, `station summary ${index}.nok_codes`) }
      : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "recent_records")
      ? { recentRecords: parseStationRecent(value.recent_records, `station summary ${index}.recent_records`) }
      : {}),
  };
}

function parseLine(value: unknown): LineSummaryLine {
  if (!isPlainObject(value)) throw new Error("invalid line summary line");
  exactKeys(value, ["line_id", "name", "station_count", "route", "entry_station_id", "terminal_station_id", "active_profile", "collector_state", "collector_connected_stations", "runtime_status", "runtime_authority", "mapping_content_sha256", "config_version"], "line summary line");
  if (!Array.isArray(value.route)) throw new Error("invalid line summary line.route");
  return {
    lineId: nonBlankString(value.line_id, "line summary line.line_id"),
    name: nonBlankString(value.name, "line summary line.name"),
    stationCount: nonNegativeSafeInteger(value.station_count, "line summary line.station_count"),
    route: value.route.map((entry, index) => nonBlankString(entry, `line summary line.route ${index}`)),
    entryStationId: nonBlankString(value.entry_station_id, "line summary line.entry_station_id"),
    terminalStationId: nonBlankString(value.terminal_station_id, "line summary line.terminal_station_id"),
    activeProfile: nonBlankString(value.active_profile, "line summary line.active_profile"),
    collectorState: nonBlankString(value.collector_state, "line summary line.collector_state"),
    collectorConnectedStations: nonNegativeSafeInteger(value.collector_connected_stations, "line summary line.collector_connected_stations"),
    runtimeStatus: nonBlankString(value.runtime_status, "line summary line.runtime_status"),
    runtimeAuthority: nonBlankString(value.runtime_authority, "line summary line.runtime_authority"),
    mappingContentSha256: nullableString(value.mapping_content_sha256, "line summary line.mapping_content_sha256"),
    configVersion: nullableString(value.config_version, "line summary line.config_version"),
  };
}

function parseOverview(value: unknown): LineSummaryOverview {
  if (!isPlainObject(value)) throw new Error("invalid line summary overview");
  exactKeys(value, ["completed_units", "final_ok", "final_nok", "final_yield", "ack_pending_events", "average_cycle_seconds", "route_conservation"], "line summary overview");
  const finalYield = nullableNonNegativeNumber(value.final_yield, "line summary overview.final_yield");
  if (finalYield !== null && finalYield > 1) throw new Error("invalid line summary overview.final_yield");
  return {
    completedUnits: nonNegativeSafeInteger(value.completed_units, "line summary overview.completed_units"),
    finalOk: nonNegativeSafeInteger(value.final_ok, "line summary overview.final_ok"),
    finalNok: nonNegativeSafeInteger(value.final_nok, "line summary overview.final_nok"),
    finalYield,
    ackPendingEvents: nonNegativeSafeInteger(value.ack_pending_events, "line summary overview.ack_pending_events"),
    averageCycleSeconds: nullableNonNegativeNumber(value.average_cycle_seconds, "line summary overview.average_cycle_seconds"),
    routeConservation: reconciliationStatus(value.route_conservation, "line summary overview.route_conservation"),
  };
}

function parseTrends(value: unknown): NonNullable<LineSummary["trends"]> {
  if (!isPlainObject(value)) throw new Error("invalid line summary trends");
  exactKeys(value, ["production", "cycle_time"], "line summary trends", ["production_by_station"]);
  if (!Array.isArray(value.production) || !Array.isArray(value.cycle_time)) throw new Error("invalid line summary trends");
  const productionByStation = value.production_by_station === undefined
    ? undefined
    : (() => {
      if (!Array.isArray(value.production_by_station)) throw new Error("invalid station production trend");
      return value.production_by_station.map((entry, index) => {
        if (!isPlainObject(entry)) throw new Error(`invalid station production trend ${index}`);
        exactKeys(entry, ["bucket_start", "station_id", "completed", "ok", "nok"], `station production trend ${index}`);
        const completed = nonNegativeSafeInteger(entry.completed, `station production trend ${index}.completed`);
        const ok = nonNegativeSafeInteger(entry.ok, `station production trend ${index}.ok`);
        const nok = nonNegativeSafeInteger(entry.nok, `station production trend ${index}.nok`);
        if (ok + nok !== completed) throw new Error(`invalid station production trend ${index} counts`);
        return {
          bucketStart: nonBlankString(entry.bucket_start, `station production trend ${index}.bucket_start`),
          stationId: nonBlankString(entry.station_id, `station production trend ${index}.station_id`),
          completed,
          ok,
          nok,
        };
      });
    })();
  return {
    production: value.production.map((entry, index) => {
      if (!isPlainObject(entry)) throw new Error(`invalid production trend ${index}`);
      exactKeys(entry, ["bucket_start", "completed", "ok", "nok"], `production trend ${index}`);
      return {
        bucketStart: nonBlankString(entry.bucket_start, `production trend ${index}.bucket_start`),
        completed: nonNegativeSafeInteger(entry.completed, `production trend ${index}.completed`),
        ok: nonNegativeSafeInteger(entry.ok, `production trend ${index}.ok`),
        nok: nonNegativeSafeInteger(entry.nok, `production trend ${index}.nok`),
      };
    }),
    ...(productionByStation ? { productionByStation } : {}),
    cycleTime: value.cycle_time.map((entry, index) => {
      if (!isPlainObject(entry)) throw new Error(`invalid cycle trend ${index}`);
      exactKeys(entry, ["bucket_start", "station_id", "average_cycle_seconds", "samples"], `cycle trend ${index}`);
      return {
        bucketStart: nonBlankString(entry.bucket_start, `cycle trend ${index}.bucket_start`),
        stationId: nonBlankString(entry.station_id, `cycle trend ${index}.station_id`),
        averageCycleSeconds: nonNegativeNumber(entry.average_cycle_seconds, `cycle trend ${index}.average_cycle_seconds`),
        samples: nonNegativeSafeInteger(entry.samples, `cycle trend ${index}.samples`),
      };
    }),
  };
}

function parseQuality(value: unknown): NonNullable<LineSummary["quality"]> {
  if (!isPlainObject(value)) throw new Error("invalid line summary quality");
  exactKeys(value, ["nok_accumulation", "new_nok_by_station", "nok_code_distribution"], "line summary quality");
  return {
    nokAccumulation: parseCountSeries(value.nok_accumulation, "nok accumulation"),
    newNokByStation: parseCountSeries(value.new_nok_by_station, "new nok by station"),
    nokCodeDistribution: parseNokCodes(value.nok_code_distribution, "nok code distribution"),
  };
}

function parseCollectorRuntime(value: unknown): readonly CollectorRuntimeStation[] {
  if (!Array.isArray(value)) throw new Error("invalid collector runtime");
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid collector runtime ${index}`);
    exactKeys(entry, ["station_id", "collector_state", "plc_connection_state", "station_status", "updated_at"], `collector runtime ${index}`);
    return {
      stationId: nonBlankString(entry.station_id, `collector runtime ${index}.station_id`),
      collectorState: nonBlankString(entry.collector_state, `collector runtime ${index}.collector_state`),
      plcConnectionState: nonBlankString(entry.plc_connection_state, `collector runtime ${index}.plc_connection_state`),
      stationStatus: nonBlankString(entry.station_status, `collector runtime ${index}.station_status`),
      updatedAt: nonBlankString(entry.updated_at, `collector runtime ${index}.updated_at`),
    };
  });
}

function parseRecentCompleted(value: unknown): readonly RecentCompletedUnit[] {
  if (!Array.isArray(value)) throw new Error("invalid recent completed units");
  return value.map((entry, index) => {
    if (!isPlainObject(entry)) throw new Error(`invalid recent completed unit ${index}`);
    exactKeys(entry, ["unit_id", "result", "completed_at", "defect_origin_station", "defect_code", "label_code", "reject_id"], `recent completed unit ${index}`);
    return {
      unitId: nonBlankString(entry.unit_id, `recent completed unit ${index}.unit_id`),
      result: nonBlankString(entry.result, `recent completed unit ${index}.result`),
      completedAt: nonBlankString(entry.completed_at, `recent completed unit ${index}.completed_at`),
      defectOriginStation: nullableString(entry.defect_origin_station, `recent completed unit ${index}.defect_origin_station`),
      defectCode: nullablePositiveInteger(entry.defect_code, `recent completed unit ${index}.defect_code`),
      labelCode: nullableString(entry.label_code, `recent completed unit ${index}.label_code`),
      rejectId: nullableString(entry.reject_id, `recent completed unit ${index}.reject_id`),
    };
  });
}

export function parseLineSummaryResponse(value: unknown): LineSummary {
  if (!isPlainObject(value)) throw new Error("invalid line summary response");
  exactKeys(
    value,
    ["contract_version", "scope", "topology", "cohort", "stations"],
    "line summary response",
    ["line", "overview", "trends", "quality", "collector_runtime", "recent_completed_units"],
  );
  if (value.contract_version !== "production-line-summary/v1") throw new Error("invalid line summary contract_version");

  if (!isPlainObject(value.scope)) throw new Error("invalid line summary scope");
  exactKeys(value.scope, ["line_id", "start_time", "end_time", "cohort_basis"], "line summary scope");
  if (value.scope.cohort_basis !== "terminal_completed") throw new Error("invalid line summary cohort_basis");
  const scope = {
    lineId: nonBlankString(value.scope.line_id, "line summary scope.line_id"),
    startTime: nonBlankString(value.scope.start_time, "line summary scope.start_time"),
    endTime: nonBlankString(value.scope.end_time, "line summary scope.end_time"),
    cohortBasis: "terminal_completed" as const,
  };

  if (!isPlainObject(value.topology)) throw new Error("invalid line summary topology");
  exactKeys(value.topology, ["entry_station_id", "terminal_station_id", "stations"], "line summary topology");
  if (!Array.isArray(value.topology.stations) || value.topology.stations.length === 0) throw new Error("invalid line summary topology stations");
  const stations = value.topology.stations.map((station, index) => nonBlankString(station, `line summary topology station ${index}`));
  if (new Set(stations).size !== stations.length) throw new Error("duplicate line summary topology station");
  const topology = {
    entryStationId: nonBlankString(value.topology.entry_station_id, "line summary topology.entry_station_id"),
    terminalStationId: nonBlankString(value.topology.terminal_station_id, "line summary topology.terminal_station_id"),
    stations,
  };
  if (!stations.includes(topology.entryStationId) || !stations.includes(topology.terminalStationId)) {
    throw new Error("line summary topology endpoints are not configured stations");
  }

  if (!isPlainObject(value.cohort)) throw new Error("invalid line summary cohort");
  exactKeys(value.cohort, ["unit_count", "reconciliation_status", "errors"], "line summary cohort");
  if (!Array.isArray(value.cohort.errors)) throw new Error("invalid line summary cohort errors");
  const errors = value.cohort.errors.map((error, index) => nonBlankString(error, `line summary cohort error ${index}`));
  const cohort = {
    unitCount: nonNegativeSafeInteger(value.cohort.unit_count, "line summary cohort.unit_count"),
    reconciliationStatus: reconciliationStatus(value.cohort.reconciliation_status, "line summary cohort.reconciliation_status"),
    errors,
  };

  if (!Array.isArray(value.stations) || value.stations.length !== stations.length) throw new Error("invalid line summary stations");
  const stationSummaries = value.stations.map(stationSummary);
  if (stationSummaries.some((station, index) => station.stationId !== stations[index])) {
    throw new Error("line summary station order does not match topology");
  }

  return {
    contractVersion: "production-line-summary/v1",
    scope,
    topology,
    cohort,
    stations: stationSummaries,
    ...(Object.prototype.hasOwnProperty.call(value, "line") ? { line: parseLine(value.line) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "overview") ? { overview: parseOverview(value.overview) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "trends") ? { trends: parseTrends(value.trends) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "quality") ? { quality: parseQuality(value.quality) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "collector_runtime") ? { collectorRuntime: parseCollectorRuntime(value.collector_runtime) } : {}),
    ...(Object.prototype.hasOwnProperty.call(value, "recent_completed_units") ? { recentCompletedUnits: parseRecentCompleted(value.recent_completed_units) } : {}),
  };
}

function parseJson(rawText: string): unknown {
  try {
    return JSON.parse(rawText) as unknown;
  } catch {
    throw new Error("malformed line summary response");
  }
}

export function parseLineSummaryResponseJson(rawText: string): LineSummary {
  return parseLineSummaryResponse(parseJson(rawText));
}
