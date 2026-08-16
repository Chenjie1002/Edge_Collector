import { describe, expect, it } from "vitest";
import { resolveDashboardProductSurface } from "../productSurfaces";

describe("dashboard product surface resolver", () => {
  it("uses browser-reachable local defaults for the existing Trace and V-PLC surfaces", () => {
    expect(resolveDashboardProductSurface("trace", {})).toEqual({
      ok: true,
      href: "http://127.0.0.1:8000/trace"
    });
    expect(resolveDashboardProductSurface("vplc", {})).toEqual({
      ok: true,
      href: "http://127.0.0.1:8200/vplc"
    });
  });

  it("uses configured browser-facing origins without hardcoding a remote host", () => {
    expect(
      resolveDashboardProductSurface("trace", {
        EDGE_MES_DASHBOARD_TRACE_ORIGIN: "https://mes.example"
      })
    ).toEqual({ ok: true, href: "https://mes.example/trace" });
    expect(
      resolveDashboardProductSurface("vplc", {
        EDGE_MES_DASHBOARD_VPLC_ORIGIN: "https://mes.example:8443/"
      })
    ).toEqual({ ok: true, href: "https://mes.example:8443/vplc" });
  });

  it.each([
    "",
    " http://127.0.0.1:8000",
    "http://api:8000/trace",
    "https://user:password@mes.example",
    "javascript:alert(1)"
  ])("fails closed for an invalid configured origin: %s", (origin) => {
    expect(
      resolveDashboardProductSurface("trace", {
        EDGE_MES_DASHBOARD_TRACE_ORIGIN: origin
      })
    ).toEqual({ ok: false, code: "ORIGIN_INVALID" });
  });
});
