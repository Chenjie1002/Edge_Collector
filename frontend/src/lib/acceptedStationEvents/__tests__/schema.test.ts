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

  it("rejects raw, debug, diagnostic, candidate, legacy, work order, and product fields", () => {
    const forbiddenPayload = {
      ...allowedItem,
      raw_payload: { value: "raw" },
      raw_hex: "deadbeef",
      adapter_reason: "diagnostic",
      candidate_context: {},
      production_snapshot: {},
      work_order: "WO-1",
      product: "SKU-1"
    };

    expect(() =>
      parseAcceptedStationEventsEnvelope({
        data: { items: [forbiddenPayload] },
        page: { next_cursor: null, limit: 50 }
      })
    ).toThrow(/forbidden/i);
  });
});
