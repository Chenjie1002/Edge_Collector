import { describe, expect, it } from "vitest";
import { toAcceptedEventsViewModel } from "../viewModel";

const item = {
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

describe("accepted station events view model", () => {
  it("builds current-page-only summaries and excludes fallback fields", () => {
    const viewModel = toAcceptedEventsViewModel({
      items: [
        item,
        { ...item, fact_key: "sha256:nok", production_result: "nok", station_id: "WS02", nok_code: "NOK_A" }
      ],
      page: { next_cursor: null, limit: 50 }
    });

    expect(viewModel.summary.label).toMatch(/current page only/i);
    expect(viewModel.summary.totalAcceptedFacts).toBe(2);
    expect(JSON.stringify(viewModel)).not.toMatch(/work_order|\bproduct\b|raw_|debug|diagnostic|candidate|legacy|read_done|ack/i);
  });

  it("does not label accepted_at as freshness, ACK, station freshness, or read_done time", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [item], page: { next_cursor: null, limit: 50 } });

    expect(JSON.stringify(viewModel)).not.toMatch(/freshness|ACK time|station freshness|read_done/i);
    expect(viewModel.rows[0].acceptedAt.label).toBe("Accepted fact timestamp");
  });
});
