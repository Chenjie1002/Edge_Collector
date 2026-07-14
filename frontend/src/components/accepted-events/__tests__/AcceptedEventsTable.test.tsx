import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { AcceptedStationEventItem } from "../../../lib/acceptedStationEvents/schema";
import { toAcceptedEventsViewModel } from "../../../lib/acceptedStationEvents/viewModel";
import { AcceptedEventsTable } from "../AcceptedEventsTable";

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
  unit_id: null,
  dmc: "",
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

const cycleComplete: AcceptedStationEventItem = {
  ...stationNok,
  station_id: "",
  event_type: "station_cycle_complete",
  production_result: null,
  fact_key: "sha256:cycle-fact",
  content_fingerprint: "sha256:cycle-content",
  nok_code: null,
  nok_origin: null,
  nok_detail_code: null,
  nok_detail_source_event_id: null,
  nok_detail_evidence_fact_key: null
};

afterEach(cleanup);

describe("AcceptedEventsTable", () => {
  it("renders explicit row-role outcome and null/empty display without unknown", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [stationNok], page: { next_cursor: null, limit: 50 } });
    const { container } = render(<AcceptedEventsTable rows={viewModel.rows} selectedFactKey={stationNok.fact_key} />);

    expect(screen.getByText("WS01")).toBeTruthy();
    expect(screen.getByText("Not applicable — NOK detail companion")).toBeTruthy();
    expect(screen.getByText("—")).toBeTruthy();
    expect(screen.getByText("Empty string")).toBeTruthy();
    expect(screen.queryByText(/unknown/i)).toBeNull();
    expect(container.querySelector("tbody tr")?.className).toBe("is-selected");
    expect(screen.queryByRole("button", { name: "WS01" })).toBeNull();
  });

  it("renders cycle events as not applicable rather than a production outcome", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [cycleComplete], page: { next_cursor: null, limit: 50 } });
    render(<AcceptedEventsTable rows={viewModel.rows} selectedFactKey={cycleComplete.fact_key} />);

    expect(screen.getByText("Not applicable — cycle event")).toBeTruthy();
    expect(screen.getAllByText("Empty string").length).toBeGreaterThanOrEqual(2);
    expect(screen.queryByText(/unknown/i)).toBeNull();
  });
});
