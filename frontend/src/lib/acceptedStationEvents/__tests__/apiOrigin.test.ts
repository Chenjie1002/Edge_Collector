import { afterEach, describe, expect, it, vi } from "vitest";
import type { AcceptedEventsApiOriginEnvironment } from "../apiOrigin";

const safeMessage = "Accepted events service is not configured.";

async function loadResolver() {
  vi.resetModules();
  return import("../apiOrigin");
}

function expectSuccessOwnKeys(result: unknown) {
  expect(result).toMatchObject({ ok: true });
  expect(Object.keys(result as object).sort()).toEqual(["ok", "origin"]);
}

function expectFailure(
  result: unknown,
  code: string,
  environment: AcceptedEventsApiOriginEnvironment
) {
  expect(result).toMatchObject({ ok: false, code, message: safeMessage });
  expect(Object.keys(result as object).sort()).toEqual(["code", "message", "ok"]);
  const serialized = JSON.stringify(result);
  if (environment.EDGE_MES_DASHBOARD_API_ORIGIN) {
    expect(serialized).not.toContain(environment.EDGE_MES_DASHBOARD_API_ORIGIN);
  }
  if (environment.EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE) {
    expect(serialized).not.toContain(environment.EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE);
  }
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe.sequential("trusted accepted-events API origin resolver", () => {
  it.each([
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:3100",
    "http://127.0.0.1:3100/",
    "http://localhost:8000",
    "http://localhost:8000/",
    "http://localhost:3100",
    "http://localhost:3100/",
    "http://[::1]:8000",
    "http://[::1]:8000/",
    "http://[::1]:3100",
    "http://[::1]:3100/"
  ])("accepts the exact local form %s", async (origin) => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const result = resolveTrustedAcceptedEventsApiOrigin({
      EDGE_MES_DASHBOARD_API_ORIGIN: origin,
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local"
    });

    expectSuccessOwnKeys(result);
    if (result.ok) expect(result.origin).toBe(new URL(origin).origin);
  });

  it.each([
    ["http://api:8000", "container"],
    ["http://api:8000/", "container"],
    ["https://accepted-api.example", "production"],
    ["https://accepted-api.example/", "production"],
    ["https://xn--bcher-kva.example", "production"],
    ["https://1.api.example", "production"],
    ["https://api1.example", "production"]
  ])("accepts the exact %s origin under its selected profile", async (origin, profile) => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const result = resolveTrustedAcceptedEventsApiOrigin({
      EDGE_MES_DASHBOARD_API_ORIGIN: origin,
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: profile
    });

    expectSuccessOwnKeys(result);
    if (result.ok) expect(result.origin).toBe(new URL(origin).origin);
  });

  it.each([
    ["ORIGIN_MISSING", { EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }],
    ["PROFILE_MISSING", { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000" }],
    ["ORIGIN_EMPTY", { EDGE_MES_DASHBOARD_API_ORIGIN: "", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }],
    ["PROFILE_EMPTY", { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "" }],
    ["PROFILE_UNSUPPORTED", { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "staging" }],
    ["ORIGIN_NON_CANONICAL", { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:08000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }],
    ["ORIGIN_PROFILE_MISMATCH", { EDGE_MES_DASHBOARD_API_ORIGIN: "http://api:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }],
    ["ORIGIN_MALFORMED", { EDGE_MES_DASHBOARD_API_ORIGIN: "https://xn--a.example", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production" }]
  ] as const)("returns the closed safe failure %s", async (code, environment) => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    expectFailure(resolveTrustedAcceptedEventsApiOrigin(environment), code, environment);
  });

  it.each([
    " http://127.0.0.1:8000",
    "http://127.0.0.1:8000\n",
    "http://127.0.0.1:8000\u0000",
    "HTTP://127.0.0.1:8000",
    "http://LOCALHOST:8000",
    "http://localhost.:8000",
    "https://accepted-api.example:443",
    "http://localhost:08000",
    "http://[0:0:0:0:0:0:0:1]:8000",
    "https://b\u00fccher.example",
    "https://accepted-api%2eexample",
    "http:\\localhost:8000",
    "https://accepted-api.example//",
    "https://user@accepted-api.example",
    "https://accepted-api.example?cursor=opaque",
    "https://accepted-api.example#fragment",
    "https://accepted-api",
    "http://localhost:99999"
  ])("rejects non-canonical raw origin %s", async (origin) => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const environment = {
      EDGE_MES_DASHBOARD_API_ORIGIN: origin,
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: origin.startsWith("https") ? "production" : "local"
    } as const;
    expectFailure(resolveTrustedAcceptedEventsApiOrigin(environment), "ORIGIN_NON_CANONICAL", environment);
  });

  it.each([
    "https://127.0.0.1",
    "https://127.1",
    "https://0177.0.0.1",
    "https://0x7f.0.0.1",
    "https://[::1]"
  ])("rejects production IP-like raw origin %s before URL parsing", async (origin) => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const environment: AcceptedEventsApiOriginEnvironment = {
      EDGE_MES_DASHBOARD_API_ORIGIN: origin,
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production"
    };

    expectFailure(resolveTrustedAcceptedEventsApiOrigin(environment), "ORIGIN_NON_CANONICAL", environment);
  });

  it("reads each supplied environment property exactly once on success", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    let originReads = 0;
    let profileReads = 0;
    const environment: AcceptedEventsApiOriginEnvironment = {
      get EDGE_MES_DASHBOARD_API_ORIGIN() {
        originReads += 1;
        return "http://api:8000";
      },
      get EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE() {
        profileReads += 1;
        return "container";
      }
    };

    expect(resolveTrustedAcceptedEventsApiOrigin(environment).ok).toBe(true);
    expect(originReads).toBe(1);
    expect(profileReads).toBe(1);
  });

  it("reads each supplied environment property exactly once on failure", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    let originReads = 0;
    let profileReads = 0;
    const environment: AcceptedEventsApiOriginEnvironment = {
      get EDGE_MES_DASHBOARD_API_ORIGIN() {
        originReads += 1;
        return "http://127.0.0.1:08000";
      },
      get EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE() {
        profileReads += 1;
        return "local";
      }
    };

    expect(resolveTrustedAcceptedEventsApiOrigin(environment).ok).toBe(false);
    expect(originReads).toBe(1);
    expect(profileReads).toBe(1);
  });

  it("uses the current typed environment pair for each invocation", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const first = resolveTrustedAcceptedEventsApiOrigin({
      EDGE_MES_DASHBOARD_API_ORIGIN: "http://api:8000",
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "container"
    });
    const second = resolveTrustedAcceptedEventsApiOrigin({
      EDGE_MES_DASHBOARD_API_ORIGIN: "https://accepted-api.example",
      EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production"
    });

    expect(first).toMatchObject({ ok: true, origin: "http://api:8000" });
    expect(second).toMatchObject({ ok: true, origin: "https://accepted-api.example" });
  });

  it("deduplicates same-code logs, logs distinct codes, and never leaks raw configuration", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const rawOrigin = "http://127.0.0.1:08000?secret=never-log";
    const rawProfile = "unsafe-profile-never-log";

    resolveTrustedAcceptedEventsApiOrigin({ EDGE_MES_DASHBOARD_API_ORIGIN: rawOrigin, EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" });
    resolveTrustedAcceptedEventsApiOrigin({ EDGE_MES_DASHBOARD_API_ORIGIN: rawOrigin, EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" });
    resolveTrustedAcceptedEventsApiOrigin({ EDGE_MES_DASHBOARD_API_ORIGIN: "http://api:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: rawProfile });

    expect(error).toHaveBeenCalledTimes(2);
    for (const call of error.mock.calls) {
      expect(call.join(" ")).toContain("DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR");
      expect(call.join(" ")).not.toContain(rawOrigin);
      expect(call.join(" ")).not.toContain(rawProfile);
    }
  });

  it("limits logging state to the eight closed safe codes", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const cases: AcceptedEventsApiOriginEnvironment[] = [
      { EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "staging" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:08000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "http://api:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" },
      { EDGE_MES_DASHBOARD_API_ORIGIN: "https://xn--a.example", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production" }
    ];

    for (const environment of cases) resolveTrustedAcceptedEventsApiOrigin(environment);
    for (const environment of cases) resolveTrustedAcceptedEventsApiOrigin(environment);

    expect(error).toHaveBeenCalledTimes(8);
  });

  it("contains a throwing logger and records the attempt before the throw", async () => {
    const { resolveTrustedAcceptedEventsApiOrigin } = await loadResolver();
    const error = vi.spyOn(console, "error").mockImplementation(() => {
      throw new Error("logger failure");
    });
    const environment = { EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" } as const;

    expectFailure(resolveTrustedAcceptedEventsApiOrigin(environment), "ORIGIN_MISSING", environment);
    expectFailure(resolveTrustedAcceptedEventsApiOrigin(environment), "ORIGIN_MISSING", environment);
    expect(error).toHaveBeenCalledTimes(1);
  });

  it("resets per-code logging only through module reset and dynamic import", async () => {
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    const environment = { EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" } as const;
    const first = await loadResolver();
    first.resolveTrustedAcceptedEventsApiOrigin(environment);
    const second = await loadResolver();
    second.resolveTrustedAcceptedEventsApiOrigin(environment);

    expect(error).toHaveBeenCalledTimes(2);
    expect(Object.keys(first)).not.toContain("resetAcceptedEventsApiOriginLoggingForTests");
  });
});
