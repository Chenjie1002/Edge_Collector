export type QuickRangeHours = 1 | 8 | 24;

export type LocalWindow = Readonly<{
  startLocal: string;
  endLocal: string;
}>;

export type LocalWindowValidation = { ok: true } | { ok: false; reason: string };

const PLANT_OFFSET = "+08:00";
const PLANT_OFFSET_MINUTES = 8 * 60;
const MAX_WINDOW_MS = 31 * 24 * 60 * 60 * 1000;
const LOCAL_MINUTE = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$/;
const TIMEZONE_AWARE = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})$/;

function daysInMonth(year: number, month: number): number {
  if (month === 2) {
    const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
    return leap ? 29 : 28;
  }
  return [4, 6, 9, 11].includes(month) ? 30 : 31;
}

function wallClockToUtc(year: number, month: number, day: number, hour: number, minute: number, second: number, milliseconds: number): number | null {
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
  return base.getTime();
}

function parseLocalMinute(value: string, utcOffset: string): number | null {
  if (utcOffset !== PLANT_OFFSET) return null;
  const match = LOCAL_MINUTE.exec(value);
  if (!match) return null;
  const wallClock = wallClockToUtc(Number(match[1]), Number(match[2]), Number(match[3]), Number(match[4]), Number(match[5]), 0, 0);
  return wallClock === null ? null : wallClock - PLANT_OFFSET_MINUTES * 60 * 1000;
}

function parseTimezoneAwareInstant(value: string): number | null {
  const match = TIMEZONE_AWARE.exec(value);
  if (!match) return null;
  const fraction = match[7] ?? "";
  const milliseconds = Number(fraction.padEnd(3, "0").slice(0, 3) || "0");
  const wallClock = wallClockToUtc(Number(match[1]), Number(match[2]), Number(match[3]), Number(match[4]), Number(match[5]), Number(match[6]), milliseconds);
  if (wallClock === null) return null;
  const offset = match[8];
  if (offset === "Z") return wallClock;
  const offsetHours = Number(offset.slice(1, 3));
  const offsetMinutes = Number(offset.slice(4, 6));
  if (offsetHours > 23 || offsetMinutes > 59) return null;
  const totalOffsetMinutes = offsetHours * 60 + offsetMinutes;
  return wallClock - (offset[0] === "+" ? totalOffsetMinutes : -totalOffsetMinutes) * 60 * 1000;
}

function localMinuteFromPlantTimestamp(timestamp: number): string {
  return new Date(timestamp + PLANT_OFFSET_MINUTES * 60 * 1000).toISOString().slice(0, 16);
}

export function localMinuteToOffsetIso(localValue: string, utcOffset: "+08:00"): string {
  if (parseLocalMinute(localValue, utcOffset) === null) throw new Error("invalid plant-local datetime");
  return `${localValue}:00${utcOffset}`;
}

export function offsetIsoToLocalMinute(value: string, utcOffset: "+08:00" = PLANT_OFFSET): string {
  if (utcOffset !== PLANT_OFFSET) throw new Error("unsupported plant timezone offset");
  const timestamp = parseTimezoneAwareInstant(value);
  if (timestamp === null) throw new Error("invalid timezone-aware datetime");
  return localMinuteFromPlantTimestamp(timestamp);
}

export function quickRangeAt(now: Date, hours: QuickRangeHours): LocalWindow {
  if (!Number.isFinite(now.getTime()) || ![1, 8, 24].includes(hours)) throw new Error("invalid quick range");
  const endTimestamp = now.getTime() - (now.getTime() % (60 * 1000));
  const endLocal = localMinuteFromPlantTimestamp(endTimestamp);
  const startLocal = localMinuteFromPlantTimestamp(endTimestamp - hours * 60 * 60 * 1000);
  return { startLocal, endLocal };
}

export function validateLocalWindow(startLocal: string, endLocal: string): LocalWindowValidation {
  const start = parseLocalMinute(startLocal, PLANT_OFFSET);
  if (start === null) return { ok: false, reason: "Start time must be a valid Asia/Shanghai local minute." };
  const end = parseLocalMinute(endLocal, PLANT_OFFSET);
  if (end === null) return { ok: false, reason: "End time must be a valid Asia/Shanghai local minute." };
  if (end <= start) return { ok: false, reason: "End time must be after Start time." };
  if (end - start > MAX_WINDOW_MS) return { ok: false, reason: "Time window must be 31 days or less." };
  return { ok: true };
}
