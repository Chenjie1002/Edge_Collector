import { describe, expect, it, vi } from "vitest";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../acceptedStationEvents/apiOrigin";
import { fetchLineSummary } from "../lineSummaryApi";

const query = {
  lineId: "LINE_001",
  startTime: "2026-08-16T10:00:00Z",
  endTime: "2026-08-16T11:00:00Z",
};

const summary = {
  contract_version: "production-line-summary/v1",
  scope: { line_id: "LINE_001", start_time: query.startTime, end_time: query.endTime, cohort_basis: "terminal_completed" },
  topology: { entry_station_id: "WS01", terminal_station_id: "WS03", stations: ["WS01", "WS02", "WS03"] },
  cohort: { unit_count: 2, reconciliation_status: "PASS", errors: [] },
  stations: [
    { station_id: "WS01", total: 2, ok: 1, nok: 1, new_nok: 1, skipped: 0, processed: 2, reconciliation_status: "PASS", evidence_count: 2, missing_unit_count: 0, duplicate_unit_count: 0, invalid_record_count: 0, result_compatibility: "native_nok_process_status_split" },
    { station_id: "WS02", total: 2, ok: 1, nok: 1, new_nok: 0, skipped: 1, processed: 1, reconciliation_status: "PASS", evidence_count: 2, missing_unit_count: 0, duplicate_unit_count: 0, invalid_record_count: 0, result_compatibility: "native_nok_process_status_split" },
    { station_id: "WS03", total: 2, ok: 1, nok: 1, new_nok: 0, skipped: 1, processed: 1, reconciliation_status: "PASS", evidence_count: 2, missing_unit_count: 0, duplicate_unit_count: 0, invalid_record_count: 0, result_compatibility: "native_nok_process_status_split" },
  ],
};

function origin() {
  const result = resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: "https://accepted-api.example",
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production",
  });
  if (!result.ok) throw new Error("origin fixture must resolve");
  return result.origin;
}

function response(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: vi.fn().mockResolvedValue(JSON.stringify(body)),
  } as unknown as Response;
}

describe("line summary api client", () => {
  it("uses one trusted terminal-cohort GET route with no-store credential-free options", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(200, summary));

    const result = await fetchLineSummary(query, origin(), fetchMock);

    expect(result.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [input, options] = fetchMock.mock.calls[0];
    const endpoint = new URL(String(input));
    expect(endpoint.pathname).toBe("/api/v2/production/line-summary");
    expect(endpoint.searchParams.get("line_id")).toBe("LINE_001");
    expect(endpoint.searchParams.get("start_time")).toBe(query.startTime);
    expect(endpoint.searchParams.get("end_time")).toBe(query.endTime);
    expect(options).toEqual({ method: "GET", cache: "no-store", credentials: "omit", redirect: "error" });
  });

  it("rejects a response whose cohort scope does not match the requested line window", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      response(200, { ...summary, scope: { ...summary.scope, line_id: "LINE_OTHER" } }),
    );

    await expect(fetchLineSummary(query, origin(), fetchMock)).resolves.toEqual({
      ok: false,
      kind: "malformed",
      message: "Line summary response was malformed.",
    });
  });

  it("fails closed before the network for an invalid time window", async () => {
    const fetchMock = vi.fn();

    await expect(fetchLineSummary({ ...query, endTime: query.startTime }, origin(), fetchMock)).resolves.toEqual({
      ok: false,
      kind: "invalid-query",
      message: "end_time must be after start_time",
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("keeps source unavailability explicit", async () => {
    await expect(fetchLineSummary(query, origin(), vi.fn().mockResolvedValue(response(503, {})))).resolves.toEqual({
      ok: false,
      kind: "unavailable",
      message: "Line summary source unavailable.",
    });
  });
});
