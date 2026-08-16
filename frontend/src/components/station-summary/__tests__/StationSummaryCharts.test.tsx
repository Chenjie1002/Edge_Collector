import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { LineProductSummary } from "../LineProductSummary";
import { StationDetailSummary } from "../StationDetailSummary";
import { StationSummaryChart } from "../StationSummaryChart";
import type { LineSummary } from "../../../lib/stationSummary/lineSummarySchema";

const echartsMock = vi.hoisted(() => {
  const charts: Array<{
    setOption: ReturnType<typeof vi.fn>;
    resize: ReturnType<typeof vi.fn>;
    dispose: ReturnType<typeof vi.fn>;
  }> = [];
  const init = vi.fn(() => {
    const chart = {
      setOption: vi.fn(),
      resize: vi.fn(),
      dispose: vi.fn(),
    };
    charts.push(chart);
    return chart;
  });
  return { charts, init, use: vi.fn() };
});

vi.mock("echarts/core", () => ({ init: echartsMock.init, use: echartsMock.use }));
vi.mock("echarts/charts", () => ({ BarChart: {}, LineChart: {} }));
vi.mock("echarts/components", () => ({ GridComponent: {}, LegendComponent: {}, TooltipComponent: {} }));
vi.mock("echarts/renderers", () => ({ CanvasRenderer: {} }));

let resizeCallback: (() => void) | undefined;
class TestResizeObserver {
  constructor(callback: () => void) {
    resizeCallback = callback;
  }

  observe = vi.fn();
  disconnect = vi.fn();
}

beforeEach(() => {
  echartsMock.charts.length = 0;
  echartsMock.init.mockClear();
  echartsMock.use.mockClear();
  resizeCallback = undefined;
  vi.stubGlobal("ResizeObserver", TestResizeObserver);
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

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
  it("renders ECharts multi-series and stacked-bar options for the line dashboard", () => {
    render(<LineProductSummary summary={summary} />);

    const cycleFigure = screen.getByRole("figure", { name: "Cycle Time Trend" });
    const productionFigure = screen.getByRole("figure", { name: "Production Trend" });
    const stackedFigure = screen.getByRole("figure", { name: "OK/NOK by Station" });
    const nokFigure = screen.getByRole("figure", { name: "NOK Code Distribution" });
    expect(cycleFigure).toBeTruthy();
    expect(productionFigure).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Cycle Time Trend" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Production Trend" })).toBeTruthy();
    expect(within(cycleFigure).getByText("y = Cycle time")).toBeTruthy();
    expect(within(productionFigure).getByText("y = Units / bucket")).toBeTruthy();
    expect(within(cycleFigure).getAllByText("unit = s").length).toBe(1);
    expect(within(productionFigure).getAllByText("unit = units").length).toBe(1);
    expect(cycleFigure.querySelector("svg")).toBeNull();
    expect(productionFigure.querySelector('[data-chart-engine="echarts"]')).toBeTruthy();
    expect(stackedFigure.querySelector('[data-chart-engine="echarts"]')).toBeTruthy();
    expect(nokFigure.querySelector('[data-chart-engine="echarts"]')).toBeTruthy();

    expect(echartsMock.init).toHaveBeenCalledTimes(4);
    const cycleOption = echartsMock.charts[0].setOption.mock.calls[0][0] as Record<string, any>;
    const productionOption = echartsMock.charts[1].setOption.mock.calls[0][0] as Record<string, any>;
    const stackedOption = echartsMock.charts[2].setOption.mock.calls[0][0] as Record<string, any>;
    const nokOption = echartsMock.charts[3].setOption.mock.calls[0][0] as Record<string, any>;
    expect(cycleOption.xAxis.type).toBe("time");
    expect(cycleOption.yAxis.name).toBe("Cycle time (s)");
    expect(cycleOption.tooltip.trigger).toBe("axis");
    expect(cycleOption.legend.data).toEqual(["WS01", "WS02", "WS03"]);
    expect(cycleOption.series).toHaveLength(3);
    expect(cycleOption.series.map((item: Record<string, any>) => item.type)).toEqual(["line", "line", "line"]);
    expect(cycleOption.series.map((item: Record<string, any>) => item.itemStyle.color)).toEqual(["#73BF69", "#F2CC0C", "#5794F2"]);
    expect(productionOption.xAxis.type).toBe("time");
    expect(productionOption.yAxis.name).toBe("Units / bucket (units)");
    expect(productionOption.series).toHaveLength(3);
    expect(stackedOption.xAxis.data).toEqual(["WS01", "WS02", "WS03"]);
    expect(stackedOption.series.map((item: Record<string, any>) => item.name)).toEqual(["OK", "NOK"]);
    expect(stackedOption.series.every((item: Record<string, any>) => item.type === "bar" && item.stack === "result")).toBe(true);
    expect(stackedOption.series.map((item: Record<string, any>) => item.itemStyle.color)).toEqual(["#73BF69", "#F2CC0C"]);
    expect(nokOption.xAxis.data).toEqual(["10001"]);
    expect(nokOption.series[0].type).toBe("bar");
    expect(nokOption.series[0].data).toEqual([1]);
  });

  it("renders explicit empty state without creating empty charts", () => {
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
    expect(echartsMock.init).toHaveBeenCalledTimes(1);
  });

  it("reuses one ECharts instance for data updates and disposes it on unmount", () => {
    const { rerender, unmount } = render(
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

    expect(echartsMock.init).toHaveBeenCalledTimes(1);
    expect(echartsMock.charts[0].setOption).toHaveBeenCalledTimes(1);
    rerender(
      <StationSummaryChart
        ariaLabel="Observed cycle time"
        points={[{ label: "2026-08-16T10:00:00Z", value: 31.25 }]}
        xAxisLabel="Time"
        yAxisLabel="Cycle time"
        unit="s"
        emptyMessage="No processed CT samples in this window."
        variant="line"
      />,
    );

    expect(echartsMock.init).toHaveBeenCalledTimes(1);
    expect(echartsMock.charts[0].setOption).toHaveBeenCalledTimes(2);
    resizeCallback?.();
    expect(echartsMock.charts[0].resize).toHaveBeenCalledTimes(1);
    unmount();
    expect(echartsMock.charts[0].dispose).toHaveBeenCalledTimes(1);
  });

  it("migrates Station Detail charts through the same ECharts wrapper", () => {
    const station = summary.stations[0];
    render(
      <StationDetailSummary
        summary={{
          ...summary,
          stations: [{
            ...station,
            activityTrend: [{ bucketStart: "2026-08-16T10:00:00Z", processed: 2, skipped: 1, newNok: 1 }],
            nokCodes: [{ code: 10001, count: 1 }],
          }, ...summary.stations.slice(1)],
        }}
        stationId="WS01"
      />,
    );

    expect(screen.getByRole("figure", { name: "WS01 processed event trend" })).toBeTruthy();
    expect(screen.getByRole("figure", { name: "WS01 observed cycle time trend" })).toBeTruthy();
    expect(screen.getByRole("figure", { name: "WS01 NOK code distribution" })).toBeTruthy();
    expect(screen.getByRole("figure", { name: "WS01 processed event trend" }).querySelector("svg")).toBeNull();
    expect(echartsMock.init).toHaveBeenCalledTimes(4);
  });

  it("keeps decimal API values in the ECharts data option", () => {
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

    const option = echartsMock.charts[0].setOption.mock.calls[0][0] as Record<string, any>;
    expect(option.series[0].data).toEqual([["2026-08-16T10:00:00Z", 30.125]]);
  });
});
