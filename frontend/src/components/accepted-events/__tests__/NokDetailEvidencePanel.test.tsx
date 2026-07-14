import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { AcceptedStationEventItem } from "../../../lib/acceptedStationEvents/schema";
import { toAcceptedEventsViewModel } from "../../../lib/acceptedStationEvents/viewModel";
import { NokDetailEvidencePanel } from "../NokDetailEvidencePanel";

const stationNok: AcceptedStationEventItem = {
  line_id: "LINE_001",
  plc_id: "PLC_001",
  station_id: "WS01",
  station_type: "ASSEMBLY",
  profile_id: "normal",
  config_hash: "sha256:abc",
  config_version: "2026.07.05.1",
  event_type: "station_nok",
  production_result: null,
  unit_id: "U-001",
  dmc: "DMC-001",
  cycle_counter: 301,
  source_event_id: "PLC_001:WS01:301-detail",
  event_ts: "2026-07-05T10:00:00Z",
  accepted_at: "2026-07-05T10:00:01Z",
  fact_key: "sha256:detail-fact",
  content_fingerprint: "sha256:detail-content",
  nok_code: 100,
  nok_origin: "station_nok",
  nok_detail_code: 101,
  nok_detail_source_event_id: "PLC_001:WS01:301",
  nok_detail_evidence_fact_key: "sha256:outcome-fact"
};

const stationResultOk: AcceptedStationEventItem = {
  ...stationNok,
  event_type: "station_result",
  production_result: "ok",
  fact_key: "sha256:ok-fact",
  content_fingerprint: "sha256:ok-content",
  nok_code: null,
  nok_origin: null,
  nok_detail_code: null,
  nok_detail_source_event_id: null,
  nok_detail_evidence_fact_key: null
};

afterEach(cleanup);

describe("NokDetailEvidencePanel", () => {
  it("labels a station_nok row as a detail companion bound to its accepted fact", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [stationNok], page: { next_cursor: null, limit: 50 } });
    render(<NokDetailEvidencePanel evidence={viewModel.selectedEvidence} />);

    const panel = screen.getByLabelText("Accepted NOK detail evidence");
    expect(panel.textContent).toContain("station_nok detail companion");
    expect(panel.textContent).toContain("Not applicable — NOK detail companion");
    expect(panel.textContent).toContain("100");
    expect(panel.textContent).toContain("101");
    expect(panel.textContent).toContain("sha256:outcome-fact");
    expect(panel.textContent).toContain("Fact reference sha256:detail-fact");
    expect(panel.textContent).not.toMatch(/unknown|adapter|raw|decoder|diagnostic/i);
  });

  it("shows explicit null placeholders for a station_result outcome without inventing NOK detail", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [stationResultOk], page: { next_cursor: null, limit: 50 } });
    render(<NokDetailEvidencePanel evidence={viewModel.selectedEvidence} />);

    const panel = screen.getByLabelText("Accepted NOK detail evidence");
    expect(panel.textContent).toContain("station_result outcome");
    expect(panel.textContent).toContain("ok");
    expect(screen.getAllByText("—").length).toBeGreaterThanOrEqual(5);
    expect(panel.textContent).not.toMatch(/unknown|adapter|raw|decoder|diagnostic/i);
  });
});
