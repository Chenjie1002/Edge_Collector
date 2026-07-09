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

  it("does not carry bypassed forbidden keys into rows, summary, or selected evidence", () => {
    const bypassItem = {
      ...item,
      production_result: "nok",
      nok_code: "NOK_A",
      raw_payload: { value: "raw" },
      raw_hex: "deadbeef",
      adapter_reason: "diagnostic",
      candidate_context: { production_result: "ok" },
      read_done: true,
      ack_status: "ACKED",
      work_order: "WO-1",
      product: "SKU-1"
    } as any;

    const viewModel = toAcceptedEventsViewModel({ items: [bypassItem], page: { next_cursor: null, limit: 50 } });
    const rendered = JSON.stringify({
      rows: viewModel.rows,
      summary: viewModel.summary,
      selectedEvidence: viewModel.selectedEvidence
    });

    expect(rendered).not.toMatch(/raw_payload|raw_hex|adapter_reason|candidate_context|read_done|ack_status|work_order|\bproduct\b|WO-1|SKU-1/i);
    expect(viewModel.selectedEvidence?.productionResult).toBe("nok");
    expect(viewModel.selectedEvidence?.nokCode).toBe("NOK_A");
  });

  it("does not carry nested or renamed bypass leakage into production render evidence", () => {
    const bypassItem = {
      ...item,
      production_result: "nok",
      nok_code: "NOK_A",
      rawPayload: { value: "LEAK_RAW_PAYLOAD_VALUE" },
      rawHex: "LEAK_RAW_HEX_VALUE",
      rawSampleId: "LEAK_RAW_SAMPLE_ID_VALUE",
      adapterReason: "LEAK_ADAPTER_REASON_VALUE",
      collectorState: "LEAK_COLLECTOR_STATE_VALUE",
      readDone: true,
      ackStatus: "LEAK_ACK_STATUS_VALUE",
      qualityParetoInput: { code: "LEAK_QUALITY_PARETO_VALUE" },
      dashboardState: { status: "LEAK_DASHBOARD_STATE_VALUE" },
      workOrder: "LEAK_WORK_ORDER_VALUE",
      productCode: "LEAK_PRODUCT_CODE_VALUE",
      production_quality: "LEAK_PRODUCTION_QUALITY_VALUE",
      production_defect: "LEAK_PRODUCTION_DEFECT_VALUE",
      production_pareto: "LEAK_PRODUCTION_PARETO_VALUE",
      result_detail: "LEAK_RESULT_DETAIL_VALUE",
      defect_code: "LEAK_DEFECT_CODE_VALUE",
      quality_state: "LEAK_QUALITY_STATE_VALUE",
      diagnostic_payload: {
        production_result: "LEAK_DIAGNOSTIC_RESULT_VALUE",
        fact_key: "LEAK_DIAGNOSTIC_FACT_VALUE"
      },
      review_payload: {
        nok_code: "LEAK_REVIEW_NOK_VALUE",
        source_event_id: "LEAK_REVIEW_SOURCE_VALUE"
      },
      audit_payload: {
        fact_key: "LEAK_AUDIT_FACT_VALUE",
        production_result: "LEAK_AUDIT_RESULT_VALUE"
      },
      candidate_payload: {
        production_result: "LEAK_CANDIDATE_RESULT_VALUE",
        nok_code: "LEAK_CANDIDATE_NOK_VALUE"
      },
      raw_payload: {
        fact_key: "LEAK_RAW_FACT_VALUE",
        source_event_id: "LEAK_RAW_SOURCE_VALUE"
      }
    } as any;

    const viewModel = toAcceptedEventsViewModel({ items: [bypassItem], page: { next_cursor: null, limit: 50 } });
    const rendered = JSON.stringify({
      rows: viewModel.rows,
      summary: viewModel.summary,
      selectedEvidence: viewModel.selectedEvidence
    });

    expect(rendered).not.toMatch(
      /rawPayload|rawHex|rawSampleId|adapterReason|collectorState|readDone|ackStatus|qualityParetoInput|dashboardState|workOrder|productCode/i
    );
    expect(rendered).not.toMatch(
      /production_quality|production_defect|production_pareto|result_detail|defect_code|quality_state|diagnostic_payload|review_payload|audit_payload|candidate_payload|raw_payload/i
    );
    expect(rendered).not.toMatch(/LEAK_/);
    expect(viewModel.rows[0].productionResult).toBe("nok");
    expect(viewModel.selectedEvidence?.nokCode).toBe("NOK_A");
    expect(viewModel.selectedEvidence?.factKey).toBe("sha256:fact");
    expect(viewModel.selectedEvidence?.sourceEventId).toBe("PLC_001:WS01:301");
  });
});
