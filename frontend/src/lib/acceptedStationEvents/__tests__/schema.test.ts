import { describe, expect, it } from "vitest";
import { acceptedStationEventFields, parseAcceptedStationEventsEnvelope } from "../schema";

const allowedItem = {
  line_id: "LINE_001",
  plc_id: "PLC_001",
  station_id: "WS01",
  station_type: "ASSEMBLY",
  profile_id: "normal",
  config_hash: "sha256:abc",
  config_version: "2026.07.05.1",
  event_type: "station_result",
  production_result: "nok",
  unit_id: "U-001",
  dmc: "DMC-001",
  cycle_counter: 301,
  source_event_id: "PLC_001:WS01:301",
  event_ts: "2026-07-05T10:00:00Z",
  accepted_at: "2026-07-05T10:00:01Z",
  fact_key: "sha256:fact",
  content_fingerprint: "sha256:content",
  nok_code: "NOK_A",
  nok_origin: "station_result",
  nok_detail_code: "D01",
  nok_detail_source_event_id: "PLC_001:WS00:300",
  nok_detail_evidence_fact_key: "sha256:evidence"
};

function validEnvelope(item: unknown = allowedItem) {
  return {
    data: { items: [typeof item === "object" && item !== null && !Array.isArray(item) ? { ...item } : item] },
    page: { next_cursor: null, limit: 50 }
  };
}

function addOwnJsonKey(target: object, key: string) {
  const jsonObject = JSON.parse(`{${JSON.stringify(key)}:"forbidden"}`) as object;
  Object.defineProperties(target, Object.getOwnPropertyDescriptors(jsonObject));
}

