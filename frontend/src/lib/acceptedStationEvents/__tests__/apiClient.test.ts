import { describe, expect, it, vi } from "vitest";
import { fetchAcceptedStationEvents } from "../apiClient";
import { resolveTrustedAcceptedEventsApiOrigin } from "../apiOrigin";

const validQuery = {
  lineId: "LINE_001",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z",
  limit: 50,
  cursor: "opaque.cursor.value"
};

const validItem = {
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
};

const validEnvelope = {
  data: { items: [validItem] },
  page: { next_cursor: null, limit: 50 }
};

const itemMissingRequiredKey = { ...validItem } as Record<string, unknown>;
delete itemMissingRequiredKey.nok_detail_code;

function response(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: vi.fn().mockResolvedValue(body)
  } as unknown as Response;
}

function trustedOrigin() {
  const resolution = resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: "https://accepted-api.example",
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production"
  });
  if (!resolution.ok) throw new Error("test fixture origin must resolve");
  return resolution.origin;
}

function expectSingleAcceptedRequest(fetchMock: ReturnType<typeof vi.fn>) {
  expect(fetchMock).toHaveBeenCalledTimes(1);
  const requestUrl = new URL(String(fetchMock.mock.calls[0][0]));
  expect(requestUrl.origin).toBe("https://accepted-api.example");
  expect(requestUrl.pathname).toBe("/api/v2/production/accepted-station-events");
  expect(String(fetchMock.mock.calls[0][0])).not.toMatch(/legacy|raw|current|diagnostic|trace|quality/i);
}

function assertOrdinaryStringIsRejectedAtCompileTime() {
  // @ts-expect-error ordinary string must not satisfy the brand
  void fetchAcceptedStationEvents(validQuery, "https://accepted-api.example");
}
void assertOrdinaryStringIsRejectedAtCompileTime;

describe("accepted station events api client", () => {
  it("constructs one GET request to the accepted station events endpoint with only frozen query params", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(200, validEnvelope));

    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock);

    expect(result.ok).toBe(true);
    expectSingleAcceptedRequest(fetchMock);
    const [url, options] = fetchMock.mock.calls[0];
    const requestUrl = new URL(String(url));
    expect(String(url)).toBe("https://accepted-api.example/api/v2/production/accepted-station-events?line_id=LINE_001&start_time=2026-07-05T00%3A00%3A00Z&end_time=2026-07-05T08%3A00%3A00Z&limit=50&cursor=opaque.cursor.value");
    expect([...requestUrl.searchParams.keys()].sort()).toEqual(["cursor", "end_time", "limit", "line_id", "start_time"]);
    expect(requestUrl.searchParams.get("cursor")).toBe("opaque.cursor.value");
    expect(options).toEqual({ method: "GET", cache: "no-store", credentials: "omit", redirect: "error" });
  });

  it("delegates pre-request validation to query construction and fails closed before fetch", async () => {
    const fetchMock = vi.fn();
    const result = await fetchAcceptedStationEvents({ ...validQuery, lineId: " " }, trustedOrigin(), fetchMock);
    expect(result).toMatchObject({ ok: false, kind: "invalid-query" });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it.each([
    ["invalid cursor", 400],
    ["expired cursor", 410],
    ["cross-scope cursor", 422]
  ])("maps %s 4xx responses to invalid-query without retry or fallback", async (_case, status) => {
    const fetchMock = vi.fn().mockResolvedValue(response(status, { error: { code: "INVALID_CURSOR" } }));
    expect(await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).toMatchObject({ ok: false, kind: "invalid-query" });
    expectSingleAcceptedRequest(fetchMock);
  });

  it("maps accepted fact source unavailable to unavailable without fallback", async () => {
    const fetchMock = vi.fn().mockResolvedValue(response(503, { detail: "accepted fact source unavailable" }));
    expect(await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).toMatchObject({ ok: false, kind: "unavailable" });
    expectSingleAcceptedRequest(fetchMock);
  });

  it.each([
    ["outer unknown key", { ...validEnvelope, unsupported: true }],
    ["outer meta", { ...validEnvelope, meta: {} }],
    ["data unknown key", { ...validEnvelope, data: { ...validEnvelope.data, diagnostic_payload: {} } }],
    ["page unknown key", { ...validEnvelope, page: { ...validEnvelope.page, dashboard_state: "stale" } }],
    ["missing required item key", { ...validEnvelope, data: { items: [itemMissingRequiredKey] } }]
  ])("maps 2xx malformed response with %s to error without fallback", async (_case, body) => {
    const fetchMock = vi.fn().mockResolvedValue(response(200, body));
    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock);

    expect(result).toMatchObject({ ok: false, kind: "error" });
    expect(result).not.toMatchObject({ ok: false, kind: "invalid-query" });
    expect(result).not.toMatchObject({ ok: false, kind: "unavailable" });
    expect(result).not.toMatchObject({ ok: true, envelope: { items: [] } });
    expectSingleAcceptedRequest(fetchMock);
  });

  it("maps malformed DTO and unexpected responses to error", async () => {
    const malformedFetch = vi.fn().mockResolvedValue(response(200, { data: { items: [{ raw_hex: "deadbeef" }] }, page: { next_cursor: null, limit: 50 } }));
    const unexpectedFetch = vi.fn().mockResolvedValue(response(500, { error: "boom" }));

    await expect(fetchAcceptedStationEvents(validQuery, trustedOrigin(), malformedFetch)).resolves.toMatchObject({ ok: false, kind: "error" });
    await expect(fetchAcceptedStationEvents(validQuery, trustedOrigin(), unexpectedFetch)).resolves.toMatchObject({ ok: false, kind: "error" });
    expectSingleAcceptedRequest(malformedFetch);
    expectSingleAcceptedRequest(unexpectedFetch);
  });

  it.each(["network", "redirect"])("maps %s failures to error with no fallback request", async (kind) => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError(`${kind} failure`));
    await expect(fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).resolves.toMatchObject({ ok: false, kind: "error" });
    expectSingleAcceptedRequest(fetchMock);
  });
});
