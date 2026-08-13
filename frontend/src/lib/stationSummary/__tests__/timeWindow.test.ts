import { describe, expect, it } from "vitest";
import { localMinuteToOffsetIso, offsetIsoToLocalMinute, quickRangeAt, validateLocalWindow } from "../timeWindow";

describe("station summary plant-time window", () => {
  it("converts datetime-local minutes with explicit Asia/Shanghai offset", () => {
    expect(localMinuteToOffsetIso("2026-07-05T08:00", "+08:00")).toBe("2026-07-05T08:00:00+08:00");
    expect(offsetIsoToLocalMinute("2026-07-05T00:00:00Z")).toBe("2026-07-05T08:00");
  });

  it("uses plant time for exact quick ranges rather than browser-local time", () => {
    const range = quickRangeAt(new Date("2026-07-05T00:15:42.500Z"), 8);
    expect(range).toEqual({ startLocal: "2026-07-05T00:15", endLocal: "2026-07-05T08:15" });
  });

  it("accepts positive windows up to 31 days and rejects invalid windows", () => {
    expect(validateLocalWindow("2026-07-01T00:00", "2026-07-01T01:00")).toEqual({ ok: true });
    expect(validateLocalWindow("2026-07-01T00:00", "2026-08-01T00:00")).toEqual({ ok: true });
    expect(validateLocalWindow("2026-07-01T00:00", "2026-08-01T00:01").ok).toBe(false);
    expect(validateLocalWindow("2026-07-01T01:00", "2026-07-01T01:00").ok).toBe(false);
    expect(validateLocalWindow("2026-07-01T01:00", "2026-07-01T00:00").ok).toBe(false);
    expect(validateLocalWindow("2026-02-30T00:00", "2026-03-01T00:00").ok).toBe(false);
  });
});
