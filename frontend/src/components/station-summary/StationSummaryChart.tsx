"use client";

import { StationSummaryEChart } from "./StationSummaryEChart";
import type { StationSummaryChartProps } from "./echartsOptions";

export {
  STATION_COLORS,
  stationColorFor,
  type StationSummaryChartPoint,
  type StationSummaryChartSeries,
} from "./echartsOptions";

export function StationSummaryChart(props: StationSummaryChartProps) {
  return <StationSummaryEChart {...props} />;
}
