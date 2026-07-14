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

type ResponseStub = {
  response: Response;
  text: ReturnType<typeof vi.fn>;
  json: ReturnType<typeof vi.fn>;
};

function response(status: number, body: unknown, rawText?: string): ResponseStub {
  const text = vi.fn().mockResolvedValue(rawText ?? JSON.stringify(body));
  const json = vi.fn().mockResolvedValue(body);
  return {
    response: {
      ok: status >= 200 && status < 300,
      status,
      text,
      json
    } as unknown as Response,
    text,
    json
  };
}

function trustedOrigin(origin = "https://accepted-api.example") {
  const resolution = resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: origin,
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
  it("uses response.text and the raw-text parser for one successful GET request", async () => {
    const stub = response(200, validEnvelope);
    const fetchMock = vi.fn().mockResolvedValue(stub.response);

    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock);

    expect(result).toMatchObject({ ok: true, envelope: { items: [validItem] } });
    expectSingleAcceptedRequest(fetchMock);
    expect(stub.text).toHaveBeenCalledTimes(1);
    expect(stub.json).not.toHaveBeenCalled();

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
  ])("maps %s 4xx responses to invalid-query without reading the body, retry, or fallback", async (_case, status) => {
    const stub = response(status, { error: { code: "INVALID_CURSOR" } });
    const fetchMock = vi.fn().mockResolvedValue(stub.response);

    expect(await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).toMatchObject({ ok: false, kind: "invalid-query" });
    expectSingleAcceptedRequest(fetchMock);
    expect(stub.text).not.toHaveBeenCalled();
    expect(stub.json).not.toHaveBeenCalled();
  });

  it("maps accepted fact source unavailable to unavailable without reading the body or fallback", async () => {
    const stub = response(503, { detail: "accepted fact source unavailable" });
    const fetchMock = vi.fn().mockResolvedValue(stub.response);

    expect(await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).toMatchObject({ ok: false, kind: "unavailable" });
    expectSingleAcceptedRequest(fetchMock);
    expect(stub.text).not.toHaveBeenCalled();
    expect(stub.json).not.toHaveBeenCalled();
  });

  it.each([
    ["outer unknown key", { ...validEnvelope, unsupported: true }],
    ["outer meta", { ...validEnvelope, meta: {} }],
    ["data unknown key", { ...validEnvelope, data: { ...validEnvelope.data, diagnostic_payload: {} } }],
    ["page unknown key", { ...validEnvelope, page: { ...validEnvelope.page, dashboard_state: "stale" } }],
    ["missing required item key", { ...validEnvelope, data: { items: [itemMissingRequiredKey] } }]
  ])("maps 2xx malformed response with %s to a stable error without fallback", async (_case, body) => {
    const stub = response(200, body);
    const fetchMock = vi.fn().mockResolvedValue(stub.response);
    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock);

    expect(result).toEqual({ ok: false, kind: "error", message: "Accepted events response was invalid." });
    expectSingleAcceptedRequest(fetchMock);
    expect(stub.text).toHaveBeenCalledTimes(1);
    expect(stub.json).not.toHaveBeenCalled();
  });

  it.each([
    ["fraction", '"cycle_counter":1.0'],
    ["exponent", '"cycle_counter":1e0'],
    ["rounded boundary fraction", '"cycle_counter":9007199254740991.1']
  ])("rejects a %s numeric lexeme without retry or partial success", async (_name, replacement) => {
    const rawText = JSON.stringify(validEnvelope).replace('"cycle_counter":301', replacement);
    const stub = response(200, validEnvelope, rawText);
    const fetchMock = vi.fn().mockResolvedValue(stub.response);

    expect(await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock)).toEqual({
      ok: false,
      kind: "error",
      message: "Accepted events response was invalid."
    });
    expectSingleAcceptedRequest(fetchMock);
    expect(stub.text).toHaveBeenCalledTimes(1);
    expect(stub.json).not.toHaveBeenCalled();
  });

  it("does not leak raw body, numeric lexeme, parser details, or trusted origin in a parser error", async () => {
    const rawSecret = "RAW-RESPONSE-SECRET";
    const secretOrigin = "https://accepted-api.example";
    const rawText = JSON.stringify({ ...validEnvelope, rawSecret }).replace('"cycle_counter":301', '"cycle_counter":9007199254740991.1');
    const stub = response(200, validEnvelope, rawText);
    const fetchMock = vi.fn().mockResolvedValue(stub.response);

    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(secretOrigin), fetchMock);

    expect(result).toEqual({ ok: false, kind: "error", message: "Accepted events response was invalid." });
    if (!result.ok) {
      expect(result.message).not.toContain(rawSecret);
      expect(result.message).not.toContain("9007199254740991.1");
      expect(result.message).not.toContain(secretOrigin);
      expect(result.message).not.toMatch(/numeric source|JSON|parser|stack/i);
    }
    expectSingleAcceptedRequest(fetchMock);
  });

  it("maps malformed DTO and unexpected 5xx responses without fallback", async () => {
    const malformedStub = response(200, { data: { items: [{ raw_hex: "deadbeef" }] }, page: { next_cursor: null, limit: 50 } });
    const unexpectedStub = response(500, { error: "boom" });
    const malformedFetch = vi.fn().mockResolvedValue(malformedStub.response);
    const unexpectedFetch = vi.fn().mockResolvedValue(unexpectedStub.response);

    await expect(fetchAcceptedStationEvents(validQuery, trustedOrigin(), malformedFetch)).resolves.toEqual({
      ok: false,
      kind: "error",
      message: "Accepted events response was invalid."
    });
    await expect(fetchAcceptedStationEvents(validQuery, trustedOrigin(), unexpectedFetch)).resolves.toMatchObject({ ok: false, kind: "error" });
    expectSingleAcceptedRequest(malformedFetch);
    expectSingleAcceptedRequest(unexpectedFetch);
    expect(unexpectedStub.text).not.toHaveBeenCalled();
  });

  it.each(["network", "redirect"])("maps %s failures to a stable error with no fallback request", async (kind) => {
    const fetchMock = vi.fn().mockRejectedValue(new TypeError(`${kind} failure at https://accepted-api.example/private`));
    const result = await fetchAcceptedStationEvents(validQuery, trustedOrigin(), fetchMock);

    expect(result).toEqual({ ok: false, kind: "error", message: "Accepted events request failed." });
    expectSingleAcceptedRequest(fetchMock);
  });
});
