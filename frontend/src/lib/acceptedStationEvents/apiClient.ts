import { buildAcceptedStationEventsQuery, type AcceptedStationEventsQuery } from "./query";
import { parseAcceptedStationEventsEnvelope, type AcceptedStationEventsEnvelope } from "./schema";

export type AcceptedStationEventsClientResult =
  | { ok: true; envelope: AcceptedStationEventsEnvelope }
  | { ok: false; kind: "invalid-query" | "unavailable" | "error"; message: string };

export async function fetchAcceptedStationEvents(
  query: AcceptedStationEventsQuery,
  fetchImpl: typeof fetch = fetch
): Promise<AcceptedStationEventsClientResult> {
  let params: URLSearchParams;
  try {
    params = buildAcceptedStationEventsQuery(query);
  } catch (error) {
    return { ok: false, kind: "invalid-query", message: error instanceof Error ? error.message : "invalid query" };
  }

  try {
    const response = await fetchImpl(`/api/v2/production/accepted-station-events?${params.toString()}`, {
      method: "GET",
      cache: "no-store"
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

    return { ok: true, envelope: parseAcceptedStationEventsEnvelope(await response.json()) };
  } catch (error) {
    return { ok: false, kind: "error", message: error instanceof Error ? error.message : "accepted events request failed" };
  }
}
