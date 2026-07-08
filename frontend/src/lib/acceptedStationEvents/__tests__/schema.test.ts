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
});
