import { describe, expect, it } from "vitest";
import {
  buildAcceptedStationEventsQuery,
  clearCursorForScopeChange,
  validateAcceptedStationEventsQuery
} from "../query";

const baseQuery = {
  lineId: "LINE_001",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z",
  limit: 50,
  cursor: "opaque.cursor.value"
};

describe("accepted station events query", () => {
  it("sends only the frozen Dashboard query parameters", () => {
    const params = buildAcceptedStationEventsQuery(baseQuery);

    expect([...params.keys()].sort()).toEqual([
      "cursor",
      "end_time",
      "limit",
      "line_id",
      "start_time"
    ]);
    expect(params.get("cursor")).toBe("opaque.cursor.value");
  });

  it.each([
    ["missing line", { ...baseQuery, lineId: "" }],
    ["missing start", { ...baseQuery, startTime: "" }],
    ["missing end", { ...baseQuery, endTime: "" }],
    ["invalid start", { ...baseQuery, startTime: "not-a-time" }],
    ["inverted window", { ...baseQuery, startTime: baseQuery.endTime, endTime: baseQuery.startTime }],
    ["too large", { ...baseQuery, endTime: "2026-08-06T00:00:01Z" }],
    ["zero limit", { ...baseQuery, limit: 0 }],
    ["over max limit", { ...baseQuery, limit: 501 }],
    ["non-integer limit", { ...baseQuery, limit: 50.5 }],
    ["NaN limit", { ...baseQuery, limit: Number.NaN }]
  ])("fails closed before request for %s", (_name, query) => {
    expect(validateAcceptedStationEventsQuery(query).ok).toBe(false);
    expect(() => buildAcceptedStationEventsQuery(query)).toThrow();
  });

  it("keeps cursor opaque and clears it when scope, time, or limit changes", () => {
    expect(clearCursorForScopeChange(baseQuery, { ...baseQuery, lineId: "LINE_002" }).cursor).toBeUndefined();
    expect(clearCursorForScopeChange(baseQuery, { ...baseQuery, startTime: "2026-07-05T01:00:00Z" }).cursor).toBeUndefined();
    expect(clearCursorForScopeChange(baseQuery, { ...baseQuery, endTime: "2026-07-05T09:00:00Z" }).cursor).toBeUndefined();
    expect(clearCursorForScopeChange(baseQuery, { ...baseQuery, limit: 100 }).cursor).toBeUndefined();
    expect(clearCursorForScopeChange(baseQuery, { ...baseQuery, cursor: "another.opaque.value" }).cursor).toBe("another.opaque.value");
  });
});
