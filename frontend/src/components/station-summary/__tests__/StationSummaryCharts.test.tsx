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
    cycleTime: [],
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
  it("shows axes, unit and exact focused value for API-backed production points", () => {
    render(<LineProductSummary summary={summary} />);

    expect(screen.getByText("x = Time")).toBeTruthy();
    expect(screen.getByText("y = Completed units / bucket")).toBeTruthy();
    expect(screen.getAllByText("unit = units").length).toBeGreaterThan(0);

    const point = screen.getByRole("button", { name: "2026-08-16T10:00:00Z · 3 units" });
    fireEvent.focus(point);
    expect(screen.getAllByRole("status").some((reading) => reading.textContent === "2026-08-16T10:00:00Z · 3 units")).toBe(true);

    const bar = within(screen.getByRole("figure", { name: "Inherited NOK across route" })).getByRole("button", { name: "WS01 · 1 units" });
    fireEvent.focus(bar);
    expect(screen.getAllByRole("status").some((reading) => reading.textContent === "WS01 · 1 units")).toBe(true);
  });

  it("renders explicit empty state without generating chart points", () => {
    render(
      <LineProductSummary
        summary={{
          ...summary,
          trends: { production: [], cycleTime: [] },
          quality: { nokAccumulation: [], newNokByStation: [], nokCodeDistribution: [] },
        }}
      />,
    );

    expect(screen.getByText("No trusted completed units in this window.")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /units$/ })).toBeNull();
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
    expect(screen.getByRole("status").textContent).toContain("2026-08-16T10:00:00Z · 30.125 s");
  });
});
