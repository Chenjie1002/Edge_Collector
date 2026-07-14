import { buildAcceptedStationEventsQuery, type AcceptedStationEventsQuery } from "./query";
import { parseAcceptedStationEventsEnvelopeJson, type AcceptedStationEventsEnvelope } from "./schema";
import type { TrustedAcceptedEventsApiOrigin } from "./apiOrigin";

export type AcceptedStationEventsClientResult =
  | { ok: true; envelope: AcceptedStationEventsEnvelope }
  | { ok: false; kind: "invalid-query" | "unavailable" | "error"; message: string };

export async function fetchAcceptedStationEvents(
  query: AcceptedStationEventsQuery,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
  fetchImpl: typeof fetch = fetch
): Promise<AcceptedStationEventsClientResult> {
  let params: URLSearchParams;
  try {
    params = buildAcceptedStationEventsQuery(query);
  } catch (error) {
    return { ok: false, kind: "invalid-query", message: error instanceof Error ? error.message : "invalid query" };
  }

  try {
    const endpoint = new URL("/api/v2/production/accepted-station-events", trustedApiOrigin);
    endpoint.search = params.toString();
    const response = await fetchImpl(endpoint, {
      method: "GET",
      cache: "no-store",
      credentials: "omit",
      redirect: "error"
    });

    if (!response.ok) {
      if (response.status >= 400 && response.status < 500) {
        return { ok: false, kind: "invalid-query", message: `accepted events query rejected (${response.status})` };
      }
      if (response.status === 503) {
        return { ok: false, kind: "unavailable", message: "accepted fact source unavailable" };
      }
      return { ok: false, kind: "error", message: `accepted events request failed (${response.status})` };
    }

    try {
      const rawText = await response.text();
      return { ok: true, envelope: parseAcceptedStationEventsEnvelopeJson(rawText) };
    } catch {
      return { ok: false, kind: "error", message: "Accepted events response was invalid." };
    }
  } catch {
    return { ok: false, kind: "error", message: "Accepted events request failed." };
  }
}
