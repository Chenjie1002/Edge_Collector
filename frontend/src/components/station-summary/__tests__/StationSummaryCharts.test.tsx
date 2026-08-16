import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { LineProductSummary } from "../LineProductSummary";
import { StationSummaryChart } from "../StationSummaryChart";
import type { LineSummary } from "../../../lib/stationSummary/lineSummarySchema";

afterEach(() => cleanup());

const summary: LineSummary = {
  contractVersion: "production-line-summary/v1",
  scope: {
    lineId: "LINE_001",
    startTime: "2026-08-16T10:00:00Z",
    endTime: "2026-08-16T11:00:00Z",
    cohortBasis: "terminal_completed",
  },
  topology: { entryStationId: "WS01", terminalStationId: "WS03", stations: ["WS01", "WS02", "WS03"] },
  cohort: { unitCount: 3, reconciliationStatus: "PASS", errors: [] },
  stations: [
    {
      stationId: "WS01",
      total: 3,
      ok: 2,
      nok: 1,
      newNok: 1,
      skipped: 0,
      processed: 3,
      reconciliationStatus: "PASS",
      evidenceCount: 3,
      missingUnitCount: 0,
      duplicateUnitCount: 0,
      invalidRecordCount: 0,
      resultCompatibility: "native_nok_process_status_split",
    },
    {
      stationId: "WS02",
      total: 3,
      ok: 2,
      nok: 1,
      newNok: 0,
      skipped: 1,
      processed: 2,
      reconciliationStatus: "PASS",
      evidenceCount: 3,
      missingUnitCount: 0,
      duplicateUnitCount: 0,
      invalidRecordCount: 0,
      resultCompatibility: "native_nok_process_status_split",
    },
    {
      stationId: "WS03",
      total: 3,
      ok: 2,
      nok: 1,
      newNok: 0,
      skipped: 1,
      processed: 2,
      reconciliationStatus: "PASS",
      evidenceCount: 3,
      missingUnitCount: 0,
      duplicateUnitCount: 0,
      invalidRecordCount: 0,
      resultCompatibility: "native_nok_process_status_split",
    },
  ],
  line: {
    lineId: "LINE_001",
    name: "Demo Line",
    stationCount: 3,
    route: ["WS01", "WS02", "WS03"],
    entryStationId: "WS01",
    terminalStationId: "WS03",
    activeProfile: "normal",
    collectorState: "RUNNING",
    collectorConnectedStations: 3,
    runtimeStatus: "RUNNING",
    runtimeAuthority: "collector_runtime_status",
    mappingContentSha256: null,
    configVersion: null,
  },
  overview: {
    completedUnits: 3,
    finalOk: 2,
    finalNok: 1,
    finalYield: 2 / 3,
    ackPendingEvents: 0,
    averageCycleSeconds: 30,
    routeConservation: "PASS",
  },
  trends: {
    production: [{ bucketStart: "2026-08-16T10:00:00Z", completed: 3, ok: 2, nok: 1 }],
    productionByStation: [
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS01", completed: 3, ok: 2, nok: 1 },
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS02", completed: 3, ok: 2, nok: 1 },
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS03", completed: 3, ok: 2, nok: 1 },
    ],
    cycleTime: [
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS01", averageCycleSeconds: 30.125, samples: 3 },
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS02", averageCycleSeconds: 29.5, samples: 3 },
      { bucketStart: "2026-08-16T10:00:00Z", stationId: "WS03", averageCycleSeconds: 28.75, samples: 3 },
    ],
  },
  quality: {
    nokAccumulation: [
      { stationId: "WS01", count: 1 },
      { stationId: "WS02", count: 1 },
      { stationId: "WS03", count: 1 },
    ],
    newNokByStation: [
      { stationId: "WS01", count: 1 },
      { stationId: "WS02", count: 0 },
      { stationId: "WS03", count: 0 },
    ],
    nokCodeDistribution: [{ code: 10001, count: 1 }],
  },
  collectorRuntime: [],
  recentCompletedUnits: [],
};

