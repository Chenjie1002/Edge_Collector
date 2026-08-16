import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { StationSummaryPageView } from "../../../app/station-summary/page";
import { fetchLineSummary } from "../../../lib/stationSummary/lineSummaryApi";
import type { LineSummary } from "../../../lib/stationSummary/lineSummarySchema";
import type { TrustedAcceptedEventsApiOrigin } from "../../../lib/acceptedStationEvents/apiOrigin";

const echartsMock = vi.hoisted(() => ({
  init: vi.fn(() => ({ setOption: vi.fn(), resize: vi.fn(), dispose: vi.fn() })),
  use: vi.fn(),
}));

vi.mock("echarts/core", () => ({ init: echartsMock.init, use: echartsMock.use }));
vi.mock("echarts/charts", () => ({ BarChart: {}, LineChart: {} }));
vi.mock("echarts/components", () => ({ GridComponent: {}, LegendComponent: {}, TooltipComponent: {} }));
vi.mock("echarts/renderers", () => ({ CanvasRenderer: {} }));

vi.mock("../../../lib/stationSummary/lineSummaryApi", () => ({
  fetchLineSummary: vi.fn(),
}));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  vi.useRealTimers();
});

const catalog = {
  contractVersion: "production-scope-options/v1",
  timezone: "Asia/Shanghai",
  utcOffset: "+08:00",
  lines: [
    {
      lineId: "LINE_001",
      name: "Demo Assembly Line Runtime",
      stations: [{ stationId: "WS01", name: "Screw Station", stationOrder: 1 }],
    },
    {
      lineId: "LINE_002",
      name: "Second Line",
      stations: [{ stationId: "WS10", name: "Pack Station", stationOrder: 1 }],
    },
  ],
} as const;

const trustedApiOrigin = "https://api.example.test" as TrustedAcceptedEventsApiOrigin;

function summary(completedUnits: number): LineSummary {
  return {
    contractVersion: "production-line-summary/v1",
    scope: {
      lineId: "LINE_001",
      startTime: "2026-08-16T08:00:00Z",
      endTime: "2026-08-16T16:00:00Z",
      cohortBasis: "terminal_completed",
    },
    topology: { entryStationId: "WS01", terminalStationId: "WS01", stations: ["WS01"] },
    cohort: { unitCount: completedUnits, reconciliationStatus: "PASS", errors: [] },
    stations: [{
      stationId: "WS01",
      total: completedUnits,
      ok: completedUnits,
      nok: 0,
      newNok: 0,
      skipped: 0,
      processed: completedUnits,
      reconciliationStatus: "PASS",
      evidenceCount: completedUnits,
      missingUnitCount: 0,
      duplicateUnitCount: 0,
      invalidRecordCount: 0,
      resultCompatibility: "native_nok_process_status_split",
    }],
    line: {
      lineId: "LINE_001",
      name: "Demo Line",
      stationCount: 1,
      route: ["WS01"],
      entryStationId: "WS01",
      terminalStationId: "WS01",
      activeProfile: "normal",
      collectorState: "RUNNING",
      collectorConnectedStations: 1,
      runtimeStatus: "RUNNING",
      runtimeAuthority: "collector_runtime_status",
      mappingContentSha256: null,
      configVersion: null,
    },
    overview: {
      completedUnits,
      finalOk: completedUnits,
      finalNok: 0,
      finalYield: 1,
      ackPendingEvents: 0,
      averageCycleSeconds: 30,
      routeConservation: "PASS",
    },
    trends: {
      production: [{ bucketStart: "2026-08-16T10:00:00Z", completed: completedUnits, ok: completedUnits, nok: 0 }],
      cycleTime: [],
    },
    quality: {
      nokAccumulation: [{ stationId: "WS01", count: 0 }],
      newNokByStation: [{ stationId: "WS01", count: 0 }],
      nokCodeDistribution: [],
    },
    collectorRuntime: [],
    recentCompletedUnits: [],
  };
}

function renderLivePage() {
  return render(
    <StationSummaryPageView
      catalog={catalog}
      trustedApiOrigin={trustedApiOrigin}
      state={{
        kind: "ready",
        view: "line",
        query: {
          lineId: "LINE_001",
          mode: "LIVE",
          startTime: "2026-08-16T08:00:00+08:00",
          endTime: "2026-08-16T16:00:00+08:00",
        },
        summary: summary(3),
      }}
    />,
  );
}

describe("Station Summary LIVE data region", () => {
  it("refreshes data in place while preserving shell, scope controls and selected tab", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-08-16T08:10:00Z"));
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: summary(7) });

    renderLivePage();
    const form = screen.getByRole("form", { name: "Station summary scope query" });
    const tabs = screen.getByRole("navigation", { name: "Production summary views" });
    fireEvent.change(screen.getByLabelText("Line"), { target: { value: "LINE_002" } });

    await act(async () => {
      vi.advanceTimersByTime(10_000);
      await Promise.resolve();
    });

    expect(screen.getByText("LIVE data current")).toBeTruthy();
    expect(fetchLineSummary).toHaveBeenCalledWith(
      expect.objectContaining({
        lineId: "LINE_001",
        mode: "LIVE",
        startTime: "2026-08-16T08:10:00+08:00",
        endTime: "2026-08-16T16:10:00+08:00",
      }),
      trustedApiOrigin,
    );
    expect(screen.getByText("Completed units").nextElementSibling?.textContent).toBe("7");
    expect(screen.getByRole("form", { name: "Station summary scope query" })).toBe(form);
    expect(screen.getByRole("navigation", { name: "Production summary views" })).toBe(tabs);
    expect((screen.getByLabelText("Line") as HTMLSelectElement).value).toBe("LINE_002");
    expect(screen.getByRole("link", { name: "Line Summary" }).getAttribute("aria-current")).toBe("page");
  });

  it("keeps the last trusted data frame and marks it stale when polling fails", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-08-16T08:10:00Z"));
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: false, kind: "error", message: "Line summary request failed." });

    renderLivePage();
    await act(async () => {
      vi.advanceTimersByTime(10_000);
      await Promise.resolve();
    });

    expect(screen.getByRole("alert").textContent).toMatch(/LIVE data stale/i);
    expect(screen.getByText("Completed units").nextElementSibling?.textContent).toBe("3");
    expect(screen.getByRole("alert").textContent).toContain("Line summary request failed.");
  });

  it("keeps the last trusted data frame when polling topology drifts from the catalog", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-08-16T08:10:00Z"));
    const drifted = summary(9);
    vi.mocked(fetchLineSummary).mockResolvedValue({
      ok: true,
      summary: { ...drifted, topology: { ...drifted.topology, stations: ["WS02"] } },
    });

    renderLivePage();
    await act(async () => {
      vi.advanceTimersByTime(10_000);
      await Promise.resolve();
    });

    expect(screen.getByRole("alert").textContent).toContain("topology does not match the trusted scope");
    expect(screen.getByText("Completed units").nextElementSibling?.textContent).toBe("3");
  });
});
