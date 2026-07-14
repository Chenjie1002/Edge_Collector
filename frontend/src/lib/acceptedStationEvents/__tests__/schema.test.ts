import { describe, expect, it, vi } from "vitest";
import {
  acceptedStationEventFields,
  parseAcceptedStationEventsEnvelope,
  parseAcceptedStationEventsEnvelopeJson
} from "../schema";

const stationResultOkItem = {
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
  accepted_at: "2026-07-05T10:00:01.123456Z",
  fact_key: "sha256:fact",
  content_fingerprint: "sha256:content",
  nok_code: null,
  nok_origin: null,
  nok_detail_code: null,
  nok_detail_source_event_id: null,
  nok_detail_evidence_fact_key: null
};

const stationResultNokItem = {
  ...stationResultOkItem,
  production_result: "nok",
  nok_code: 100,
  nok_origin: "station_result"
};

const stationNokItem = {
  ...stationResultOkItem,
  event_type: "station_nok",
  production_result: null,
  nok_code: 100,
  nok_origin: "station_nok",
  nok_detail_code: 101,
  nok_detail_source_event_id: "PLC_001:WS01:300",
  nok_detail_evidence_fact_key: "sha256:upstream"
};

const cycleStartItem = {
  ...stationResultOkItem,
  event_type: "station_cycle_start",
  production_result: null
};

function validEnvelope(item: unknown = stationResultOkItem) {
  return {
    data: { items: [typeof item === "object" && item !== null && !Array.isArray(item) ? { ...item } : item] },
    page: { next_cursor: null, limit: 50 }
  };
}

function validEnvelopeJson(item: object = stationResultOkItem, limit = 50) {
  return JSON.stringify({ data: { items: [item] }, page: { next_cursor: null, limit } });
}

function replaceNumericToken(rawText: string, field: string, currentValue: number, token: string) {
  const current = `"${field}":${currentValue}`;
  const replacement = `"${field}":${token}`;
  expect(rawText).toContain(current);
  return rawText.replace(current, replacement);
}

function addOwnJsonKey(target: object, key: string) {
  const jsonObject = JSON.parse(`{${JSON.stringify(key)}:"forbidden"}`) as object;
  Object.defineProperties(target, Object.getOwnPropertyDescriptors(jsonObject));
}

function parseWithoutReviverContext(text: string, reviver?: (this: unknown, key: string, value: unknown) => unknown) {
  const originalParse = vi.mocked(JSON.parse).getMockImplementation();
  const parsed = originalParse ? originalParse(text) : JSON.parse(text);
  if (!reviver) return parsed;

  const walk = (holder: Record<string, unknown>, key: string): unknown => {
    const current = holder[key];
    if (current && typeof current === "object") {
      for (const childKey of Object.keys(current)) {
        (current as Record<string, unknown>)[childKey] = walk(current as Record<string, unknown>, childKey);
      }
    }
    return reviver.call(holder, key, current);
  };

  return walk({ "": parsed }, "");
}

