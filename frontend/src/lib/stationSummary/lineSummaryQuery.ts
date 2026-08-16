import { parseStationSummaryInstant } from "./query";

export type LineSummaryMode = "LIVE" | "FIXED";

export type LineSummaryQuery = Readonly<{
  lineId: string;
  startTime: string;
  endTime: string;
  stationId?: string;
  mode?: LineSummaryMode;
}>;

export type LineSummaryQueryValidation =
  | { ok: true; query: LineSummaryQuery }
  | { ok: false; reason: string };

const MAX_WINDOW_MS = 31 * 24 * 60 * 60 * 1000;

export function validateLineSummaryQuery(query: LineSummaryQuery): LineSummaryQueryValidation {
  const lineId = query.lineId.trim();
  if (!lineId) return { ok: false, reason: "line_id is required" };
  const mode = query.mode ?? "FIXED";
  if (mode !== "LIVE" && mode !== "FIXED") return { ok: false, reason: "mode must be LIVE or FIXED" };

  let startTimestamp: number;
  let endTimestamp: number;
  try {
    startTimestamp = parseStationSummaryInstant(query.startTime);
  } catch {
    return { ok: false, reason: "start_time must be a timezone-aware ISO-8601 instant" };
  }
  try {
    endTimestamp = parseStationSummaryInstant(query.endTime);
  } catch {
    return { ok: false, reason: "end_time must be a timezone-aware ISO-8601 instant" };
  }
  if (endTimestamp <= startTimestamp) return { ok: false, reason: "end_time must be after start_time" };
  if (endTimestamp - startTimestamp > MAX_WINDOW_MS) return { ok: false, reason: "time window must be 31 days or less" };

  const stationId = query.stationId?.trim();
  return {
    ok: true,
    query: {
      lineId,
      startTime: query.startTime,
      endTime: query.endTime,
      mode,
      ...(stationId ? { stationId } : {}),
    },
  };
}
