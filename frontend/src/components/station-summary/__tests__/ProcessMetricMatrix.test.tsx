import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { ProcessMetricsPanelViewModel } from "../../../lib/stationSummary/viewModel";
import { ProcessMetricMatrix } from "../ProcessMetricMatrix";

const processMetrics: ProcessMetricsPanelViewModel = {
  sourceLabel: "trusted Process Metrics route",
  status: "PARTIAL",
  scopeLabel: "LINE_001 / WS01",
  windowLabel: "2026-07-05T00:00:00Z → 2026-07-05T08:00:00Z [from,to)",
  reason: "accepted facts selected",
  sourceAuthority: "production_accepted_station_event_fact",
  metrics: [
    {
      name: "accepted_event_count",
      unit: "events",
      countingUnit: "event-count",
      status: "SUPPORTED",
      reason: "accepted facts selected",
      source: "production_accepted_station_event_fact",
      numericValueAllowed: true,
      valueText: "2"
    },
    {
      name: "full_oee",
      unit: "ratio",
      countingUnit: "unavailable",
      status: "UNSUPPORTED",
      reason: "required A/P authority absent",
      source: "not-accepted",
      numericValueAllowed: false,
      valueText: "No numeric value authorized"
    }
  ],
  message: undefined
};

describe("ProcessMetricMatrix", () => {
  it("shows per-metric source/status/reason and preserves no-value rules", () => {
    render(<ProcessMetricMatrix panel={processMetrics} />);

    const panel = screen.getByLabelText("trusted Process Metrics route");
    expect(panel.textContent).toContain("SUPPORTED");
    expect(panel.textContent).toContain("UNSUPPORTED");
    expect(panel.textContent).toContain("No numeric value authorized");
    expect(panel.textContent).toContain("not-accepted");
    expect(panel.textContent).not.toContain("Full OEE0");
  });
});
