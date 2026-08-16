"use client";

import { useId, useState } from "react";

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

export const STATION_COLORS = [
  "#73BF69",
  "#F2CC0C",
  "#5794F2",
  "#FF9830",
  "#B877D9",
] as const;

const STATION_COLOR_BY_ID: Readonly<Record<string, string>> = {
  WS01: STATION_COLORS[0],
  WS02: STATION_COLORS[1],
  WS03: STATION_COLORS[2],
  WS04: STATION_COLORS[3],
  WS05: STATION_COLORS[4],
};

export function stationColorFor(stationId: string, routeIndex = 0): string {
  return STATION_COLOR_BY_ID[stationId] ?? STATION_COLORS[routeIndex % STATION_COLORS.length];
}

const WIDTH = 720;
const HEIGHT = 280;
const MARGIN = { top: 24, right: 24, bottom: 64, left: 68 };
const DEFAULT_COLOR = "#5794F2";

type Props = Readonly<{
  ariaLabel: string;
  points?: readonly StationSummaryChartPoint[];
  series?: readonly StationSummaryChartSeries[];
  xAxisLabel: string;
  yAxisLabel: string;
  unit: string;
  emptyMessage: string;
  variant?: "bar" | "line" | "stacked-bar";
}>;

type ActivePoint = Readonly<{
  label: string;
  seriesId: string;
}>;

function displayValue(value: number): string {
  return String(value);
}

function pointLabel(point: StationSummaryChartPoint, unit: string, seriesLabel?: string): string {
  const prefix = seriesLabel ? `${seriesLabel} · ` : "";
  return `${prefix}${point.label} · ${displayValue(point.value)} ${unit}`;
}

