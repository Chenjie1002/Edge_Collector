import { NextRequest } from "next/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllEnvs();
});

describe("Station Summary browser proxy", () => {
  it("proxies only the trusted read-only line-summary path", async () => {
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN", "http://api:8000");
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE", "container");
    const upstreamResponse = new Response('{"ok":true}', {
      status: 200,
      headers: { "content-type": "application/json" },
    });
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(upstreamResponse);
    const request = new NextRequest("http://dashboard.test/api/station-summary/production/line-summary?line_id=LINE_001");

    const response = await GET(request, { params: Promise.resolve({ path: ["production", "line-summary"] }) });

    expect(response.status).toBe(200);
    expect(await response.text()).toBe('{"ok":true}');
    expect(fetchSpy).toHaveBeenCalledWith(
      new URL("http://api:8000/api/v2/production/line-summary?line_id=LINE_001"),
      expect.objectContaining({ method: "GET", cache: "no-store", redirect: "error" }),
    );
  });

  it("fails closed for an unlisted path without contacting the API", async () => {
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN", "http://api:8000");
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE", "container");
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const request = new NextRequest("http://dashboard.test/api/station-summary/deployment/activate");

    const response = await GET(request, { params: Promise.resolve({ path: ["deployment", "activate"] }) });

    expect(response.status).toBe(404);
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
