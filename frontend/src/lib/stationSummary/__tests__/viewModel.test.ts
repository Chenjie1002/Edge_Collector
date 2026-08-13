import { describe, expect, it } from "vitest";
import type { StationSummaryClientSuccess } from "../apiClient";
import type { FixedProcessMetricName, ProcessMetric, ProcessMetricsResponse, QualityResponse } from "../schema";
import { toStationSummaryViewModel } from "../viewModel";

const query = {
  lineId: "LINE_001",
  stationId: "WS01",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z"
};

const quality: QualityResponse = {
  scope: { line_id: "LINE_001", station_id: "WS01", start_time: query.startTime, end_time: query.endTime },
  counts: { ok: 1, nok: 1, denominator: 2 },
  quality_rate: 0.5,
  nok_code_distribution: { "100": 1 },
  data_sufficiency: "SUPPORTED" as const
};

const processMetric = (name: FixedProcessMetricName, value?: number): ProcessMetric => {
  const unit = name === "quality_rate" ? "ratio" : "events";
  if (value === undefined) {
    return {
      name,
      unit,
      counting_unit: "event-count",
      status: "UNSUPPORTED",
      reason: { code: "FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED", detail: "fixture" },
      source: { authority: "not-accepted", lineage: "fact_key", fallback: "none" },
      numeric_value_allowed: false
    };
  }
  return {
    name,
    unit,
    counting_unit: "event-count",
    status: "SUPPORTED",
    reason: { code: "ACCEPTED_FACT_QUERY_OK", detail: "fixture" },
    source: { authority: "production_accepted_station_event_fact", lineage: "fact_key", fallback: "none" },
    numeric_value_allowed: true,
    value
  };
};

const process: ProcessMetricsResponse = {
  contract_version: "P1-G3-PROCESS-KPI-1.0",
  scope: { line_id: "LINE_001", station_id: "WS01", aggregation: "station" },
  window: { from: query.startTime, to: query.endTime, interval: "[from,to)", duration_seconds: 28800 },
  status: "PARTIAL" as const,
  reason: { code: "ACCEPTED_FACT_QUERY_OK", detail: "fixture" },
  source: { authority: "production_accepted_station_event_fact", identity: "fact_key", config_window_state: "UNRESOLVED", fallback: "none" },
  metrics: [
    processMetric("accepted_event_count", 2),
    processMetric("observed_accepted_event_rate", 2 / 28800),
    processMetric("quality_rate", 0.5),
    processMetric("full_oee")
  ]
};

describe("station summary view model", () => {
  it("keeps source identity, status, scope/window, and numeric permission separate", () => {
    const result: StationSummaryClientSuccess = {
      ok: true,
      quality: { ok: true, dto: quality },
      processMetrics: { ok: true, dto: process }
    };
    const viewModel = toStationSummaryViewModel(query, result);

    expect(viewModel.quality.sourceLabel).toBe("trusted Quality route");
    expect(viewModel.quality.status).toBe("SUPPORTED");
    expect(viewModel.quality.qualityRate).toBe(0.5);
    expect(viewModel.processMetrics.sourceLabel).toBe("trusted Process Metrics route");
    expect(viewModel.processMetrics.status).toBe("PARTIAL");
    expect(viewModel.processMetrics.metrics.find((metric) => metric.name === "full_oee")?.valueText).toBe("No numeric value authorized");
    expect(viewModel.processMetrics.metrics.find((metric) => metric.name === "full_oee")?.numericValueAllowed).toBe(false);
  });

  it("maps a valid zero-event response to EMPTY without turning unsupported metrics into zero", () => {
    const emptyProcess = {
      ...process,
      metrics: [processMetric("accepted_event_count", 0), processMetric("observed_accepted_event_rate", 0), processMetric("full_oee")]
    };
    const result: StationSummaryClientSuccess = {
      ok: true,
      quality: {
        ok: true,
        dto: { ...quality, counts: { ok: 0, nok: 0, denominator: 0 }, quality_rate: null, data_sufficiency: "UNAVAILABLE" }
      },
      processMetrics: { ok: true, dto: emptyProcess }
    };
    const viewModel = toStationSummaryViewModel(query, result);

    expect(viewModel.processMetrics.status).toBe("EMPTY");
    expect(viewModel.processMetrics.metrics.find((metric) => metric.name === "accepted_event_count")?.valueText).toBe("0");
    expect(viewModel.processMetrics.metrics.find((metric) => metric.name === "full_oee")?.valueText).toBe("No numeric value authorized");
    expect(viewModel.quality.qualityRateText).toBe("No numeric rate authorized");
  });

  it("maps each source failure independently and removes all production values", () => {
    const result: StationSummaryClientSuccess = {
      ok: true,
      quality: { ok: false, kind: "unavailable", message: "Quality source unavailable." },
      processMetrics: { ok: false, kind: "malformed", message: "Process Metrics response was malformed." }
    };
    const viewModel = toStationSummaryViewModel(query, result);

    expect(viewModel.quality.status).toBe("UNAVAILABLE");
    expect(viewModel.quality.message).toContain("unavailable");
    expect(viewModel.quality.counts).toBeNull();
    expect(viewModel.quality.qualityRate).toBeNull();
    expect(viewModel.quality.nokDistribution).toEqual([]);
    expect(viewModel.processMetrics.status).toBe("MALFORMED");
    expect(viewModel.processMetrics.message).toContain("malformed");
    expect(viewModel.processMetrics.metrics).toEqual([]);
  });
});