describe("Station Summary charts", () => {
  it("renders one multi-series chart for CT and one for station production", () => {
    render(<LineProductSummary summary={summary} />);

    const cycleFigure = screen.getByRole("figure", { name: "Cycle Time Trend" });
    const productionFigure = screen.getByRole("figure", { name: "Production Trend" });
    expect(cycleFigure).toBeTruthy();
    expect(productionFigure).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Cycle Time Trend" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Production Trend" })).toBeTruthy();
    expect(within(cycleFigure).getByText("WS01")).toBeTruthy();
    expect(within(cycleFigure).getByText("WS02")).toBeTruthy();
    expect(within(cycleFigure).getByText("WS03")).toBeTruthy();
    expect(within(productionFigure).getByText("WS01")).toBeTruthy();
    expect(within(productionFigure).getByText("WS02")).toBeTruthy();
    expect(within(productionFigure).getByText("WS03")).toBeTruthy();
    expect(within(cycleFigure).getByText("y = Cycle time")).toBeTruthy();
    expect(within(productionFigure).getByText("y = Units / bucket")).toBeTruthy();
    expect(within(cycleFigure).getAllByText("unit = s").length).toBe(1);
    expect(within(productionFigure).getAllByText("unit = units").length).toBe(1);

    const point = within(productionFigure).getByRole("button", { name: "WS01 · 2026-08-16T10:00:00Z · 3 units" });
    fireEvent.focus(point);
    expect(within(productionFigure).getByRole("tooltip").textContent).toContain("WS01");
    expect(within(productionFigure).getByRole("tooltip").textContent).toContain("3 units");

    const stackedFigure = screen.getByRole("figure", { name: "OK/NOK by Station" });
    const bar = within(stackedFigure).getByRole("button", { name: "WS01 · OK · 2 units" });
    fireEvent.focus(bar);
    expect(within(stackedFigure).getByRole("tooltip").textContent).toContain("OK");
    expect(within(stackedFigure).getByRole("tooltip").textContent).toContain("2 units");
    expect(document.querySelectorAll(".mes-chart-reading")).toHaveLength(0);
  });

  it("renders explicit empty state without generating chart points", () => {
    render(
      <LineProductSummary
        summary={{
          ...summary,
          trends: { production: [], productionByStation: [], cycleTime: [] },
          quality: { nokAccumulation: [], newNokByStation: [], nokCodeDistribution: [] },
        }}
      />,
    );

    expect(screen.getByText("No trusted completed units in this window.")).toBeTruthy();
    expect(screen.queryByRole("figure", { name: "Cycle Time Trend" })).toBeNull();
    expect(screen.queryByRole("figure", { name: "Production Trend" })).toBeNull();
    expect(screen.getByRole("figure", { name: "OK/NOK by Station" })).toBeTruthy();
  });

  it("keeps decimal API values exact in focus readings", () => {
    render(
      <StationSummaryChart
        ariaLabel="Observed cycle time"
        points={[{ label: "2026-08-16T10:00:00Z", value: 30.125 }]}
        xAxisLabel="Time"
        yAxisLabel="Cycle time"
        unit="s"
        emptyMessage="No processed CT samples in this window."
        variant="line"
      />,
    );

    const point = screen.getByRole("button", { name: "2026-08-16T10:00:00Z · 30.125 s" });
    fireEvent.focus(point);
    expect(screen.getByRole("tooltip").textContent).toContain("2026-08-16T10:00:00Z · 30.125 s");
  });

  it("shows an anchored pointer-near tooltip with exact value and unit, then hides it on leave", () => {
    render(
      <StationSummaryChart
        ariaLabel="Observed cycle time"
        points={[{ label: "2026-08-16T10:00:00Z", value: 30.125 }]}
        xAxisLabel="Time"
        yAxisLabel="Cycle time"
        unit="s"
        emptyMessage="No processed CT samples in this window."
        variant="line"
      />,
    );

    const point = screen.getByRole("button", { name: "2026-08-16T10:00:00Z · 30.125 s" });
    fireEvent.mouseEnter(point);

    const tooltip = screen.getByRole("tooltip");
    expect(tooltip.classList.contains("mes-chart-tooltip")).toBe(true);
    expect(tooltip.textContent).toContain("2026-08-16T10:00:00Z");
    expect(tooltip.textContent).toContain("30.125 s");
    expect(tooltip.getAttribute("data-anchor-x")).toBe("382");
    expect(tooltip.getAttribute("data-anchor-y")).toBeTruthy();
    expect(tooltip.style.left).not.toBe("");

    fireEvent.mouseLeave(point);
    expect(screen.queryByRole("tooltip")).toBeNull();
  });

  it("anchors the exact tooltip to the keyboard-focused bar", () => {
    render(
      <StationSummaryChart
        ariaLabel="Inherited NOK"
        points={[{ label: "WS01", value: 2 }]}
        xAxisLabel="Station"
        yAxisLabel="Unit count"
        unit="units"
        emptyMessage="No inherited NOK data in this window."
      />,
    );

    const bar = screen.getByRole("button", { name: "WS01 · 2 units" });
    fireEvent.focus(bar);

    expect(screen.getByRole("tooltip").textContent).toContain("WS01");
    expect(screen.getByRole("tooltip").textContent).toContain("2 units");
    fireEvent.blur(bar);
    expect(screen.queryByRole("tooltip")).toBeNull();
  });
});
