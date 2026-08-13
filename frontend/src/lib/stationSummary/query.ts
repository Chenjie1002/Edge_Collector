export type StationSummaryQuery = {
  lineId: string;
  stationId: string;
  startTime: string;
  endTime: string;
};

export type StationSummaryQueryValidation =
  | { ok: true; query: StationSummaryQuery }
  | { ok: false; reason: string };

const MAX_WINDOW_MS = 31 * 24 * 60 * 60 * 1000;
const TIMEZONE_AWARE_ISO =
  /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})$/;

function daysInMonth(year: number, month: number): number {
  if (month === 2) {
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    return leap ? 29 : 28;
  }
  return [4, 6, 9, 11].includes(month) ? 30 : 31;
}

function parseTimezoneAwareInstant(value: string): number | null {
  const match = TIMEZONE_AWARE_ISO.exec(value);
  if (!match) return null;

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const fractional = match[7];
  const offset = match[8];

  if (
    month < 1 ||
    month > 12 ||
    day < 1 ||
    day > daysInMonth(year, month) ||
    hour > 23 ||
    minute > 59 ||
    second > 59
  ) {
    return null;
  }

  let milliseconds = 0;
  if (offset !== "Z") {
    const offsetHours = Number(offset.slice(1, 3));
    const offsetMinutes = Number(offset.slice(4, 6));
    if (offsetHours > 23 || offsetMinutes > 59) return null;
  }

  if (fractional) {
    milliseconds = Number(fractional.padEnd(3, "0").slice(0, 3));
  }

  const utc = Date.UTC(year >= 100 ? year : 100, month - 1, day, hour, minute, second, milliseconds);
  const base = new Date(utc);
  if (year < 100) base.setUTCFullYear(year);

  if (
    base.getUTCFullYear() !== year ||
    base.getUTCMonth() !== month - 1 ||
    base.getUTCDate() !== day ||
    base.getUTCHours() !== hour ||
    base.getUTCMinutes() !== minute ||
    base.getUTCSeconds() !== second ||
    base.getUTCMilliseconds() !== milliseconds
  ) {
    return null;
  }

  if (offset === "Z") return base.getTime();
  const sign = offset[0] === "+" ? 1 : -1;
  const offsetMinutes = Number(offset.slice(1, 3)) * 60 + Number(offset.slice(4, 6));
  return base.getTime() - sign * offsetMinutes * 60 * 1000;
}

function validateInstant(value: string, field: string): { ok: true; timestamp: number } | { ok: false; reason: string } {
  if (!value) return { ok: false, reason: `${field} is required` };
  const timestamp = parseTimezoneAwareInstant(value);
  if (timestamp === null || !Number.isFinite(timestamp)) {
    return { ok: false, reason: `${field} must be a timezone-aware ISO-8601 instant` };
  }
  return { ok: true, timestamp };
}

export function validateStationSummaryQuery(query: StationSummaryQuery): StationSummaryQueryValidation {
  const lineId = query.lineId.trim();
  if (!lineId) return { ok: false, reason: "line_id is required" };

  const stationId = query.stationId.trim();
  if (!stationId) return { ok: false, reason: "station_id is required" };

  const start = validateInstant(query.startTime, "start_time");
  if (!start.ok) return start;
  const end = validateInstant(query.endTime, "end_time");
  if (!end.ok) return end;
  if (end.timestamp <= start.timestamp) return { ok: false, reason: "end_time must be after start_time" };
  if (end.timestamp - start.timestamp > MAX_WINDOW_MS) {
    return { ok: false, reason: "time window must be 31 days or less" };
  }

  return {
    ok: true,
    query: { lineId, stationId, startTime: query.startTime, endTime: query.endTime }
  };
}

function validatedQuery(query: StationSummaryQuery): StationSummaryQuery {
  const validation = validateStationSummaryQuery(query);
  if (!validation.ok) throw new Error(validation.reason);
  return validation.query;
}

export function buildQualityQuery(query: StationSummaryQuery): URLSearchParams {
  const valid = validatedQuery(query);
  const params = new URLSearchParams();
  params.set("line_id", valid.lineId);
  params.set("station_id", valid.stationId);
  params.set("start_time", valid.startTime);
  params.set("end_time", valid.endTime);
  return params;
}

export function buildProcessMetricsQuery(query: StationSummaryQuery): URLSearchParams {
  const valid = validatedQuery(query);
  const params = new URLSearchParams();
  params.set("line_id", valid.lineId);
  params.set("station_id", valid.stationId);
  params.set("from", valid.startTime);
  params.set("to", valid.endTime);
  return params;
}

export function parseStationSummaryInstant(value: string): number {
  const parsed = parseTimezoneAwareInstant(value);
  if (parsed === null) throw new Error("invalid station summary timestamp");
  return parsed;
}
