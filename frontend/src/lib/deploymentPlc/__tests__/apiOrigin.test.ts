import { afterEach, describe, expect, it, vi } from "vitest";

import { resolveDeploymentApiOrigin } from "../apiOrigin";

afterEach(() => {
  vi.unstubAllEnvs();
});

describe("deployment API origin resolver", () => {
  it("uses the runtime dashboard API origin when no explicit environment is passed", () => {
    vi.stubEnv("EDGE_MES_DASHBOARD_API_ORIGIN", "http://api:8000");

    expect(resolveDeploymentApiOrigin()).toEqual({
      ok: true,
      origin: "http://api:8000"
    });
  });
});
