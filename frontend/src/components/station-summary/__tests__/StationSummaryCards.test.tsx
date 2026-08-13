import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { QualitySummaryViewModel } from "../../../lib/stationSummary/viewModel";
import { StationSummaryCards } from "../StationSummaryCards";

const quality: QualitySummaryViewModel = {
  sourceLabel: "trusted Quality route",
  status: "UNAVAILABLE",
  dataSufficiency: "UNAVAILABLE",
  scopeLabel: "LINE_001 / WS01",
  windowLabel: "2026-07-05T00:00:00Z → 2026-07-05T08:00:00Z [from,to)",
  counts: null,
  qualityRate: null,
  qualityRateText: "No numeric rate authorized",
  nokDistribution: [],
  message: "Quality denominator is unavailable."
};

describe("StationSummaryCards", () => {
  it("keeps the trusted source/status visible and does not display an unavailable rate as zero", () => {
    render(<StationSummaryCards quality={quality} />);

    const panel = screen.getByLabelText("Trusted Quality route summary");
    expect(panel.textContent).toContain("trusted Quality route");
    expect(panel.textContent).toContain("UNAVAILABLE");
    expect(panel.textContent).toContain("No numeric rate authorized");
    expect(panel.textContent).not.toContain("0%");
    expect(panel.textContent).not.toContain("Quality rate0");
  });
});
