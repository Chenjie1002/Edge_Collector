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

type AcceptedStationEventField = (typeof acceptedStationEventFields)[number];

export type AcceptedStationEventItem = Record<AcceptedStationEventField, string | number | null>;

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

function parseItem(value: unknown): AcceptedStationEventItem {
  assertPlainObject(value, "accepted event item");
  assertExactOwnKeys(value, "accepted event DTO field", acceptedStationEventFields);

  const item = {} as AcceptedStationEventItem;
  for (const field of acceptedStationEventFields) {
    const fieldValue = value[field];
    if (fieldValue !== null && typeof fieldValue !== "string" && typeof fieldValue !== "number") {
      throw new Error(`invalid accepted event DTO field: ${field}`);
    }
    item[field] = fieldValue;
  }

  return item;
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
  if (nextCursor !== null && typeof nextCursor !== "string") throw new Error("invalid page.next_cursor: must be string or null");
  if (typeof limit !== "number" || !Number.isInteger(limit) || limit < 1 || limit > 500) {
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
