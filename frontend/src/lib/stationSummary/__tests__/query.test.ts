import { describe, expect, it } from "vitest";
import {
  buildProcessMetricsQuery,
  buildQualityQuery,
  validateStationSummaryQuery
} from "../query";

const baseQuery = {
  lineId: "LINE_001",
  stationId: "WS01",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z"
};

describe("station summary query", () => {
  it("validates one bounded scope and builds the two canonical route queries", () => {
    const validation = validateStationSummaryQuery(baseQuery);

    expect(validation).toEqual({ ok: true, query: baseQuery });
    expect([...buildQualityQuery(baseQuery).entries()]).toEqual([
      ["line_id", "LINE_001"],
      ["station_id", "WS01"],
      ["start_time", "2026-07-05T00:00:00Z"],
      ["end_time", "2026-07-05T08:00:00Z"]
    ]);
    expect([...buildProcessMetricsQuery(baseQuery).entries()]).toEqual([
      ["line_id", "LINE_001"],
      ["station_id", "WS01"],
      ["from", "2026-07-05T00:00:00Z"],
      ["to", "2026-07-05T08:00:00Z"]
    ]);
  });

  it.each([
    ["missing line", { ...baseQuery, lineId: " " }],
    ["missing station", { ...baseQuery, stationId: "" }],
    ["naive start", { ...baseQuery, startTime: "2026-07-05T00:00:00" }],
    ["invalid date", { ...baseQuery, startTime: "2026-02-30T00:00:00Z" }],
    ["inverted window", { ...baseQuery, startTime: baseQuery.endTime, endTime: baseQuery.startTime }],
    ["window over 31 days", { ...baseQuery, endTime: "2026-08-06T00:00:01Z" }]
  ])("fails closed before either request for %s", (_name, query) => {
    expect(validateStationSummaryQuery(query).ok).toBe(false);
    expect(() => buildQualityQuery(query)).toThrow();
    expect(() => buildProcessMetricsQuery(query)).toThrow();
  });
});
