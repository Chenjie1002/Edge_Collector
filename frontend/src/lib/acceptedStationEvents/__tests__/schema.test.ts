import { describe, expect, it } from "vitest";
import { parseAcceptedStationEventsEnvelope } from "../schema";

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

describe("accepted station events schema", () => {
  it("admits the accepted fact DTO allowlist", () => {
    const parsed = parseAcceptedStationEventsEnvelope({
      data: { items: [allowedItem] },
      page: { next_cursor: "opaque", limit: 50 }
    });

    expect(parsed.items[0]).toEqual(allowedItem);
    expect(parsed.page.next_cursor).toBe("opaque");
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
  ])("rejects forbidden leakage fixture: %s", (_name, forbiddenFields) => {
    expect(() =>
      parseAcceptedStationEventsEnvelope({
        data: { items: [{ ...allowedItem, ...forbiddenFields }] },
        page: { next_cursor: null, limit: 50 }
      })
    ).toThrow(/forbidden/i);
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
    [
      "nested diagnostic accepted-looking fields",
      { diagnostic_payload: { production_result: "LEAK_DIAGNOSTIC_RESULT", fact_key: "LEAK_DIAGNOSTIC_FACT" } }
    ],
    [
      "nested review accepted-looking fields",
      { review_payload: { nok_code: "LEAK_REVIEW_NOK", source_event_id: "LEAK_REVIEW_SOURCE" } }
    ],
    [
      "nested audit accepted-looking fields",
      { audit_payload: { fact_key: "LEAK_AUDIT_FACT", production_result: "LEAK_AUDIT_RESULT" } }
    ],
    [
      "nested candidate accepted-looking fields",
      { candidate_payload: { production_result: "LEAK_CANDIDATE_RESULT", nok_code: "LEAK_CANDIDATE_NOK" } }
    ],
    [
      "nested raw accepted-looking fields",
      { raw_payload: { fact_key: "LEAK_RAW_FACT", source_event_id: "LEAK_RAW_SOURCE" } }
    ]
  ])("rejects nested or renamed forbidden leakage fixture: %s", (_name, forbiddenFields) => {
    expect(() =>
      parseAcceptedStationEventsEnvelope({
        data: { items: [{ ...allowedItem, ...forbiddenFields }] },
        page: { next_cursor: null, limit: 50 }
      })
    ).toThrow(/forbidden/i);
  });

  it("does not return envelope, data, or page-level forbidden payloads", () => {
    const parsed = parseAcceptedStationEventsEnvelope({
      data: {
        items: [allowedItem],
        rawPayload: "LEAK_DATA_RAW_PAYLOAD",
        diagnostic_payload: { fact_key: "LEAK_DATA_FACT" }
      },
      page: {
        next_cursor: null,
        limit: 50,
        dashboardState: "LEAK_PAGE_DASHBOARD_STATE",
        quality_pareto_input: "LEAK_PAGE_QUALITY_PARETO"
      },
      review_payload: { production_result: "LEAK_ENVELOPE_RESULT" },
      audit_payload: { source_event_id: "LEAK_ENVELOPE_SOURCE" }
    });
    const parsedJson = JSON.stringify(parsed);

    expect(parsed).toEqual({ items: [allowedItem], page: { next_cursor: null, limit: 50 } });
    expect(parsedJson).not.toMatch(
      /rawPayload|diagnostic_payload|dashboardState|quality_pareto_input|review_payload|audit_payload|LEAK_/i
    );
  });
});
