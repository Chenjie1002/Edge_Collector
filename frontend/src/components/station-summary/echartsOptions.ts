import type { EChartsOption } from "echarts";

export type StationSummaryChartPoint = Readonly<{
  label: string;
  value: number;
}>;

export type StationSummaryChartSeries = Readonly<{
  id: string;
  label: string;
  color?: string;
  points: readonly StationSummaryChartPoint[];
}>;

export type StationSummaryChartVariant = "bar" | "line" | "stacked-bar";

export type StationSummaryChartProps = Readonly<{
  ariaLabel: string;
  points?: readonly StationSummaryChartPoint[];
  series?: readonly StationSummaryChartSeries[];
  xAxisLabel: string;
  yAxisLabel: string;
  unit: string;
  emptyMessage: string;
  variant?: StationSummaryChartVariant;
}>;

export const STATION_COLORS = [
  "#73BF69",
  "#F2CC0C",
  "#5794F2",
  "#FF9830",
  "#F2495C",
  "#B877D9",
  "#8AB8FF",
  "#56A64B",
] as const;

const STATION_COLOR_BY_ID: Readonly<Record<string, string>> = {
  WS01: STATION_COLORS[0],
  WS02: STATION_COLORS[1],
  WS03: STATION_COLORS[2],
  WS04: STATION_COLORS[3],
  WS05: STATION_COLORS[4],
  WS06: STATION_COLORS[5],
  WS07: STATION_COLORS[6],
  WS08: STATION_COLORS[7],
};

const DEFAULT_COLOR = "#5794F2";
const RESULT_STACK = "result";

export function stationColorFor(stationId: string, routeIndex = 0): string {
  return STATION_COLOR_BY_ID[stationId] ?? STATION_COLORS[routeIndex % STATION_COLORS.length];
}

export function normalizeStationSummarySeries(
  points: readonly StationSummaryChartPoint[] | undefined,
  series: readonly StationSummaryChartSeries[] | undefined,
): readonly StationSummaryChartSeries[] {
  if (series?.length) {
    return series.map((item, index) => ({
      ...item,
      color: item.color ?? stationColorFor(item.id, index),
    }));
  }
  return [{ id: "value", label: "", color: DEFAULT_COLOR, points: points ?? [] }];
}

function uniqueLabels(series: readonly StationSummaryChartSeries[]): readonly string[] {
  const labels = new Set<string>();
  series.forEach((item) => item.points.forEach((point) => labels.add(point.label)));
  return [...labels];
}

function pointAt(series: StationSummaryChartSeries, label: string): StationSummaryChartPoint | undefined {
  return series.points.find((point) => point.label === label);
}

function axisName(label: string, unit: string): string {
  return unit ? `${label} (${unit})` : label;
}

function timeAxisLabel(value: number): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "Asia/Shanghai",
  }).format(date);
}

function legendData(series: readonly StationSummaryChartSeries[]): readonly string[] {
  return series.map((item) => item.label).filter(Boolean);
}

export function hasStationSummaryChartData(props: StationSummaryChartProps): boolean {
  return normalizeStationSummarySeries(props.points, props.series).some((item) => item.points.length > 0);
}

export function buildStationSummaryOption(props: StationSummaryChartProps): EChartsOption {
  const variant = props.variant ?? "bar";
  const chartSeries = normalizeStationSummarySeries(props.points, props.series);
  const labels = uniqueLabels(chartSeries);
  const isTimeSeries = variant === "line";
  const legends = legendData(chartSeries);

  const series = chartSeries.map((item, index) => {
    const color = item.color ?? stationColorFor(item.id, index);
    const name = item.label || props.yAxisLabel;
    const data = isTimeSeries
      ? item.points.map((point) => [point.label, point.value])
      : labels.map((label) => pointAt(item, label)?.value ?? 0);

    if (isTimeSeries) {
      return {
        name,
        type: "line" as const,
        data,
        itemStyle: { color },
        showSymbol: false,
        connectNulls: true,
        lineStyle: { color, width: 2 },
        areaStyle: { color, opacity: 0.08 },
      };
    }
    return {
      name,
      type: "bar" as const,
      data,
      itemStyle: { color },
      barMaxWidth: 42,
      ...(variant === "stacked-bar" ? { stack: RESULT_STACK } : {}),
    };
  });

  return {
    animationDuration: 250,
    animationDurationUpdate: 250,
    grid: {
      top: 24,
      right: 24,
      bottom: legends.length > 1 ? 62 : 44,
      left: 70,
    },
    legend: {
      show: legends.length > 1,
      data: [...legends],
      bottom: 4,
      type: "scroll",
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: isTimeSeries ? "cross" : "shadow" },
      valueFormatter: (value) => `${value} ${props.unit}`,
    },
    xAxis: isTimeSeries
      ? {
          type: "time",
          name: props.xAxisLabel,
          nameLocation: "middle",
          nameGap: 30,
          boundaryGap: [0, 0],
          axisLabel: { formatter: timeAxisLabel },
        }
      : {
          type: "category",
          name: props.xAxisLabel,
          nameLocation: "middle",
          nameGap: 30,
          data: [...labels],
          axisLabel: { interval: 0, hideOverlap: true },
        },
    yAxis: {
      type: "value",
      name: axisName(props.yAxisLabel, props.unit),
      nameLocation: "middle",
      nameGap: 48,
      axisLabel: { formatter: (value: number) => String(value) },
    },
    series,
  };
}
