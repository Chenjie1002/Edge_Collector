export const acceptedStationEventFields = [
  "line_id",
  "plc_id",
  "station_id",
  "station_type",
  "profile_id",
  "config_hash",
  "config_version",
  "event_type",
  "production_result",
  "unit_id",
  "dmc",
  "cycle_counter",
  "source_event_id",
  "event_ts",
  "accepted_at",
  "fact_key",
  "content_fingerprint",
  "nok_code",
  "nok_origin",
  "nok_detail_code",
  "nok_detail_source_event_id",
  "nok_detail_evidence_fact_key"
] as const;

export const acceptedStationEventTypes = [
  "station_cycle_start",
  "station_cycle_complete",
  "station_result",
  "station_nok"
] as const;

export const acceptedProductionResults = ["ok", "nok", "skip", "not_applicable"] as const;

export type AcceptedStationEventType = (typeof acceptedStationEventTypes)[number];
export type AcceptedProductionResult = (typeof acceptedProductionResults)[number];

export type AcceptedStationEventItem = {
  line_id: string;
  plc_id: string;
  station_id: string;
  station_type: string;
  profile_id: string;
  config_hash: string;
  config_version: string;
  event_type: AcceptedStationEventType;
  production_result: AcceptedProductionResult | null;
  unit_id: string | null;
  dmc: string | null;
  cycle_counter: number;
  source_event_id: string;
  event_ts: string;
  accepted_at: string;
  fact_key: string;
  content_fingerprint: string;
  nok_code: number | null;
  nok_origin: string | null;
  nok_detail_code: number | null;
  nok_detail_source_event_id: string | null;
  nok_detail_evidence_fact_key: string | null;
};

export type AcceptedStationEventsEnvelope = {
  items: AcceptedStationEventItem[];
  page: {
    next_cursor: string | null;
    limit: number;
  };
};

const envelopeKeys = ["data", "page"] as const;
const dataKeys = ["items"] as const;
const pageKeys = ["next_cursor", "limit"] as const;
const canonicalIntegerPattern = /^(?:0|-?[1-9][0-9]*)$/;
const sourceValidatedNumericKeys = new Set(["cycle_counter", "nok_code", "nok_detail_code", "limit"]);
const minSafeInteger = BigInt(Number.MIN_SAFE_INTEGER);
const maxSafeInteger = BigInt(Number.MAX_SAFE_INTEGER);

type JsonParseContext = {
  source?: string;
};

type JsonReviverWithContext = (
  this: unknown,
  key: string,
  value: unknown,
  context?: JsonParseContext
) => unknown;

type JsonParseWithContext = (text: string, reviver?: JsonReviverWithContext) => unknown;

function assertExactOwnKeys(value: Record<string, unknown>, label: string, allowedKeys: readonly string[]) {
  const allowedKeySet = new Set<string>(allowedKeys);
  for (const key of Object.keys(value)) {
    if (!allowedKeySet.has(key)) {
      throw new Error(`forbidden ${label} key: ${key}`);
    }
  }
  for (const key of allowedKeys) {
    if (!Object.prototype.hasOwnProperty.call(value, key)) {
      throw new Error(`missing required ${label} key: ${key}`);
    }
  }
}

function assertPlainObject(value: unknown, label: string): asserts value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
}

function parseRequiredString(value: unknown, field: string): string {
  if (typeof value !== "string") throw new Error(`invalid accepted event DTO field: ${field}`);
  return value;
}

function parseNullableString(value: unknown, field: string): string | null {
  if (value === null || typeof value === "string") return value;
  throw new Error(`invalid accepted event DTO field: ${field}`);
}

function parseSafeInteger(value: unknown, field: string): number {
  if (typeof value !== "number" || !Number.isSafeInteger(value)) {
    throw new Error(`invalid accepted event DTO field: ${field}`);
  }
  return value;
}

function parseNullableSafeInteger(value: unknown, field: string): number | null {
  if (value === null) return null;
  return parseSafeInteger(value, field);
}

function parseEventType(value: unknown): AcceptedStationEventType {
  const eventType = parseRequiredString(value, "event_type");
  if (!(acceptedStationEventTypes as readonly string[]).includes(eventType)) {
    throw new Error("invalid accepted event DTO field: event_type");
  }
  return eventType as AcceptedStationEventType;
}

function parseProductionResult(value: unknown): AcceptedProductionResult | null {
  if (value === null) return null;
  const result = parseRequiredString(value, "production_result");
  if (!(acceptedProductionResults as readonly string[]).includes(result)) {
    throw new Error("invalid accepted event DTO field: production_result");
  }
  return result as AcceptedProductionResult;
}

function isValidUtcIsoString(value: string): boolean {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z$/.exec(value);
  if (!match) return false;

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const millisecond = Number((match[7] ?? "").padEnd(3, "0").slice(0, 3));

  if (month < 1 || month > 12 || day < 1 || day > 31 || hour > 23 || minute > 59 || second > 59) {
    return false;
  }

  const parsed = new Date(0);
  parsed.setUTCFullYear(year, month - 1, day);
  parsed.setUTCHours(hour, minute, second, millisecond);

  return (
    parsed.getUTCFullYear() === year &&
    parsed.getUTCMonth() === month - 1 &&
    parsed.getUTCDate() === day &&
    parsed.getUTCHours() === hour &&
    parsed.getUTCMinutes() === minute &&
    parsed.getUTCSeconds() === second &&
    parsed.getUTCMilliseconds() === millisecond
  );
}

function parseUtcTimestamp(value: unknown, field: "event_ts" | "accepted_at"): string {
  const timestamp = parseRequiredString(value, field);
  if (!isValidUtcIsoString(timestamp)) throw new Error(`invalid accepted event DTO field: ${field}`);
  return timestamp;
}

