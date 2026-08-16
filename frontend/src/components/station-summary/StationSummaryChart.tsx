"use client";

import { useState } from "react";

export type StationSummaryChartPoint = Readonly<{
  label: string;
  value: number;
}>;

type Props = Readonly<{
  ariaLabel: string;
  points: readonly StationSummaryChartPoint[];
  xAxisLabel: string;
  yAxisLabel: string;
  unit: string;
  emptyMessage: string;
  variant?: "bar" | "line";
}>;

const WIDTH = 720;
const HEIGHT = 280;
const MARGIN = { top: 24, right: 24, bottom: 64, left: 68 };

function displayValue(value: number): string {
  return String(value);
}

function pointLabel(point: StationSummaryChartPoint, unit: string): string {
  return `${point.label} · ${displayValue(point.value)} ${unit}`;
}

export function StationSummaryChart({
  ariaLabel,
  points,
  xAxisLabel,
  yAxisLabel,
  unit,
  emptyMessage,
  variant = "bar",
}: Props) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  if (!points.length) return <p className="mes-empty">{emptyMessage}</p>;

  const plotWidth = WIDTH - MARGIN.left - MARGIN.right;
  const plotHeight = HEIGHT - MARGIN.top - MARGIN.bottom;
  const baseline = MARGIN.top + plotHeight;
  const maximum = Math.max(1, ...points.map((point) => point.value));
  const xFor = (index: number) => MARGIN.left + (points.length === 1 ? plotWidth / 2 : (index / (points.length - 1)) * plotWidth);
  const yFor = (value: number) => baseline - (value / maximum) * plotHeight;
  const barWidth = Math.min(64, Math.max(18, plotWidth / Math.max(points.length, 1) * 0.58));
  const linePoints = points.map((point, index) => `${xFor(index)},${yFor(point.value)}`).join(" ");
  const activePoint = activeIndex === null ? null : points[activeIndex];

  return (
    <figure className="mes-svg-chart" aria-label={ariaLabel}>
      <div className="mes-chart-axis-summary" aria-label={`${ariaLabel} axes`}>
        <span>x = {xAxisLabel}</span>
        <span>y = {yAxisLabel}</span>
        <span>unit = {unit}</span>
      </div>
      <svg role="img" aria-label={ariaLabel} viewBox={`0 0 ${WIDTH} ${HEIGHT}`}>
        <line className="mes-chart-axis" data-axis="y" x1={MARGIN.left} y1={MARGIN.top} x2={MARGIN.left} y2={baseline} />
        <line className="mes-chart-axis" data-axis="x" x1={MARGIN.left} y1={baseline} x2={WIDTH - MARGIN.right} y2={baseline} />
        <line className="mes-chart-gridline" x1={MARGIN.left} y1={MARGIN.top + plotHeight / 2} x2={WIDTH - MARGIN.right} y2={MARGIN.top + plotHeight / 2} />
        <text className="mes-chart-tick" x={MARGIN.left - 10} y={MARGIN.top + 4} textAnchor="end">{displayValue(maximum)}</text>
        <text className="mes-chart-tick" x={MARGIN.left - 10} y={MARGIN.top + plotHeight / 2 + 4} textAnchor="end">{displayValue(maximum / 2)}</text>
        <text className="mes-chart-tick" x={MARGIN.left - 10} y={baseline + 4} textAnchor="end">0</text>
        <text className="mes-chart-axis-title" x={WIDTH / 2} y={HEIGHT - 10} textAnchor="middle">{xAxisLabel}</text>
        <text className="mes-chart-axis-title" transform={`translate(16 ${MARGIN.top + plotHeight / 2}) rotate(-90)`} textAnchor="middle">{yAxisLabel}</text>
        {variant === "line" ? <polyline className="mes-chart-line" points={linePoints} /> : null}
        {points.map((point, index) => {
          const x = xFor(index);
          const y = yFor(point.value);
          const label = pointLabel(point, unit);
          const setActive = () => setActiveIndex(index);
          return variant === "line" ? (
            <circle
              key={`${point.label}-${index}`}
              className="mes-chart-point"
              role="button"
              tabIndex={0}
              aria-label={label}
              cx={x}
              cy={y}
              r={6}
              onMouseEnter={setActive}
              onFocus={setActive}
              onMouseLeave={() => setActiveIndex(null)}
              onBlur={() => setActiveIndex(null)}
            >
              <title>{label}</title>
            </circle>
          ) : (
            <rect
              key={`${point.label}-${index}`}
              className="mes-chart-bar"
              role="button"
              tabIndex={0}
              aria-label={label}
              x={x - barWidth / 2}
              y={y}
              width={barWidth}
              height={Math.max(0, baseline - y)}
              rx={4}
              onMouseEnter={setActive}
              onFocus={setActive}
              onMouseLeave={() => setActiveIndex(null)}
              onBlur={() => setActiveIndex(null)}
            >
              <title>{label}</title>
            </rect>
          );
        })}
        {points.map((point, index) => (
          <text key={`label-${point.label}-${index}`} className="mes-chart-x-tick" x={xFor(index)} y={baseline + 22} textAnchor="middle">{point.label}</text>
        ))}
      </svg>
      <div className="mes-chart-reading" role="status" aria-live="polite">
        {activePoint ? pointLabel(activePoint, unit) : "Hover or focus a point to read the exact value."}
      </div>
    </figure>
  );
}
