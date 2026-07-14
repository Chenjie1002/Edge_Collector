import { describe, expect, it } from "vitest";
import type { AcceptedStationEventItem } from "../schema";
import { toAcceptedEventsViewModel } from "../viewModel";

const stationResultOk: AcceptedStationEventItem = {
  line_id: "LINE_001",
  plc_id: "PLC_001",
  station_id: "WS01",
  station_type: "ASSEMBLY",
  profile_id: "normal",
  config_hash: "sha256:abc",
  config_version: "2026.07.05.1",
  event_type: "station_result",
  production_result: "ok",
  unit_id: null,
  dmc: "",
  cycle_counter: 301,
  source_event_id: "PLC_001:WS01:301",
  event_ts: "2026-07-05T10:00:00Z",
  accepted_at: "2026-07-05T10:00:01Z",
  fact_key: "sha256:fact-ok",
  content_fingerprint: "sha256:content-ok",
  nok_code: null,
  nok_origin: null,
  nok_detail_code: null,
  nok_detail_source_event_id: null,
  nok_detail_evidence_fact_key: null
};

const stationResultNok: AcceptedStationEventItem = {
  ...stationResultOk,
  station_id: "WS02",
  production_result: "nok",
  fact_key: "sha256:fact-nok",
  content_fingerprint: "sha256:content-nok",
  nok_code: 100,
  nok_origin: "station_result"
};

const stationNok: AcceptedStationEventItem = {
  ...stationResultOk,
  station_id: "WS03",
  event_type: "station_nok",
  production_result: null,
  fact_key: "sha256:fact-detail",
  content_fingerprint: "sha256:content-detail",
  nok_code: 100,
  nok_origin: "station_nok",
  nok_detail_code: 101,
  nok_detail_source_event_id: "PLC_001:WS03:300",
  nok_detail_evidence_fact_key: "sha256:fact-nok"
};

const cycleStart: AcceptedStationEventItem = {
  ...stationResultOk,
  station_id: "",
  event_type: "station_cycle_start",
  production_result: null,
  fact_key: "sha256:fact-cycle",
  content_fingerprint: "sha256:content-cycle"
};

function envelope(items: AcceptedStationEventItem[]) {
  return { items, page: { next_cursor: null, limit: 50 } };
}

describe("accepted station events view model", () => {
  it("retains typed raw values separately from null and empty-string display values", () => {
    const viewModel = toAcceptedEventsViewModel(envelope([stationResultOk]));
    const row = viewModel.rows[0];

    expect(row.sourceItem).toEqual(stationResultOk);
    expect(row.unitId).toEqual({ raw: null, text: "—", kind: "null" });
    expect(row.dmc).toEqual({ raw: "", text: "Empty string", kind: "empty-string" });
    expect(row.productionResult).toEqual({ raw: "ok", text: "ok", kind: "value" });
    expect(row.factKey).toBe(stationResultOk.fact_key);
    expect(stationResultOk.unit_id).toBeNull();
    expect(stationResultOk.dmc).toBe("");
  });

  it("derives explicit outcome display by row role without changing raw production_result", () => {
    const viewModel = toAcceptedEventsViewModel(envelope([stationResultOk, stationNok, cycleStart]));

    expect(viewModel.rows[0].productionResult).toEqual({ raw: "ok", text: "ok", kind: "value" });
    expect(viewModel.rows[1].productionResult).toEqual({
      raw: null,
      text: "Not applicable — NOK detail companion",
      kind: "not-applicable"
    });
    expect(viewModel.rows[2].productionResult).toEqual({
      raw: null,
      text: "Not applicable — cycle event",
      kind: "not-applicable"
    });
    expect(viewModel.rows[1].sourceItem.production_result).toBeNull();
    expect(viewModel.rows[2].sourceItem.production_result).toBeNull();
  });

  it("counts production results only for station_result while retaining all accepted rows in the current-page total", () => {
    const viewModel = toAcceptedEventsViewModel(envelope([stationResultOk, stationResultNok, stationNok, cycleStart]));

    expect(viewModel.summary.label).toBe("Current page only");
    expect(viewModel.summary.totalAcceptedFacts).toBe(4);
    expect(viewModel.summary.byResult).toEqual({ ok: 1, nok: 1 });
    expect(viewModel.summary.byResult).not.toHaveProperty("Not applicable — NOK detail companion");
    expect(viewModel.summary.byResult).not.toHaveProperty("Not applicable — cycle event");
    expect(viewModel.summary.byStation).toEqual({ WS01: 1, WS02: 1, WS03: 1, "": 1 });
  });

  it("derives table, NOK/detail, and trace data from the same selected raw item and fact_key", () => {
    const viewModel = toAcceptedEventsViewModel(
      envelope([stationResultOk, stationResultNok, stationNok]),
      stationNok.fact_key
    );

    const selectedRow = viewModel.rows.find((row) => row.factKey === stationNok.fact_key);
    expect(selectedRow?.sourceItem).toEqual(stationNok);
    expect(viewModel.selectedEvidence?.sourceItem).toBe(selectedRow?.sourceItem);
    expect(viewModel.selectedReference?.sourceItem).toBe(selectedRow?.sourceItem);
    expect(viewModel.selectedEvidence?.factKey).toBe(stationNok.fact_key);
    expect(viewModel.selectedReference?.factKey).toBe(stationNok.fact_key);
    expect(viewModel.selectedEvidence?.rowRole).toBe("station_nok detail companion");
    expect(viewModel.selectedEvidence?.productionResult.text).toBe("Not applicable — NOK detail companion");
    expect(viewModel.selectedEvidence?.nokDetailEvidenceFactKey.raw).toBe(stationNok.nok_detail_evidence_fact_key);
  });

  it("falls back to the first item without converting its fact_key", () => {
    const viewModel = toAcceptedEventsViewModel(envelope([stationResultOk, stationResultNok]));

    expect(viewModel.selectedEvidence?.sourceItem).toEqual(stationResultOk);
    expect(viewModel.selectedReference?.sourceItem).toBe(viewModel.selectedEvidence?.sourceItem);
    expect(viewModel.selectedEvidence?.factKey).toBe(stationResultOk.fact_key);
  });

  it("keeps accepted_at labelled only as accepted fact timestamp", () => {
    const viewModel = toAcceptedEventsViewModel(envelope([stationResultOk]));

    expect(viewModel.rows[0].acceptedAt.label).toBe("Accepted fact timestamp");
    expect(viewModel.rows[0].acceptedAt.raw).toBe(stationResultOk.accepted_at);
    expect(JSON.stringify(viewModel)).not.toMatch(/freshness|ACK time|station freshness|read_done/i);
  });

  it("does not carry bypassed forbidden keys into rows, summary, evidence, or references", () => {
    const bypassItem = {
      ...stationResultNok,
      raw_payload: { value: "raw" },
      raw_hex: "deadbeef",
      adapter_reason: "diagnostic",
      candidate_context: { production_result: "ok" },
      read_done: true,
      ack_status: "ACKED",
      work_order: "WO-1",
      product: "SKU-1"
    } as AcceptedStationEventItem;

    const viewModel = toAcceptedEventsViewModel(envelope([bypassItem]));
    const rendered = JSON.stringify(viewModel);

    expect(rendered).not.toMatch(/raw_payload|raw_hex|adapter_reason|candidate_context|read_done|ack_status|work_order|\bproduct\b|WO-1|SKU-1/i);
    expect(viewModel.selectedEvidence?.productionResult.raw).toBe("nok");
    expect(viewModel.selectedEvidence?.nokCode.raw).toBe(100);
  });
});
