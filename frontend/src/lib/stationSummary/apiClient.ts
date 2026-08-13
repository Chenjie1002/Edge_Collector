import { resolveTrustedAcceptedEventsApiOrigin, type TrustedAcceptedEventsApiOrigin } from "../acceptedStationEvents/apiOrigin";
import { buildProcessMetricsQuery, buildQualityQuery, type StationSummaryQuery, validateStationSummaryQuery } from "./query";
import {
  parseProcessMetricsResponseJson,
  parseQualityResponseJson,
  type ProcessMetricsResponse,
  type QualityResponse
} from "./schema";

export type StationSummarySourceFailureKind = "invalid-query" | "unavailable" | "malformed" | "error";

export type StationSummarySourceResult<T> =
  | { ok: true; dto: T }
  | { ok: false; kind: StationSummarySourceFailureKind; message: string };

export type StationSummaryClientSuccess = {
  ok: true;
  quality: StationSummarySourceResult<QualityResponse>;
  processMetrics: StationSummarySourceResult<ProcessMetricsResponse>;
};

export type StationSummaryClientResult =
  | StationSummaryClientSuccess
  | { ok: false; kind: "invalid-query"; message: string };

function sameInstant(left: string, right: string): boolean {
  return Date.parse(left) === Date.parse(right);
}

function qualityScopeMatches(query: StationSummaryQuery, dto: QualityResponse): boolean {
  return (
    dto.scope.line_id === query.lineId &&
    dto.scope.station_id === query.stationId &&
    sameInstant(dto.scope.start_time, query.startTime) &&
    sameInstant(dto.scope.end_time, query.endTime)
  );
}

function processScopeMatches(query: StationSummaryQuery, dto: ProcessMetricsResponse): boolean {
  return (
    dto.scope.line_id === query.lineId &&
    dto.scope.station_id === query.stationId &&
    sameInstant(dto.window.from, query.startTime) &&
    sameInstant(dto.window.to, query.endTime) &&
    dto.window.duration_seconds === (Date.parse(query.endTime) - Date.parse(query.startTime)) / 1000
  );
}

async function fetchQuality(
  query: StationSummaryQuery,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
  fetchImpl: typeof fetch
): Promise<StationSummarySourceResult<QualityResponse>> {
  try {
    const endpoint = new URL("/api/v2/production/quality", trustedApiOrigin);
    endpoint.search = buildQualityQuery(query).toString();
    const response = await fetchImpl(endpoint, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error"
    });
    if (!response.ok) {
      if (response.status >= 400 && response.status < 500) {
        return { ok: false, kind: "invalid-query", message: `Quality query rejected (${response.status}).` };
      }
      if (response.status === 503) return { ok: false, kind: "unavailable", message: "Quality source unavailable." };
      return { ok: false, kind: "error", message: `Quality request failed (${response.status}).` };
    }

    const dto = parseQualityResponseJson(await response.text());
    if (!qualityScopeMatches(query, dto)) throw new Error("scope mismatch");
    return { ok: true, dto };
  } catch (error) {
    if (error instanceof Error && error.message === "scope mismatch") {
      return { ok: false, kind: "malformed", message: "Quality response was malformed." };
    }
    if (error instanceof Error && error.message === "malformed station summary response") {
      return { ok: false, kind: "malformed", message: "Quality response was malformed." };
    }
    if (error instanceof Error && /invalid|forbidden|missing|Quality/.test(error.message)) {
      return { ok: false, kind: "malformed", message: "Quality response was malformed." };
    }
    return { ok: false, kind: "error", message: "Quality request failed." };
  }
}

async function fetchProcessMetrics(
  query: StationSummaryQuery,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
  fetchImpl: typeof fetch
): Promise<StationSummarySourceResult<ProcessMetricsResponse>> {
  try {
    const endpoint = new URL("/api/v2/process-metrics", trustedApiOrigin);
    endpoint.search = buildProcessMetricsQuery(query).toString();
    const response = await fetchImpl(endpoint, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error"
    });
    if (!response.ok) {
      if (response.status >= 400 && response.status < 500) {
        return { ok: false, kind: "invalid-query", message: `Process Metrics query rejected (${response.status}).` };
      }
      if (response.status === 503) return { ok: false, kind: "unavailable", message: "Process Metrics source unavailable." };
      return { ok: false, kind: "error", message: `Process Metrics request failed (${response.status}).` };
    }

    const dto = parseProcessMetricsResponseJson(await response.text());
    if (!processScopeMatches(query, dto)) throw new Error("scope mismatch");
    return { ok: true, dto };
  } catch (error) {
    if (error instanceof Error && (error.message === "scope mismatch" || error.message === "malformed station summary response")) {
      return { ok: false, kind: "malformed", message: "Process Metrics response was malformed." };
    }
    if (error instanceof Error && /invalid|forbidden|missing|Process/.test(error.message)) {
      return { ok: false, kind: "malformed", message: "Process Metrics response was malformed." };
    }
    return { ok: false, kind: "error", message: "Process Metrics request failed." };
  }
}

export async function fetchStationSummary(
  query: StationSummaryQuery,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
  fetchImpl: typeof fetch = fetch
): Promise<StationSummaryClientResult> {
  const validation = validateStationSummaryQuery(query);
  if (!validation.ok) return { ok: false, kind: "invalid-query", message: validation.reason };

  const [quality, processMetrics] = await Promise.all([
    fetchQuality(validation.query, trustedApiOrigin, fetchImpl),
    fetchProcessMetrics(validation.query, trustedApiOrigin, fetchImpl)
  ]);
  return { ok: true, quality, processMetrics };
}

export function resolveStationSummaryOrigin() {
  return resolveTrustedAcceptedEventsApiOrigin();
}
