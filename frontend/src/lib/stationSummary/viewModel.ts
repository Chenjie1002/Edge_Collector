import type { StationSummaryClientSuccess, StationSummarySourceFailureKind, StationSummarySourceResult } from "./apiClient";
import { FIXED_PROCESS_METRIC_NAMES, type ProcessMetric, type ProcessMetricsResponse, type QualityResponse } from "./schema";
import type { StationSummaryQuery } from "./query";

export type StationSummaryStatus =
  | "SUPPORTED"
  | "PARTIAL"
  | "UNAVAILABLE"
  | "UNSUPPORTED"
  | "EMPTY"
  | "INVALID_QUERY"
  | "MALFORMED"
  | "ERROR";

export type QualitySummaryViewModel = {
  sourceLabel: "trusted Quality route";
  status: StationSummaryStatus;
  dataSufficiency: QualityResponse["data_sufficiency"] | null;
  scopeLabel: string;
  windowLabel: string;
  counts: QualityResponse["counts"] | null;
  qualityRate: number | null;
  qualityRateText: string;
  nokDistribution: Array<[string, number]>;
  message?: string;
};

export type ProcessMetricViewModel = {
  name: ProcessMetric["name"];
  unit: string;
  countingUnit: ProcessMetric["counting_unit"];
  status: ProcessMetric["status"];
  reason: string;
  source: string;
  numericValueAllowed: boolean;
  valueText: string;
};

export type ProcessMetricsPanelViewModel = {
  sourceLabel: "trusted Process Metrics route";
  status: StationSummaryStatus;
  scopeLabel: string;
  windowLabel: string;
  reason: string;
  sourceAuthority: string;
  metrics: ProcessMetricViewModel[];
  message?: string;
};

export type StationSummaryViewModel = {
  query: StationSummaryQuery;
  quality: QualitySummaryViewModel;
  processMetrics: ProcessMetricsPanelViewModel;
};

function scopeLabel(lineId: string, stationId: string): string {
  return `${lineId} / ${stationId}`;
}

function windowLabel(from: string, to: string): string {
  return `${from} → ${to} [from,to)`;
}

function percentageText(value: number | null): string {
  if (value === null) return "No numeric rate authorized";
  const percent = (value * 100).toFixed(2).replace(/\.?(0+)$/, "");
  return `${percent}%`;
}

function failureStatus(kind: StationSummarySourceFailureKind): StationSummaryStatus {
  if (kind === "invalid-query") return "INVALID_QUERY";
  if (kind === "unavailable") return "UNAVAILABLE";
  if (kind === "malformed") return "MALFORMED";
  return "ERROR";
}

function emptyQuality(): QualitySummaryViewModel {
  return {
    sourceLabel: "trusted Quality route",
    status: "ERROR",
    dataSufficiency: null,
    scopeLabel: "—",
    windowLabel: "—",
    counts: null,
    qualityRate: null,
    qualityRateText: "No numeric rate authorized",
    nokDistribution: []
  };
}

function mapQuality(query: StationSummaryQuery, source: StationSummarySourceResult<QualityResponse>): QualitySummaryViewModel {
  if (!source.ok) {
    return {
      ...emptyQuality(),
      status: failureStatus(source.kind),
      scopeLabel: scopeLabel(query.lineId, query.stationId),
      windowLabel: windowLabel(query.startTime, query.endTime),
      message: source.message
    };
  }
  const dto = source.dto;
  return {
    sourceLabel: "trusted Quality route",
    status: dto.data_sufficiency,
    dataSufficiency: dto.data_sufficiency,
    scopeLabel: scopeLabel(dto.scope.line_id, dto.scope.station_id),
    windowLabel: windowLabel(dto.scope.start_time, dto.scope.end_time),
    counts: dto.counts,
    qualityRate: dto.quality_rate,
    qualityRateText: dto.counts.denominator > 0 && dto.quality_rate !== null ? percentageText(dto.quality_rate) : "No numeric rate authorized",
    nokDistribution: Object.entries(dto.nok_code_distribution),
    message: dto.data_sufficiency === "UNAVAILABLE" ? "Quality denominator is unavailable." : undefined
  };
}

function mapProcessMetric(metric: ProcessMetric): ProcessMetricViewModel {
  return {
    name: metric.name,
    unit: metric.unit,
    countingUnit: metric.counting_unit,
    status: metric.status,
    reason: metric.reason.detail,
    source: metric.source.authority,
    numericValueAllowed: metric.numeric_value_allowed,
    valueText: metric.numeric_value_allowed && metric.value !== undefined ? String(metric.value) : "No numeric value authorized"
  };
}

function mapProcessMetrics(query: StationSummaryQuery, source: StationSummarySourceResult<ProcessMetricsResponse>): ProcessMetricsPanelViewModel {
  if (!source.ok) {
    return {
      sourceLabel: "trusted Process Metrics route",
      status: failureStatus(source.kind),
      scopeLabel: scopeLabel(query.lineId, query.stationId),
      windowLabel: windowLabel(query.startTime, query.endTime),
      reason: source.message,
      sourceAuthority: "production_accepted_station_event_fact",
      metrics: [],
      message: source.message
    };
  }
  const dto = source.dto;
  const ordered = [...dto.metrics].sort((left, right) => FIXED_PROCESS_METRIC_NAMES.indexOf(left.name) - FIXED_PROCESS_METRIC_NAMES.indexOf(right.name));
  const countMetric = dto.metrics.find((metric) => metric.name === "accepted_event_count");
  const status: StationSummaryStatus = countMetric?.numeric_value_allowed && countMetric.value === 0 ? "EMPTY" : dto.status;
  return {
    sourceLabel: "trusted Process Metrics route",
    status,
    scopeLabel: scopeLabel(dto.scope.line_id, dto.scope.station_id),
    windowLabel: windowLabel(dto.window.from, dto.window.to),
    reason: dto.reason.detail,
    sourceAuthority: dto.source.authority,
    metrics: ordered.map(mapProcessMetric),
    message: status === "EMPTY" ? "No accepted station-result facts returned for this bounded scope." : undefined
  };
}

export function toStationSummaryViewModel(query: StationSummaryQuery, result: StationSummaryClientSuccess): StationSummaryViewModel {
  return {
    query,
    quality: mapQuality(query, result.quality),
    processMetrics: mapProcessMetrics(query, result.processMetrics)
  };
}
