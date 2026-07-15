import { afterEach, describe, expect, it, vi } from "vitest";
import { GET } from "../route";

afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

describe("dashboard health route", () => {
  it("returns the fixed process-only readiness response without external dependencies", async () => {
    const fetchSpy = vi.fn();
    vi.stubGlobal("fetch", fetchSpy);
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN", "http://unreachable.invalid");
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE", "invalid");

    const response = await GET();
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toContain("application/json");
    expect(body).toEqual({ status: "ok", service: "dashboard" });
    expect(Object.keys(body)).toEqual(["status", "service"]);
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
