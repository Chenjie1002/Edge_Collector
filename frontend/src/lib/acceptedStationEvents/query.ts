export type AcceptedStationEventsQuery = {
  lineId: string;
  startTime: string;
  endTime: string;
  limit: number;
  cursor?: string;
};

export type QueryValidationResult =
  | { ok: true; query: AcceptedStationEventsQuery }
  | { ok: false; reason: string };

const MAX_WINDOW_MS = 31 * 24 * 60 * 60 * 1000;
const TIMEZONE_AWARE_ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/;

export function validateAcceptedStationEventsQuery(query: AcceptedStationEventsQuery): QueryValidationResult {
  const lineId = query.lineId.trim();
  if (!lineId) return { ok: false, reason: "line_id is required" };
  if (!query.startTime || !query.endTime) return { ok: false, reason: "start_time and end_time are required" };
  if (!TIMEZONE_AWARE_ISO.test(query.startTime) || !TIMEZONE_AWARE_ISO.test(query.endTime)) {
    return { ok: false, reason: "start_time and end_time must be timezone-aware ISO-8601 instants" };
  }

  const start = Date.parse(query.startTime);
  const end = Date.parse(query.endTime);
  if (!Number.isFinite(start) || !Number.isFinite(end)) return { ok: false, reason: "time range is invalid" };
  if (end <= start) return { ok: false, reason: "end_time must be after start_time" };
  if (end - start > MAX_WINDOW_MS) return { ok: false, reason: "time window must be 31 days or less" };
  if (!Number.isInteger(query.limit) || query.limit < 1 || query.limit > 500) {
    return { ok: false, reason: "limit must be between 1 and 500" };
  }

  return { ok: true, query: { ...query, lineId } };
}

export function buildAcceptedStationEventsQuery(query: AcceptedStationEventsQuery): URLSearchParams {
  const validation = validateAcceptedStationEventsQuery(query);
  if (!validation.ok) throw new Error(validation.reason);

  const params = new URLSearchParams();
  params.set("line_id", validation.query.lineId);
  params.set("start_time", validation.query.startTime);
  params.set("end_time", validation.query.endTime);
  params.set("limit", String(validation.query.limit));
  if (validation.query.cursor) params.set("cursor", validation.query.cursor);
  return params;
}

export function clearCursorForScopeChange(
  previous: AcceptedStationEventsQuery,
  next: AcceptedStationEventsQuery
): AcceptedStationEventsQuery {
  if (
    previous.lineId !== next.lineId ||
    previous.startTime !== next.startTime ||
    previous.endTime !== next.endTime ||
    previous.limit !== next.limit
  ) {
    const { cursor: _cursor, ...withoutCursor } = next;
    return withoutCursor;
  }
  return next;
}
