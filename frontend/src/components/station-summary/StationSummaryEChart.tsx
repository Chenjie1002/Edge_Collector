"use client";

import { useEffect, useMemo, useRef } from "react";
import * as echarts from "echarts/core";
import { BarChart, LineChart } from "echarts/charts";
import { GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import {
  buildStationSummaryOption,
  hasStationSummaryChartData,
  type StationSummaryChartProps,
} from "./echartsOptions";

echarts.use([BarChart, LineChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer]);

export function StationSummaryEChart(props: StationSummaryChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<ReturnType<typeof echarts.init> | null>(null);
  const hasData = useMemo(() => hasStationSummaryChartData(props), [props.points, props.series]);
  const option = useMemo(() => buildStationSummaryOption(props), [
    props.points,
    props.series,
    props.xAxisLabel,
    props.yAxisLabel,
    props.unit,
    props.variant,
  ]);

  useEffect(() => {
    const container = containerRef.current;
    if (!hasData || !container) return undefined;

    const chart = echarts.init(container, undefined, { renderer: "canvas" });
    chartRef.current = chart;
    const resizeObserver = typeof ResizeObserver === "function"
      ? new ResizeObserver(() => chart.resize())
      : undefined;
    resizeObserver?.observe(container);
    const onWindowResize = () => chart.resize();
    window.addEventListener("resize", onWindowResize);

    return () => {
      resizeObserver?.disconnect();
      window.removeEventListener("resize", onWindowResize);
      chart.dispose();
      chartRef.current = null;
    };
  }, [hasData]);

  useEffect(() => {
    if (chartRef.current && hasData) {
      chartRef.current.setOption(option, { notMerge: false, lazyUpdate: true });
    }
  }, [hasData, option]);

  if (!hasData) return <p className="mes-empty">{props.emptyMessage}</p>;

  return (
    <figure className="mes-echart-figure" aria-label={props.ariaLabel}>
      <div className="mes-chart-axis-summary" aria-label={`${props.ariaLabel} axes`}>
        <span>x = {props.xAxisLabel}</span>
        <span>y = {props.yAxisLabel}</span>
        <span>unit = {props.unit}</span>
      </div>
      <div className="mes-echart-plot">
        <div
          ref={containerRef}
          className="mes-echart"
          data-chart-engine="echarts"
          role="img"
          aria-label={props.ariaLabel}
        />
      </div>
    </figure>
  );
}