describe("accepted station events raw-text schema", () => {
  it.each([
    ["fraction cycle counter", "cycle_counter", 301, "1.0"],
    ["exponent cycle counter", "cycle_counter", 301, "1e0"],
    ["rounded boundary fraction", "cycle_counter", 301, "9007199254740991.1"],
    ["unsafe cycle counter", "cycle_counter", 301, "9007199254740992"],
    ["negative zero cycle counter", "cycle_counter", 301, "-0"],
    ["fraction NOK code", "nok_code", 100, "10.0"],
    ["exponent NOK detail code", "nok_detail_code", 101, "2e0"],
    ["fraction page limit", "limit", 50, "50.0"]
  ])("rejects non-canonical or unsafe numeric source: %s", (_name, field, currentValue, token) => {
    const item = field === "nok_detail_code" ? stationNokItem : field === "nok_code" ? stationResultNokItem : stationResultOkItem;
    const rawText = replaceNumericToken(validEnvelopeJson(item), field, currentValue, token);

    expect(() => parseAcceptedStationEventsEnvelopeJson(rawText)).toThrow(/invalid accepted events response/i);
  });

  it("rejects a numeric-looking string before it can become a cycle counter", () => {
    const rawText = validEnvelopeJson({ ...stationResultOkItem, cycle_counter: "12" });
    expect(() => parseAcceptedStationEventsEnvelopeJson(rawText)).toThrow(/invalid accepted events response/i);
  });

  it.each([
    [0, stationResultOkItem],
    [Number.MAX_SAFE_INTEGER, stationResultOkItem],
    [Number.MIN_SAFE_INTEGER, stationResultOkItem]
  ])("accepts canonical safe cycle counter %s", (cycleCounter, template) => {
    const parsed = parseAcceptedStationEventsEnvelopeJson(validEnvelopeJson({ ...template, cycle_counter: cycleCounter }));
    expect(parsed.items[0].cycle_counter).toBe(cycleCounter);
  });

  it("accepts nullable numeric fields and a canonical page limit", () => {
    const parsed = parseAcceptedStationEventsEnvelopeJson(validEnvelopeJson(stationResultOkItem, 50));
    expect(parsed.items[0].nok_code).toBeNull();
    expect(parsed.items[0].nok_detail_code).toBeNull();
    expect(parsed.page.limit).toBe(50);
  });

  it("fails closed when the runtime JSON parser does not provide source context", () => {
    const originalParse = JSON.parse.bind(JSON);
    const parseSpy = vi.spyOn(JSON, "parse").mockImplementation(((text: string, reviver?: (this: unknown, key: string, value: unknown) => unknown) => {
      const parsed = originalParse(text);
      if (!reviver) return parsed;

      const walk = (holder: Record<string, unknown>, key: string): unknown => {
        const current = holder[key];
        if (current && typeof current === "object") {
          for (const childKey of Object.keys(current)) {
            (current as Record<string, unknown>)[childKey] = walk(current as Record<string, unknown>, childKey);
          }
        }
        return reviver.call(holder, key, current);
      };

      return walk({ "": parsed }, "");
    }) as typeof JSON.parse);

    try {
      expect(() => parseAcceptedStationEventsEnvelopeJson(validEnvelopeJson())).toThrow(/invalid accepted events response/i);
    } finally {
      parseSpy.mockRestore();
    }
  });

  it("does not include raw body or numeric lexeme in a raw-text parse error", () => {
    const rawSecret = "RAW-BODY-SHOULD-NOT-LEAK";
    const rawText = replaceNumericToken(
      validEnvelopeJson({ ...stationResultOkItem, unit_id: rawSecret }),
      "cycle_counter",
      301,
      "9007199254740991.1"
    );

    try {
      parseAcceptedStationEventsEnvelopeJson(rawText);
      throw new Error("expected parser to reject raw body");
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      expect(message).toBe("Invalid accepted events response");
      expect(message).not.toContain(rawSecret);
      expect(message).not.toContain("9007199254740991.1");
    }
  });

  it("rejects the entire response when one item has an invalid numeric token", () => {
    const rawText = JSON.stringify({
      data: { items: [stationResultOkItem, { ...stationResultOkItem, fact_key: "sha256:bad", cycle_counter: 302 }] },
      page: { next_cursor: null, limit: 50 }
    }).replace('"cycle_counter":302', '"cycle_counter":2e0');

    expect(() => parseAcceptedStationEventsEnvelopeJson(rawText)).toThrow(/invalid accepted events response/i);
  });
});

