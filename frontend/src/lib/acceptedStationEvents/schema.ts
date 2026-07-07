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

const allowedFieldSet = new Set<string>(acceptedStationEventFields);

function assertPlainObject(value: unknown, label: string): asserts value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
}

function parseItem(value: unknown): AcceptedStationEventItem {
  assertPlainObject(value, "accepted event item");

  for (const key of Object.keys(value)) {
    if (!allowedFieldSet.has(key)) {
      throw new Error(`forbidden accepted event DTO field: ${key}`);
    }
  }

  const item: Partial<AcceptedStationEventItem> = {};
  for (const field of acceptedStationEventFields) {
    const fieldValue = value[field];
    if (fieldValue !== null && typeof fieldValue !== "string" && typeof fieldValue !== "number") {
      throw new Error(`invalid accepted event DTO field: ${field}`);
    }
    item[field] = fieldValue ?? null;
  }

  return item as AcceptedStationEventItem;
}

export function parseAcceptedStationEventsEnvelope(value: unknown): AcceptedStationEventsEnvelope {
  assertPlainObject(value, "accepted station events envelope");
  assertPlainObject(value.data, "data");
  assertPlainObject(value.page, "page");

  if (!Array.isArray(value.data.items)) throw new Error("data.items must be an array");

  const nextCursor = value.page.next_cursor;
  const limit = value.page.limit;
  if (nextCursor !== null && typeof nextCursor !== "string") throw new Error("page.next_cursor must be string or null");
  if (typeof limit !== "number" || !Number.isInteger(limit) || limit < 1 || limit > 500) {
    throw new Error("page.limit must be between 1 and 500");
  }

  return {
    items: value.data.items.map(parseItem),
    page: {
      next_cursor: nextCursor,
      limit
    }
  };
}