function normalizeSeries(
  points: readonly StationSummaryChartPoint[] | undefined,
  series: readonly StationSummaryChartSeries[] | undefined,
): readonly StationSummaryChartSeries[] {
  if (series?.length) {
    return series.map((item) => ({ ...item, color: item.color ?? DEFAULT_COLOR }));
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

export function StationSummaryChart({
  ariaLabel,
  points,
  series,
  xAxisLabel,
  yAxisLabel,
  unit,
  emptyMessage,
  variant = "bar",
}: Props) {
  const [activePoint, setActivePoint] = useState<ActivePoint | null>(null);
  const tooltipId = useId();
  const chartSeries = normalizeSeries(points, series);
  const labels = uniqueLabels(chartSeries);
  if (!labels.length) return <p className="mes-empty">{emptyMessage}</p>;

  const plotWidth = WIDTH - MARGIN.left - MARGIN.right;
  const plotHeight = HEIGHT - MARGIN.top - MARGIN.bottom;
  const baseline = MARGIN.top + plotHeight;
  const maximum = variant === "stacked-bar"
    ? Math.max(1, ...labels.map((label) => chartSeries.reduce((total, item) => total + (pointAt(item, label)?.value ?? 0), 0)))
    : Math.max(1, ...chartSeries.flatMap((item) => item.points.map((point) => point.value)));
  const xFor = (index: number) => MARGIN.left + (labels.length === 1 ? plotWidth / 2 : (index / (labels.length - 1)) * plotWidth);
  const yFor = (value: number) => baseline - (value / maximum) * plotHeight;
  const activeLabel = activePoint?.label ?? null;
  const activeLabelIndex = activeLabel === null ? -1 : labels.indexOf(activeLabel);
  const activeX = activeLabelIndex < 0 ? null : xFor(activeLabelIndex);
  const activeSeriesPoint = activePoint
    ? pointAt(chartSeries.find((item) => item.id === activePoint.seriesId) ?? chartSeries[0], activePoint.label)
    : undefined;
  const activeY = activeX === null ? null : yFor(activeSeriesPoint?.value ?? 0);
  const tooltipPlacement = activeY !== null && activeY <= MARGIN.top + 48 ? "below" : "above";
  const tooltipLeft = activeX === null ? null : `${Math.min(94, Math.max(6, (activeX / WIDTH) * 100))}%`;
  const activeValues = activeLabel === null
    ? []
    : chartSeries.map((item) => ({ series: item, point: pointAt(item, activeLabel) }));
  const isLegacySingleSeries = chartSeries.length === 1 && chartSeries[0].label === "";
  const barWidth = Math.min(64, Math.max(18, plotWidth / Math.max(labels.length, 1) * 0.58));

  const activate = (seriesId: string, label: string) => setActivePoint({ seriesId, label });
  const clearActive = () => setActivePoint(null);

  return (
    <figure className="mes-svg-chart" aria-label={ariaLabel}>
      <div className="mes-chart-axis-summary" aria-label={`${ariaLabel} axes`}>
        <span>x = {xAxisLabel}</span>
        <span>y = {yAxisLabel}</span>
        <span>unit = {unit}</span>
      </div>
      <div className="mes-chart-plot">
        <svg role="img" aria-label={ariaLabel} viewBox={`0 0 ${WIDTH} ${HEIGHT}`}>
          <line className="mes-chart-axis" data-axis="y" x1={MARGIN.left} y1={MARGIN.top} x2={MARGIN.left} y2={baseline} />
          <line className="mes-chart-axis" data-axis="x" x1={MARGIN.left} y1={baseline} x2={WIDTH - MARGIN.right} y2={baseline} />
          <line className="mes-chart-gridline" x1={MARGIN.left} y1={MARGIN.top + plotHeight / 2} x2={WIDTH - MARGIN.right} y2={MARGIN.top + plotHeight / 2} />
          <text className="mes-chart-tick" x={MARGIN.left - 10} y={MARGIN.top + 4} textAnchor="end">{displayValue(maximum)}</text>
          <text className="mes-chart-tick" x={MARGIN.left - 10} y={MARGIN.top + plotHeight / 2 + 4} textAnchor="end">{displayValue(maximum / 2)}</text>
          <text className="mes-chart-tick" x={MARGIN.left - 10} y={baseline + 4} textAnchor="end">0</text>
          <text className="mes-chart-axis-title" x={WIDTH / 2} y={HEIGHT - 10} textAnchor="middle">{xAxisLabel}</text>
          <text className="mes-chart-axis-title" transform={`translate(16 ${MARGIN.top + plotHeight / 2}) rotate(-90)`} textAnchor="middle">{yAxisLabel}</text>

          {variant === "line" ? chartSeries.map((item) => {
            const linePoints = item.points
              .map((point) => `${xFor(labels.indexOf(point.label))},${yFor(point.value)}`)
              .join(" ");
            return (
              <polyline
                key={`line-${item.id}`}
                className="mes-chart-line"
                data-series={item.id}
                data-color={item.color}
                points={linePoints}
                style={{ stroke: item.color }}
              />
            );
          }) : null}

          {variant === "stacked-bar" ? labels.map((label, labelIndex) => {
            let accumulated = 0;
            return chartSeries.map((item) => {
              const point = pointAt(item, label);
              const value = point?.value ?? 0;
              const y = yFor(accumulated + value);
              const height = Math.max(0, yFor(accumulated) - y);
              accumulated += value;
              const labelText = `${label} · ${item.label} · ${displayValue(value)} ${unit}`;
              return (
                <rect
                  key={`stack-${item.id}-${label}`}
                  className="mes-chart-bar mes-chart-bar-stacked"
                  data-series={item.id}
                  data-color={item.color}
                  data-label={label}
                  style={{ fill: item.color }}
                  role="button"
                  tabIndex={0}
                  aria-label={labelText}
                  aria-describedby={activeLabel === label ? tooltipId : undefined}
                  x={xFor(labelIndex) - barWidth / 2}
                  y={y}
                  width={barWidth}
                  height={height}
                  rx={3}
                  onPointerEnter={() => activate(item.id, label)}
                  onPointerLeave={clearActive}
                  onMouseEnter={() => activate(item.id, label)}
                  onMouseLeave={clearActive}
                  onFocus={() => activate(item.id, label)}
                  onBlur={clearActive}
                >
                  <title>{labelText}</title>
                </rect>
              );
            });
          }) : null}

          {variant === "bar" ? labels.flatMap((label, labelIndex) => chartSeries.map((item, seriesIndex) => {
            const point = pointAt(item, label);
            if (!point) return null;
            const groupWidth = Math.min(64, Math.max(18, barWidth));
            const segmentWidth = groupWidth / chartSeries.length;
            const x = xFor(labelIndex) - groupWidth / 2 + seriesIndex * segmentWidth;
            const y = yFor(point.value);
            const labelText = pointLabel(point, unit, item.label || undefined);
            return (
              <rect
                key={`bar-${item.id}-${label}`}
                className="mes-chart-bar"
                data-series={item.id}
                data-color={item.color}
                style={{ fill: item.color }}
                role="button"
                tabIndex={0}
                aria-label={labelText}
                aria-describedby={activeLabel === label ? tooltipId : undefined}
                x={x}
                y={y}
                width={segmentWidth}
                height={Math.max(0, baseline - y)}
                rx={4}
                onPointerEnter={() => activate(item.id, label)}
                onPointerLeave={clearActive}
                onMouseEnter={() => activate(item.id, label)}
                onMouseLeave={clearActive}
                onFocus={() => activate(item.id, label)}
                onBlur={clearActive}
              >
                <title>{labelText}</title>
              </rect>
            );
          })) : null}

          {variant === "line" ? chartSeries.flatMap((item) => item.points.map((point) => {
            const labelIndex = labels.indexOf(point.label);
            const labelText = pointLabel(point, unit, item.label || undefined);
            return (
              <circle
                key={`point-${item.id}-${point.label}`}
                className="mes-chart-point"
                data-series={item.id}
                data-color={item.color}
                style={{ fill: item.color }}
                role="button"
                tabIndex={0}
                aria-label={labelText}
                aria-describedby={activeLabel === point.label ? tooltipId : undefined}
                cx={xFor(labelIndex)}
                cy={yFor(point.value)}
                r={6}
                onPointerEnter={() => activate(item.id, point.label)}
                onPointerLeave={clearActive}
                onMouseEnter={() => activate(item.id, point.label)}
                onMouseLeave={clearActive}
                onFocus={() => activate(item.id, point.label)}
                onBlur={clearActive}
              >
                <title>{labelText}</title>
              </circle>
            );
          })) : null}

          {labels.map((label, index) => (
            <text key={`label-${label}`} className="mes-chart-x-tick" x={xFor(index)} y={baseline + 22} textAnchor="middle">{label}</text>
          ))}
        </svg>
        {activeLabel && activeX !== null && activeY !== null && tooltipLeft !== null ? (
          <div
            id={tooltipId}
            className="mes-chart-tooltip"
            role="tooltip"
            data-anchor-x={activeX}
            data-anchor-y={activeY}
            data-placement={tooltipPlacement}
            style={{ left: tooltipLeft, top: `${(activeY / HEIGHT) * 100}%` }}
          >
            {isLegacySingleSeries ? (
              <>
                <span>{activeLabel}{" · "}</span>
                <strong>{displayValue(activeValues[0]?.point?.value ?? 0)} {unit}</strong>
              </>
            ) : (
              <>
                <span>{activeLabel}</span>
                <ul className="mes-chart-tooltip-series">
                  {activeValues.map(({ series: item, point }) => (
                    <li key={item.id}>
                      <span><i style={{ backgroundColor: item.color }} />{item.label}</span>
                      <strong>· {point ? `${displayValue(point.value)} ${unit}` : "—"}</strong>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        ) : null}
      </div>
      {chartSeries.length > 1 ? (
        <div className="mes-chart-legend" role="list" aria-label={`${ariaLabel} legend`}>
          {chartSeries.map((item) => (
            <span key={item.id} role="listitem" data-series={item.id} data-color={item.color}>
              <i style={{ backgroundColor: item.color }} />{item.label}
            </span>
          ))}
        </div>
      ) : null}
    </figure>
  );
}
