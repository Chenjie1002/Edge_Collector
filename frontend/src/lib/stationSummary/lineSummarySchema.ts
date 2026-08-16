export type LineSummaryReconciliationStatus = "PASS" | "FAIL";

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
}>;

type JsonObject = Record<string, unknown>;

function isPlainObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function exactKeys(value: JsonObject, required: readonly string[], label: string): void {
  const allowed = new Set(required);
  if (Object.keys(value).some((key) => !allowed.has(key)) || required.some((key) => !Object.prototype.hasOwnProperty.call(value, key))) {
    throw new Error(`invalid ${label}`);
  }
}

function nonBlankString(value: unknown, label: string): string {
  if (typeof value !== "string" || value.trim() === "") throw new Error(`invalid ${label}`);
  return value;
}

function nonNegativeSafeInteger(value: unknown, label: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value < 0) throw new Error(`invalid ${label}`);
  return value;
}

function reconciliationStatus(value: unknown, label: string): LineSummaryReconciliationStatus {
  if (value !== "PASS" && value !== "FAIL") throw new Error(`invalid ${label}`);
  return value;
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
  return {
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
}

export function parseLineSummaryResponse(value: unknown): LineSummary {
  if (!isPlainObject(value)) throw new Error("invalid line summary response");
  exactKeys(value, ["contract_version", "scope", "topology", "cohort", "stations"], "line summary response");
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

  return { contractVersion: "production-line-summary/v1", scope, topology, cohort, stations: stationSummaries };
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
