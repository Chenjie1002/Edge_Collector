import { describe, expect, it, vi } from "vitest";
import { fetchAcceptedStationEvents } from "../apiClient";

const validQuery = {
  lineId: "LINE_001",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z",
  limit: 50,
  cursor: "opaque.cursor.value"
};

const validEnvelope = {
  data: {
    items: [
      {
        line_id: "LINE_001",
        plc_id: "PLC_001",
        station_id: "WS01",
        station_type: "ASSEMBLY",
        profile_id: "normal",
        config_hash: "sha256:abc",
        config_version: "2026.07.05.1",
        event_type: "station_result",
        production_result: "ok",
        unit_id: "U-001",
        dmc: "DMC-001",
        cycle_counter: 301,
        source_event_id: "PLC_001:WS01:301",
        event_ts: "2026-07-05T10:00:00Z",
        accepted_at: "2026-07-05T10:00:01Z",
        fact_key: "sha256:fact",
        content_fingerprint: "sha256:content",
        nok_code: null,
        nok_origin: null,
        nok_detail_code: null,
        nok_detail_source_event_id: null,
        nok_detail_evidence_fact_key: null
      }
    ]
  },
  page: { next_cursor: null, limit: 50 }
};

function response(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: vi.fn().mockResolvedValue(body)
  } as unknown as Response;
}

describe("accepted station events api client", () => {
  it("constructs one GET request to the accepted station events endpoint with only frozen query params", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(200, validEnvelope));

    const result = await fetchAcceptedStationEvents(validQuery, fetchMock);

    expect(result.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, options] = fetchMock.mock.calls[0];
    const requestUrl = new URL(url as string, "http://dashboard.test");
    expect(requestUrl.pathname).toBe("/api/v2/production/accepted-station-events");
    expect([...requestUrl.searchParams.keys()].sort()).toEqual([
      "cursor",
      "end_time",
      "limit",
      "line_id",
      "start_time"
    ]);
    expect(requestUrl.searchParams.get("cursor")).toBe("opaque.cursor.value");
    expect(options).toMatchObject({ method: "GET", cache: "no-store" });
    expect(String(url)).not.toMatch(/legacy|raw|current|diagnostic|trace|quality/i);
  });

  it("delegates pre-request validation to query construction and fails closed before fetch", async () => {
    const fetchMock = vi.fn();

    const result = await fetchAcceptedStationEvents({ ...validQuery, lineId: " " }, fetchMock);

    expect(result).toMatchObject({ ok: false, kind: "invalid-query" });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it.each([
    ["invalid cursor", 400],
    ["expired cursor", 410],
    ["cross-scope cursor", 422]
  ])("maps %s 4xx responses to invalid-query without retry or fallback", async (_case, status) => {
    const fetchMock = vi.fn().mockResolvedValue(response(status, { error: { code: "INVALID_CURSOR" } }));

    const result = await fetchAcceptedStationEvents(validQuery, fetchMock);

    expect(result).toMatchObject({ ok: false, kind: "invalid-query" });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/v2/production/accepted-station-events?");
  });

  it("maps accepted fact source unavailable to unavailable without fallback", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(503, { detail: "accepted fact source unavailable" }));

    const result = await fetchAcceptedStationEvents(validQuery, fetchMock);

    expect(result).toMatchObject({ ok: false, kind: "unavailable" });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(String(fetchMock.mock.calls[0][0])).not.toMatch(/legacy|raw|current|diagnostic/i);
  });

  it("maps malformed DTO and unexpected responses to error", async () => {
    const malformedFetch = vi.fn().mockResolvedValue(response(200, { data: { items: [{ raw_hex: "deadbeef" }] }, page: { next_cursor: null, limit: 50 } }));
    const unexpectedFetch = vi.fn().mockResolvedValue(response(500, { error: "boom" }));

    await expect(fetchAcceptedStationEvents(validQuery, malformedFetch)).resolves.toMatchObject({ ok: false, kind: "error" });
    await expect(fetchAcceptedStationEvents(validQuery, unexpectedFetch)).resolves.toMatchObject({ ok: false, kind: "error" });
    expect(malformedFetch).toHaveBeenCalledTimes(1);
    expect(unexpectedFetch).toHaveBeenCalledTimes(1);
  });
});
