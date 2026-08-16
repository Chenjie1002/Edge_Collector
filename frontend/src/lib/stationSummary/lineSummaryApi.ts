import type { TrustedAcceptedEventsApiOrigin } from "../acceptedStationEvents/apiOrigin";
import { validateLineSummaryQuery, type LineSummaryQuery } from "./lineSummaryQuery";
import { parseLineSummaryResponseJson, type LineSummary } from "./lineSummarySchema";

export type LineSummaryClientFailureKind = "invalid-query" | "unavailable" | "malformed" | "error";

export type LineSummaryClientResult =
  | { ok: true; summary: LineSummary }
  | { ok: false; kind: LineSummaryClientFailureKind; message: string };

function sameInstant(left: string, right: string): boolean {
  return Date.parse(left) === Date.parse(right);
}

function scopeMatches(query: LineSummaryQuery, summary: LineSummary): boolean {
  return (
    summary.scope.lineId === query.lineId &&
    sameInstant(summary.scope.startTime, query.startTime) &&
    sameInstant(summary.scope.endTime, query.endTime) &&
    summary.scope.cohortBasis === "terminal_completed"
  );
}

export async function fetchLineSummary(
  query: LineSummaryQuery,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
  fetchImpl: typeof fetch = fetch,
): Promise<LineSummaryClientResult> {
  const validation = validateLineSummaryQuery(query);
  if (!validation.ok) return { ok: false, kind: "invalid-query", message: validation.reason };

  const endpoint = new URL("/api/v2/production/line-summary", trustedApiOrigin);
  const params = new URLSearchParams();
  params.set("line_id", validation.query.lineId);
  params.set("start_time", validation.query.startTime);
  params.set("end_time", validation.query.endTime);
  endpoint.search = params.toString();

  let response: Response;
  try {
    response = await fetchImpl(endpoint, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error",
    });
  } catch {
    return { ok: false, kind: "error", message: "Line summary request failed." };
  }

  if (!response.ok) {
    if (response.status >= 400 && response.status < 500) {
      return { ok: false, kind: "invalid-query", message: `Line summary query rejected (${response.status}).` };
    }
    if (response.status === 503) return { ok: false, kind: "unavailable", message: "Line summary source unavailable." };
    return { ok: false, kind: "error", message: `Line summary request failed (${response.status}).` };
  }

  let summary: LineSummary;
  try {
    summary = parseLineSummaryResponseJson(await response.text());
  } catch {
    return { ok: false, kind: "malformed", message: "Line summary response was malformed." };
  }
  if (!scopeMatches(validation.query, summary)) {
    return { ok: false, kind: "malformed", message: "Line summary response was malformed." };
  }
  return { ok: true, summary };
}
