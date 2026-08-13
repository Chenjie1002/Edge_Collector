import { describe, expect, it, vi } from "vitest";
import { fetchTrustedScopeCatalog } from "../scopeCatalog";

const catalogDto = {
  contract_version: "production-scope-options/v1",
  authority: {
    kind: "active_runtime_mapping",
    source: "config/mapping.yaml",
    config_version: "2026.06.26-slice-a",
    content_sha256: "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  },
  timezone: "Asia/Shanghai",
  utc_offset: "+08:00",
  lines: [
    {
      line_id: "LINE_001",
      name: "Demo Assembly Line Runtime",
      stations: [
        { station_id: "WS02", name: "EOL Test Station", station_order: 1 },
        { station_id: "WS03", name: "Label Station", station_order: 2 },
      ],
    },
    {
      line_id: "LINE_002",
      name: "Second Line",
      stations: [{ station_id: "WS10", name: "Pack Station", station_order: 1 }],
    },
  ],
} as const;

describe("fetchTrustedScopeCatalog", () => {
  it("requests the trusted scope route and preserves ordered lines and stations", async () => {
    const fetchImpl = vi.fn<typeof fetch>(async (input, init) => {
      expect(String(input)).toBe("https://api.example.test/api/v2/production/scope-options");
      expect(init?.method).toBe("GET");
      expect(init?.cache).toBe("no-store");
      return new Response(JSON.stringify(catalogDto), { status: 200 });
    });

    const result = await fetchTrustedScopeCatalog("https://api.example.test", fetchImpl);

    expect(result).toEqual({
      ok: true,
      catalog: {
        contractVersion: "production-scope-options/v1",
        timezone: "Asia/Shanghai",
        utcOffset: "+08:00",
        lines: [
          {
            lineId: "LINE_001",
            name: "Demo Assembly Line Runtime",
            stations: [
              { stationId: "WS02", name: "EOL Test Station", stationOrder: 1 },
              { stationId: "WS03", name: "Label Station", stationOrder: 2 },
            ],
          },
          {
            lineId: "LINE_002",
            name: "Second Line",
            stations: [{ stationId: "WS10", name: "Pack Station", stationOrder: 1 }],
          },
        ],
      },
    });
  });

  it("rejects extra authority fields without exposing the response", async () => {
    const malformed = structuredClone(catalogDto) as Record<string, unknown>;
    malformed.authority = { ...catalogDto.authority, unexpected: "no" };
    const result = await fetchTrustedScopeCatalog("https://api.example.test", async () => new Response(JSON.stringify(malformed)));
    expect(result).toEqual({ ok: false, kind: "invalid-response", message: "Scope catalog unavailable" });
  });

  it("rejects non-increasing station order", async () => {
    const malformed = structuredClone(catalogDto) as any;
    malformed.lines[0].stations[1].station_order = 1;
    const result = await fetchTrustedScopeCatalog("https://api.example.test", async () => new Response(JSON.stringify(malformed)));
    expect(result).toEqual({ ok: false, kind: "invalid-response", message: "Scope catalog unavailable" });
  });

  it("maps HTTP and transport failures to the same unavailable state", async () => {
    const httpResult = await fetchTrustedScopeCatalog("https://api.example.test", async () => new Response("blocked", { status: 503 }));
    expect(httpResult).toEqual({ ok: false, kind: "unavailable", message: "Scope catalog unavailable" });

    const transportResult = await fetchTrustedScopeCatalog("https://api.example.test", async () => {
      throw new Error("network detail must not escape");
    });
    expect(transportResult).toEqual({ ok: false, kind: "invalid-response", message: "Scope catalog unavailable" });
  });
});