describe("accepted station events schema", () => {
  it("admits only the exact envelope and complete DTO allowlist", () => {
    const parsed = parseAcceptedStationEventsEnvelope({
      data: { items: [allowedItem] },
      page: { next_cursor: "opaque", limit: 50 }
    });

    expect(parsed.items[0]).toEqual(allowedItem);
    expect(parsed.page).toEqual({ next_cursor: "opaque", limit: 50 });
  });

  it("admits empty items and explicit null values without treating them as missing", () => {
    expect(parseAcceptedStationEventsEnvelope({ data: { items: [] }, page: { next_cursor: null, limit: 50 } })).toEqual({
      items: [],
      page: { next_cursor: null, limit: 50 }
    });

    const nullableItem = { ...allowedItem, nok_code: null, nok_origin: null, nok_detail_code: null };
    expect(parseAcceptedStationEventsEnvelope(validEnvelope(nullableItem)).items[0]).toEqual(nullableItem);
  });

  it.each(acceptedStationEventFields)("preserves explicit null for required item key: %s", (field) => {
    const item = { ...allowedItem, [field]: null };
    const parsedItem = parseAcceptedStationEventsEnvelope(validEnvelope(item)).items[0];

    expect(Object.prototype.hasOwnProperty.call(parsedItem, field)).toBe(true);
    expect(Object.keys(parsedItem)).toHaveLength(acceptedStationEventFields.length);
    expect(parsedItem[field]).toBeNull();
    expect(parsedItem).toEqual(item);
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

  it.each([
    ["data", (envelope: Record<string, unknown>) => delete envelope.data],
    ["page", (envelope: Record<string, unknown>) => delete envelope.page],
    ["items", (envelope: Record<string, unknown>) => delete (envelope.data as Record<string, unknown>).items],
    ["next_cursor", (envelope: Record<string, unknown>) => delete (envelope.page as Record<string, unknown>).next_cursor],
    ["limit", (envelope: Record<string, unknown>) => delete (envelope.page as Record<string, unknown>).limit]
  ])("rejects missing required %s key", (_name, mutate) => {
    const envelope = validEnvelope() as Record<string, unknown>;
    mutate(envelope);
    expect(() => parseAcceptedStationEventsEnvelope(envelope)).toThrow(/missing|required/i);
  });

  it.each(acceptedStationEventFields)("rejects a missing required item key: %s", (field) => {
    const item = { ...allowedItem } as Record<string, unknown>;
    delete item[field];

    expect(Object.keys(item)).toHaveLength(acceptedStationEventFields.length - 1);
    expect(acceptedStationEventFields.filter((candidate) => candidate !== field).every((candidate) => candidate in item)).toBe(true);
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope(item))).toThrow(/missing|required/i);
  });

  it.each([
    ["raw_payload", { raw_payload: { value: "raw" } }],
    ["raw_hex", { raw_hex: "deadbeef" }],
    ["raw_sample_id", { raw_sample_id: "raw-1" }],
    ["raw bytes", { raw_bytes: [222, 173, 190, 239] }],
    ["decoded/source normalized candidate payload", { normalized_candidate_payload: { production_result: "ok" } }],
    ["adapter disposition", { adapter_disposition: "accepted" }],
    ["adapter reason", { adapter_reason: "diagnostic" }],
    ["adapter phase", { adapter_phase: "projection" }],
    ["candidate context", { candidate_context: { station_id: "WS01" } }],
    ["raw-normalized comparison context", { raw_normalized_comparison_context: { diff: [] } }],
    ["decoder errors", { decoder_errors: ["RAW_PARSE_ERROR"] }],
    ["diagnostic payloads", { diagnostic_payload: { code: "ADAPTER_REJECTED" } }],
    ["review payloads", { review_payload: { reviewer: "dq" } }],
    ["audit payloads", { audit_payload: { raw_hex: "deadbeef" } }],
    ["ack_status", { ack_status: "ACKED" }],
    ["read_done", { read_done: true }],
    ["collector_state", { collector_state: "STALE" }],
    ["quality_pareto_input", { quality_pareto_input: { code: "NOK_A" } }],
    ["dashboard_state", { dashboard_state: { status: "fresh" } }],
    ["bare result", { result: "ok" }],
    ["bare defect", { defect: "D01" }],
    ["bare quality", { quality: "good" }],
    ["bare pareto", { pareto: "NOK_A" }],
    ["work_order", { work_order: "WO-1" }],
    ["product", { product: "SKU-1" }]
  ])("retains rejection of forbidden leakage fixture: %s", (_name, forbiddenFields) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...allowedItem, ...forbiddenFields }))).toThrow(/forbidden|unsupported/i);
  });

  it.each([
    ["camelCase rawPayload", { rawPayload: { value: "LEAK_RAW_PAYLOAD" } }],
    ["camelCase rawHex", { rawHex: "LEAK_RAW_HEX" }],
    ["camelCase rawSampleId", { rawSampleId: "LEAK_RAW_SAMPLE_ID" }],
    ["camelCase adapterReason", { adapterReason: "LEAK_ADAPTER_REASON" }],
    ["camelCase collectorState", { collectorState: "LEAK_COLLECTOR_STATE" }],
    ["camelCase readDone", { readDone: true }],
    ["camelCase ackStatus", { ackStatus: "LEAK_ACK_STATUS" }],
    ["camelCase qualityParetoInput", { qualityParetoInput: { code: "LEAK_QUALITY_PARETO" } }],
    ["camelCase dashboardState", { dashboardState: { status: "LEAK_DASHBOARD_STATE" } }],
    ["camelCase workOrder", { workOrder: "LEAK_WORK_ORDER" }],
    ["camelCase productCode", { productCode: "LEAK_PRODUCT_CODE" }],
    ["production_quality alias", { production_quality: "LEAK_PRODUCTION_QUALITY" }],
    ["production_defect alias", { production_defect: "LEAK_PRODUCTION_DEFECT" }],
    ["production_pareto alias", { production_pareto: "LEAK_PRODUCTION_PARETO" }],
    ["result_detail alias", { result_detail: "LEAK_RESULT_DETAIL" }],
    ["defect_code alias", { defect_code: "LEAK_DEFECT_CODE" }],
    ["quality_state alias", { quality_state: "LEAK_QUALITY_STATE" }],
    ["nested diagnostic accepted-looking fields", { diagnostic_payload: { production_result: "LEAK_DIAGNOSTIC_RESULT", fact_key: "LEAK_DIAGNOSTIC_FACT" } }],
    ["nested review accepted-looking fields", { review_payload: { nok_code: "LEAK_REVIEW_NOK", source_event_id: "LEAK_REVIEW_SOURCE" } }],
    ["nested audit accepted-looking fields", { audit_payload: { fact_key: "LEAK_AUDIT_FACT", production_result: "LEAK_AUDIT_RESULT" } }],
    ["nested candidate accepted-looking fields", { candidate_payload: { production_result: "LEAK_CANDIDATE_RESULT", nok_code: "LEAK_CANDIDATE_NOK" } }],
    ["nested raw accepted-looking fields", { raw_payload: { fact_key: "LEAK_RAW_FACT", source_event_id: "LEAK_RAW_SOURCE" } }]
  ])("retains rejection of nested or renamed forbidden leakage fixture: %s", (_name, forbiddenFields) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...allowedItem, ...forbiddenFields }))).toThrow(/forbidden|unsupported/i);
  });

  it.each([
    ["item raw evidence", "item", "raw_payload"],
    ["item candidate evidence", "item", "candidate_payload"],
    ["item diagnostic evidence", "item", "diagnostic_payload"],
    ["item review evidence", "item", "review_payload"],
    ["item audit evidence", "item", "audit_payload"],
    ["item ACK/read_done", "item", "read_done"],
    ["item collector evidence", "item", "collector_state"],
    ["item quality/Pareto", "item", "quality_pareto_input"],
    ["item dashboard evidence", "item", "dashboard_state"],
    ["item camelCase alias", "item", "rawPayload"],
    ["item accepted-looking nested field", "item", "accepted_fact"],
    ["item work order", "item", "work_order"],
    ["item product", "item", "product"],
    ["data raw evidence", "data", "raw"],
    ["data diagnostic evidence", "data", "diagnostic_payload"],
    ["page dashboard evidence", "page", "dashboard_state"],
    ["page Pareto evidence", "page", "quality_pareto_input"],
    ["outer review evidence", "outer", "review_payload"],
    ["outer audit evidence", "outer", "audit_payload"]
  ])("rejects unsupported evidence at %s", (_name, level, key) => {
    const envelope = validEnvelope() as Record<string, unknown>;
    const target =
      level === "outer"
        ? envelope
        : level === "data"
          ? (envelope.data as object)
          : level === "page"
            ? (envelope.page as object)
            : ((envelope.data as { items: object[] }).items[0] as object);
    addOwnJsonKey(target, key);
    expect(() => parseAcceptedStationEventsEnvelope(envelope)).toThrow(/forbidden|unsupported/i);
  });

  it.each(["", "__proto__", "prototype", "constructor"])("rejects prototype-looking own JSON key %s at every layer", (key) => {
    for (const level of ["outer", "data", "page", "item"] as const) {
      const envelope = validEnvelope() as Record<string, unknown>;
      const target =
        level === "outer"
          ? envelope
          : level === "data"
            ? (envelope.data as object)
            : level === "page"
              ? (envelope.page as object)
              : ((envelope.data as { items: object[] }).items[0] as object);
      addOwnJsonKey(target, key);
      expect(Object.prototype.hasOwnProperty.call(target, key)).toBe(true);
      expect(() => parseAcceptedStationEventsEnvelope(envelope)).toThrow(/forbidden|unsupported/i);
    }
  });

  it.each([null, [], "envelope", 1, true])("rejects invalid envelope shape: %j", (value) => {
    expect(() => parseAcceptedStationEventsEnvelope(value)).toThrow(/object|invalid/i);
  });

  it.each([null, [], "data", 1, true])("rejects invalid data shape: %j", (data) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data, page: { next_cursor: null, limit: 50 } })).toThrow(/object|invalid/i);
  });

  it.each([null, [], "page", 1, true])("rejects invalid page shape: %j", (page) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data: { items: [] }, page })).toThrow(/object|invalid/i);
  });

  it.each([null, {}, "items", 1, true])("rejects non-array data.items: %j", (items) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data: { items }, page: { next_cursor: null, limit: 50 } })).toThrow(/array|invalid/i);
  });

  it.each([null, [], "item", 1, true])("rejects invalid item shape: %j", (item) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope(item))).toThrow(/object|invalid/i);
  });

  it.each([{}, [], true, undefined])("rejects invalid item field value: %j", (fieldValue) => {
    expect(() => parseAcceptedStationEventsEnvelope(validEnvelope({ ...allowedItem, line_id: fieldValue }))).toThrow(/invalid/i);
  });

  it.each([{}, [], 1, true, undefined])("rejects invalid next_cursor value: %j", (nextCursor) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data: { items: [] }, page: { next_cursor: nextCursor, limit: 50 } })).toThrow(/invalid/i);
  });

  it.each(["50", null, 1.5, 0, 501])("rejects invalid limit value: %j", (limit) => {
    expect(() => parseAcceptedStationEventsEnvelope({ data: { items: [] }, page: { next_cursor: null, limit } })).toThrow(/invalid/i);
  });
});
