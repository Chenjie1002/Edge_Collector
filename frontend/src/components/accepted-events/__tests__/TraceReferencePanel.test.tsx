import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import type { AcceptedStationEventItem } from "../../../lib/acceptedStationEvents/schema";
import { toAcceptedEventsViewModel } from "../../../lib/acceptedStationEvents/viewModel";
import { TraceReferencePanel } from "../TraceReferencePanel";

const item: AcceptedStationEventItem = {
  line_id: "LINE_001",
  plc_id: "PLC_001",
  station_id: "",
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
  fact_key: "sha256:fact",
  content_fingerprint: "sha256:content",
  nok_code: null,
  nok_origin: null,
  nok_detail_code: null,
  nok_detail_source_event_id: null,
  nok_detail_evidence_fact_key: null
};

afterEach(cleanup);

describe("TraceReferencePanel", () => {
  it("renders accepted raw references through explicit null and empty-string display rules", () => {
    const viewModel = toAcceptedEventsViewModel({ items: [item], page: { next_cursor: null, limit: 50 } });
    render(<TraceReferencePanel reference={viewModel.selectedReference} />);

    const trace = screen.getByLabelText("Accepted fact trace references");
    expect(trace.textContent).toContain("sha256:fact");
    expect(trace.textContent).toContain("301");
    expect(trace.textContent).toContain("—");
    expect(trace.textContent).toContain("Empty string");
    expect(trace.textContent).toContain("LINE_001 / PLC_001 / Empty string");
    expect(trace.textContent).not.toMatch(/unknown|raw|debug|payload|work order|product/i);
  });
});
