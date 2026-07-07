import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PageSummaryStrip } from "../PageSummaryStrip";

describe("PageSummaryStrip", () => {
  it("labels aggregates as current page only", () => {
    render(
      <PageSummaryStrip
        summary={{
          label: "Current page only",
          totalAcceptedFacts: 3,
          byResult: { ok: 2, nok: 1 },
          byStation: { WS01: 2, WS02: 1 }
        }}
      />
    );

    expect(screen.getByText("Current page only")).toBeTruthy();
    expect(screen.queryByText(/line-wide|global|total production/i)).toBeNull();
  });
});
