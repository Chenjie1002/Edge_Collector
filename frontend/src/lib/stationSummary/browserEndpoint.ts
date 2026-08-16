import type { TrustedAcceptedEventsApiOrigin } from "../acceptedStationEvents/apiOrigin";

const CONTAINER_API_ORIGIN = "http://api:8000" as TrustedAcceptedEventsApiOrigin;
const API_PREFIX = "/api/v2";

export function buildStationSummaryEndpoint(
  path: string,
  trustedApiOrigin: TrustedAcceptedEventsApiOrigin,
): URL {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  if (
    typeof window !== "undefined" &&
    trustedApiOrigin === CONTAINER_API_ORIGIN &&
    normalizedPath.startsWith(`${API_PREFIX}/`)
  ) {
    return new URL(`/api/station-summary${normalizedPath.slice(API_PREFIX.length)}`, window.location.origin);
  }
  return new URL(normalizedPath, trustedApiOrigin);
}
