import { describe, expect, it } from "vitest";
import type { TrustedAcceptedEventsApiOrigin } from "../../acceptedStationEvents/apiOrigin";
import { buildStationSummaryEndpoint } from "../browserEndpoint";

describe("buildStationSummaryEndpoint", () => {
  it("uses the same-origin proxy for the container-only API origin in a browser", () => {
    const endpoint = buildStationSummaryEndpoint(
      "/api/v2/production/line-summary",
      "http://api:8000" as TrustedAcceptedEventsApiOrigin,
    );

    expect(endpoint.origin).toBe(window.location.origin);
    expect(endpoint.pathname).toBe("/api/station-summary/production/line-summary");
  });

  it("keeps a browser-reachable or production trusted origin direct", () => {
    const endpoint = buildStationSummaryEndpoint(
      "/api/v2/production/line-summary",
      "https://accepted-api.example" as TrustedAcceptedEventsApiOrigin,
    );

    expect(endpoint.toString()).toBe("https://accepted-api.example/api/v2/production/line-summary");
  });
});