function hasAnyDetailValue(item: AcceptedStationEventItem): boolean {
  return (
    item.nok_detail_code !== null ||
    item.nok_detail_source_event_id !== null ||
    item.nok_detail_evidence_fact_key !== null
  );
}

function assertCrossFieldContract(item: AcceptedStationEventItem): void {
  if (item.event_type === "station_result") {
    if (item.production_result === null) throw new Error("invalid accepted event contract combination");
    if (hasAnyDetailValue(item)) throw new Error("invalid accepted event contract combination");

    if (item.production_result === "nok") {
      if (item.nok_code === null || item.nok_origin === null) {
        throw new Error("invalid accepted event contract combination");
      }
      return;
    }

    if (item.nok_code !== null || item.nok_origin !== null) {
      throw new Error("invalid accepted event contract combination");
    }
    return;
  }

  if (item.event_type === "station_nok") {
    if (
      item.production_result !== null ||
      item.nok_code === null ||
      item.nok_origin === null ||
      item.nok_detail_code === null ||
      item.nok_detail_source_event_id === null ||
      item.nok_detail_evidence_fact_key === null
    ) {
      throw new Error("invalid accepted event contract combination");
    }
    return;
  }

  if (
    item.production_result !== null ||
    item.nok_code !== null ||
    item.nok_origin !== null ||
    hasAnyDetailValue(item)
  ) {
    throw new Error("invalid accepted event contract combination");
  }
}

function parseItem(value: unknown): AcceptedStationEventItem {
  assertPlainObject(value, "accepted event item");
  assertExactOwnKeys(value, "accepted event DTO field", acceptedStationEventFields);

  const item: AcceptedStationEventItem = {
    line_id: parseRequiredString(value.line_id, "line_id"),
    plc_id: parseRequiredString(value.plc_id, "plc_id"),
    station_id: parseRequiredString(value.station_id, "station_id"),
    station_type: parseRequiredString(value.station_type, "station_type"),
    profile_id: parseRequiredString(value.profile_id, "profile_id"),
    config_hash: parseRequiredString(value.config_hash, "config_hash"),
    config_version: parseRequiredString(value.config_version, "config_version"),
    event_type: parseEventType(value.event_type),
    production_result: parseProductionResult(value.production_result),
    unit_id: parseNullableString(value.unit_id, "unit_id"),
    dmc: parseNullableString(value.dmc, "dmc"),
    cycle_counter: parseSafeInteger(value.cycle_counter, "cycle_counter"),
    source_event_id: parseRequiredString(value.source_event_id, "source_event_id"),
    event_ts: parseUtcTimestamp(value.event_ts, "event_ts"),
    accepted_at: parseUtcTimestamp(value.accepted_at, "accepted_at"),
    fact_key: parseRequiredString(value.fact_key, "fact_key"),
    content_fingerprint: parseRequiredString(value.content_fingerprint, "content_fingerprint"),
    nok_code: parseNullableSafeInteger(value.nok_code, "nok_code"),
    nok_origin: parseNullableString(value.nok_origin, "nok_origin"),
    nok_detail_code: parseNullableSafeInteger(value.nok_detail_code, "nok_detail_code"),
    nok_detail_source_event_id: parseNullableString(value.nok_detail_source_event_id, "nok_detail_source_event_id"),
    nok_detail_evidence_fact_key: parseNullableString(value.nok_detail_evidence_fact_key, "nok_detail_evidence_fact_key")
  };

  assertCrossFieldContract(item);
  return item;
}

function validateNumericSource(key: string, value: unknown, context?: JsonParseContext): unknown {
  if (typeof value !== "number" || !sourceValidatedNumericKeys.has(key)) return value;

  const source = context?.source;
  if (typeof source !== "string" || !canonicalIntegerPattern.test(source)) {
    throw new Error("invalid numeric source");
  }

  const integer = BigInt(source);
  if (integer < minSafeInteger || integer > maxSafeInteger) {
    throw new Error("invalid numeric source");
  }

  return value;
}

export function parseAcceptedStationEventsEnvelope(value: unknown): AcceptedStationEventsEnvelope {
  assertPlainObject(value, "accepted station events envelope");
  assertExactOwnKeys(value, "accepted station events envelope", envelopeKeys);
  assertPlainObject(value.data, "data");
  assertExactOwnKeys(value.data, "data", dataKeys);
  assertPlainObject(value.page, "page");
  assertExactOwnKeys(value.page, "page", pageKeys);

  if (!Array.isArray(value.data.items)) throw new Error("invalid data.items: must be an array");

  const nextCursor = value.page.next_cursor;
  const limit = value.page.limit;
  if (nextCursor !== null && typeof nextCursor !== "string") {
    throw new Error("invalid page.next_cursor: must be string or null");
  }
  if (typeof limit !== "number" || !Number.isSafeInteger(limit) || limit < 1 || limit > 500) {
    throw new Error("invalid page.limit: must be an integer between 1 and 500");
  }

  return {
    items: value.data.items.map(parseItem),
    page: {
      next_cursor: nextCursor,
      limit
    }
  };
}

export function parseAcceptedStationEventsEnvelopeJson(rawText: string): AcceptedStationEventsEnvelope {
  try {
    const parseJson = JSON.parse as unknown as JsonParseWithContext;
    const parsed = parseJson(rawText, (key, value, context) => validateNumericSource(key, value, context));
    return parseAcceptedStationEventsEnvelope(parsed);
  } catch {
    throw new Error("Invalid accepted events response");
  }
}
