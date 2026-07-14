import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { PageSummaryStrip } from "../PageSummaryStrip";

afterEach(cleanup);

describe("PageSummaryStrip", () => {
  it("labels totals as current-page accepted facts and result mix as station_result only", () => {
    render(
      <PageSummaryStrip
        summary={{
          label: "Current page only",
          totalAcceptedFacts: 4,
          byResult: { ok: 1, nok: 1 },
          byStation: { WS01: 2, WS02: 1, "": 1 }
        }}
      />
    );

    const summary = screen.getByLabelText("Accepted events page summary");
    expect(summary.textContent).toContain("Current page only");
    expect(summary.textContent).toContain("4accepted facts");
    expect(summary.textContent).toContain("Production result mix (station_result only)");
    expect(summary.textContent).toContain("ok: 1 / nok: 1");
    expect(summary.textContent).toContain("Empty string: 1");
    expect(summary.textContent).not.toMatch(/line-wide|global|total production|unknown/i);
  });
});
