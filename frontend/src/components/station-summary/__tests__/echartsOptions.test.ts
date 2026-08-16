import { describe, expect, it } from "vitest";
import {
  buildStationSummaryOption,
  hasStationSummaryChartData,
  stationColorFor,
  type StationSummaryChartProps,
} from "../echartsOptions";

function optionFor(props: StationSummaryChartProps): Record<string, any> {
  return buildStationSummaryOption(props) as Record<string, any>;
}

const routeSeries = [
  { id: "WS01", label: "WS01", points: [{ label: "2026-08-16T10:00:00Z", value: 30 }] },
  { id: "WS02", label: "WS02", points: [{ label: "2026-08-16T10:00:00Z", value: 29 }] },
  { id: "WS03", label: "WS03", points: [{ label: "2026-08-16T10:00:00Z", value: 28 }] },
] as const;

describe("Station Summary ECharts option builders", () => {
  it("builds a time-axis CT option with one colored line per route station", () => {
    const option = optionFor({
      ariaLabel: "Cycle Time Trend",
      series: routeSeries,
      xAxisLabel: "Time",
      yAxisLabel: "Cycle time",
      unit: "s",
      emptyMessage: "empty",
      variant: "line",
    });

    expect(option.xAxis.type).toBe("time");
    expect(option.yAxis.name).toBe("Cycle time (s)");
    expect(option.tooltip.trigger).toBe("axis");
    expect(option.tooltip.axisPointer.type).toBe("cross");
    expect(option.tooltip.valueFormatter(30.125)).toBe("30.125 s");
    expect(option.legend.data).toEqual(["WS01", "WS02", "WS03"]);
    expect(option.series).toHaveLength(3);
    expect(option.series.every((item: Record<string, any>) => item.type === "line")).toBe(true);
    expect(option.series.map((item: Record<string, any>) => item.itemStyle.color)).toEqual([
      "#73BF69",
      "#F2CC0C",
      "#5794F2",
    ]);
    expect(option.series[0].data).toEqual([["2026-08-16T10:00:00Z", 30]]);
    expect(option.xAxis.axisLabel.formatter(Date.parse("2026-08-16T10:00:00Z"))).toMatch(/^\d{2}:\d{2}$/);
  });

  it("builds production as the same multi-series time option with units per bucket", () => {
    const option = optionFor({
      ariaLabel: "Production Trend",
      series: routeSeries.map((series, index) => ({
        ...series,
        points: [{ label: "2026-08-16T10:00:00Z", value: index + 1 }],
      })),
      xAxisLabel: "Time",
      yAxisLabel: "Units / bucket",
      unit: "units",
      emptyMessage: "empty",
      variant: "line",
    });

    expect(option.xAxis.type).toBe("time");
    expect(option.yAxis.name).toBe("Units / bucket (units)");
    expect(option.series.map((item: Record<string, any>) => item.data[0][1])).toEqual([1, 2, 3]);
  });

  it("builds OK/NOK as a route-ordered stacked bar", () => {
    const option = optionFor({
      ariaLabel: "OK/NOK by Station",
      series: [
        { id: "OK", label: "OK", color: "#73BF69", points: [{ label: "WS01", value: 2 }, { label: "WS02", value: 3 }] },
        { id: "NOK", label: "NOK", color: "#F2CC0C", points: [{ label: "WS01", value: 1 }, { label: "WS02", value: 0 }] },
      ],
      xAxisLabel: "Station",
      yAxisLabel: "Units",
      unit: "units",
      emptyMessage: "empty",
      variant: "stacked-bar",
    });

    expect(option.xAxis.type).toBe("category");
    expect(option.xAxis.data).toEqual(["WS01", "WS02"]);
    expect(option.series.map((item: Record<string, any>) => [item.name, item.type, item.stack])).toEqual([
      ["OK", "bar", "result"],
      ["NOK", "bar", "result"],
    ]);
  });

  it("maps NOK code categories and counts without changing API values", () => {
    const option = optionFor({
      ariaLabel: "NOK Code Distribution",
      points: [{ label: "10001", value: 4 }, { label: "10002", value: 1 }],
      xAxisLabel: "NOK Code",
      yAxisLabel: "NOK units",
      unit: "units",
      emptyMessage: "empty",
    });

    expect(option.xAxis.data).toEqual(["10001", "10002"]);
    expect(option.series).toHaveLength(1);
    expect(option.series[0].type).toBe("bar");
    expect(option.series[0].data).toEqual([4, 1]);
  });

  it("keeps chart colors deterministic and treats absent points as empty data", () => {
    expect(stationColorFor("WS01", 8)).toBe("#73BF69");
    expect(stationColorFor("WS10", 0)).toBe("#73BF69");
    expect(stationColorFor("WS10", 1)).toBe("#F2CC0C");
    expect(hasStationSummaryChartData({
      ariaLabel: "empty",
      points: [],
      xAxisLabel: "x",
      yAxisLabel: "y",
      unit: "u",
      emptyMessage: "empty",
    })).toBe(false);
  });
});