describe("accepted station events typed schema", () => {
  it("admits the exact envelope and typed DTO contract", () => {
    const parsed = parseAcceptedStationEventsEnvelope({
      data: { items: [stationResultOkItem, stationResultNokItem, stationNokItem, cycleStartItem] },
      page: { next_cursor: "opaque", limit: 50 }
    });

    expect(parsed.items).toEqual([stationResultOkItem, stationResultNokItem, stationNokItem, cycleStartItem]);
    expect(parsed.page).toEqual({ next_cursor: "opaque", limit: 50 });
  });

  it("admits empty items and explicit null only on nullable fields", () => {
    expect(parseAcceptedStationEventsEnvelope({ data: { items: [] }, page: { next_cursor: null, limit: 50 } })).toEqual({
      items: [],
      page: { next_cursor: null, limit: 50 }
    });

    expect(parseAcceptedStationEventsEnvelope(validEnvelope(stationResultOkItem)).items[0]).toEqual(stationResultOkItem);
  });

  it.each([
    "line_id",
    "plc_id",
    "station_id",
    "station_type",
    "profile_id",
    "config_hash",
    "config_version",
    "event_type",
    "source_event_id",
    "event_ts",
    "accepted_at",
    "fact_key",
    "content_fingerprint"
  ])("rejects null and non-string values for required string field %s", (field) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, [field]: null }))).toThrow(/invalid/i);
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, [field]: 12 }))).toThrow(/invalid/i);
  });

  it.each(["production_result", "unit_id", "dmc", "nok_origin", "nok_detail_source_event_id", "nok_detail_evidence_fact_key"])(
    "rejects non-string non-null values for nullable string field %s",
    (field) => {
      expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, [field]: 12 }))).toThrow(/invalid/i);
    }
  );

  it.each([
    ["cycle_counter", null],
    ["cycle_counter", "12"],
    ["cycle_counter", 1.5],
    ["cycle_counter", Number.MAX_SAFE_INTEGER + 1],
    ["nok_code", "10"],
    ["nok_code", 1.5],
    ["nok_detail_code", "2"],
    ["nok_detail_code", 2.5]
  ])("rejects invalid numeric field %s=%j", (field, value) => {
    const template = field === "nok_detail_code" ? stationNokItem : field === "nok_code" ? stationResultNokItem : stationResultOkItem;
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...template, [field]: value }))).toThrow(/invalid/i);
  });

  it.each([
    "2026-07-05T10:00:00+00:00",
    "2026-07-05T10:00:00",
    "2026-02-30T10:00:00Z",
    "not-a-time"
  ])("rejects invalid or non-Z UTC timestamp %s", (timestamp) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, event_ts: timestamp }))).toThrow(/event_ts|invalid/i);
  });

  it("keeps event_ts and accepted_at as distinct valid UTC values", () => {
    const parsed = parseAcceptedStationEventsEnvelope(validEnvelope(stationResultOkItem)).items[0];
    expect(parsed.event_ts).toBe("2026-07-05T10:00:00Z");
    expect(parsed.accepted_at).toBe("2026-07-05T10:00:01.123456Z");
  });

  it.each(["station_heartbeat", "unknown_event"])("rejects unsupported event type %s", (eventType) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, event_type: eventType }))).toThrow(/event_type|invalid/i);
  });

  it.each(["unknown", "OK", "failed"])("rejects unsupported production result %s", (productionResult) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, production_result: productionResult }))).toThrow(/production_result|invalid/i);
  });

  it.each([
    ["station_result requires a result", { ...stationResultOkItem, production_result: null }],
    ["station_result NOK requires code", { ...stationResultNokItem, nok_code: null }],
    ["station_result NOK requires origin", { ...stationResultNokItem, nok_origin: null }],
    ["station_result NOK forbids detail", { ...stationResultNokItem, nok_detail_code: 101 }],
    ["station_result non-NOK forbids code", { ...stationResultOkItem, nok_code: 100 }],
    ["station_result non-NOK forbids origin", { ...stationResultOkItem, nok_origin: "station_result" }],
    ["station_nok requires null result", { ...stationNokItem, production_result: "nok" }],
    ["station_nok requires NOK code", { ...stationNokItem, nok_code: null }],
    ["station_nok requires detail code", { ...stationNokItem, nok_detail_code: null }],
    ["station_nok requires detail source event", { ...stationNokItem, nok_detail_source_event_id: null }],
    ["station_nok requires evidence fact", { ...stationNokItem, nok_detail_evidence_fact_key: null }],
    ["cycle event forbids result", { ...cycleStartItem, production_result: "ok" }],
    ["cycle event forbids NOK", { ...cycleStartItem, nok_code: 100 }],
    ["cycle event forbids detail", { ...cycleStartItem, nok_detail_code: 101 }]
  ])("rejects cross-field violation: %s", (_name, item) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope(item))).toThrow(/invalid.*combination|contract/i);
  });

  it.each([
    ["outer unknown", (envelope: Record<string, unknown>) => addOwnJsonKey(envelope, "unsupported")],
    ["outer meta", (envelope: Record<string, unknown>) => addOwnJsonKey(envelope, "meta")],
    ["data unknown", (envelope: Record<string, unknown>) => addOwnJsonKey(envelope.data as object, "raw")],
    ["page unknown", (envelope: Record<string, unknown>) => addOwnJsonKey(envelope.page as object, "dashboard_state")],
    ["item unknown", (envelope: Record<string, unknown>) => addOwnJsonKey((envelope.data as { items: object[] }).items[0], "work_order")]
  ])("rejects %s exact-key violation", (_name, mutate) => {
    const envelope = validEnvelope() as Record<string, unknown>;
    mutate(envelope);
    expect(() => parseAcceptedStationEventsEnvelope(envelope)).toThrow(/forbidden|unsupported/i);
  });

  it.each(acceptedStationEventFields)("rejects a missing required item key: %s", (field) => {
    const item = { ...stationResultOkItem } as Record<string, unknown>;
    delete item[field];
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope(item))).toThrow(/missing|required/i);
  });

  it.each([
    ["raw payload", { raw_payload: { value: "raw" } }],
    ["raw hex", { raw_hex: "deadbeef" }],
    ["adapter reason", { adapter_reason: "diagnostic" }],
    ["candidate context", { candidate_context: { station_id: "WS01" } }],
    ["read_done", { read_done: true }],
    ["quality/Pareto", { quality_pareto_input: { code: 100 } }],
    ["work order", { work_order: "WO-1" }],
    ["product", { product: "SKU-1" }]
  ])("retains rejection of forbidden leakage fixture: %s", (_name, forbiddenFields) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...stationResultOkItem, ...forbiddenFields }))).toThrow(/forbidden|unsupported/i);
  });

  it.each([null, [], "envelope", 1, true])("rejects invalid envelope shape: %j", (value) => {
    expect(() => parseAcceptedStationEventsEnvelope(value)).toThrow(/object|invalid/i);
  });

  it.each(["50", null, 1.5, 0, 501, Number.MAX_SAFE_INTEGER + 1])("rejects invalid limit value: %j", (limit) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data: { items: [] }, page: { next_cursor: null, limit } })).toThrow(/invalid/i);
  });
});
