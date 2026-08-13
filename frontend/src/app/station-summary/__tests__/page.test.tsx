import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import StationSummaryPage, { StationSummaryPageView } from "../page";
import { fetchStationSummary } from "../../../lib/stationSummary/apiClient";
import {
  resolveTrustedAcceptedEventsApiOrigin,
  type TrustedAcceptedEventsApiOrigin,
} from "../../../lib/acceptedStationEvents/apiOrigin";
import { fetchTrustedScopeCatalog } from "../../../lib/stationSummary/scopeCatalog";

vi.mock("../../../lib/stationSummary/apiClient", () => ({
  fetchStationSummary: vi.fn(),
}));

vi.mock("../../../lib/stationSummary/scopeCatalog", () => ({
  fetchTrustedScopeCatalog: vi.fn(),
}));

vi.mock("../../../lib/acceptedStationEvents/apiOrigin", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../../../lib/acceptedStationEvents/apiOrigin")>();
  return { ...actual, resolveTrustedAcceptedEventsApiOrigin: vi.fn() };
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

const catalog = {
  contractVersion: "production-scope-options/v1",
  timezone: "Asia/Shanghai",
  utcOffset: "+08:00",
  lines: [
    {
      lineId: "LINE_001",
      name: "Demo Assembly Line Runtime",
      stations: [{ stationId: "WS01", name: "Screw Station", stationOrder: 1 }],
    },
  ],
} as const;

const trustedTestApiOrigin: TrustedAcceptedEventsApiOrigin = "https://api.example.test" as TrustedAcceptedEventsApiOrigin;

describe("station summary page", () => {
  it("renders loading without prior production values", () => {
    render(
      <StationSummaryPageView
        state={{
          kind: "loading",
          message: "Loading station summary.",
          priorDataNotice: "Prior station values are hidden while this request is loading.",
        }}
      />,
    );

    const main = screen.getByRole("main");
    expect(main.classList.contains("dashboard-shell")).toBe(true);
    expect(main.classList.contains("station-summary-shell")).toBe(true);
    expect(screen.getByRole("heading", { level: 1, name: "Station Summary" })).toBeTruthy();
    expect(screen.getByText(/Trusted production view for one station and time window/i)).toBeTruthy();
    expect(screen.getByText("Loading station summary.")).toBeTruthy();
    expect(screen.getByText(/Prior station values are hidden/i)).toBeTruthy();
    expect(screen.queryByLabelText("Trusted Quality route summary")).toBeNull();
    expect(screen.queryByLabelText("Trusted Process Metrics route")).toBeNull();
  });

  it("rejects a partial query before resolving the origin or fetching either route", async () => {
    render(await StationSummaryPage({ searchParams: { line_id: "LINE_001", station_id: "WS01" } }));

    expect(screen.getByText("INVALID_QUERY")).toBeTruthy();
    expect(fetchStationSummary).not.toHaveBeenCalled();
    expect(resolveTrustedAcceptedEventsApiOrigin).not.toHaveBeenCalled();
  });

  it("presents an unconfigured trusted API as a fail-closed error before fetching", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({
      ok: false,
      code: "ORIGIN_MISSING",
      message: "Accepted events service is not configured.",
    });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_001",
          station_id: "WS01",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    const alert = screen.getByRole("alert");
    expect(alert.classList.contains("state-error")).toBe(true);
    expect(screen.getByRole("heading", { level: 2, name: "Data source not configured" })).toBeTruthy();
    expect(screen.getByText(/trusted API is not configured/i)).toBeTruthy();
    expect(screen.getByText(/No fallback or fabricated production values are shown/i)).toBeTruthy();
    expect(screen.queryByText("EMPTY")).toBeNull();
    expect(screen.queryByLabelText("Trusted Quality route summary")).toBeNull();
    expect(screen.queryByLabelText("Trusted Process Metrics route")).toBeNull();
    expect(resolveTrustedAcceptedEventsApiOrigin).toHaveBeenCalledTimes(1);
    expect(fetchTrustedScopeCatalog).not.toHaveBeenCalled();
    expect(fetchStationSummary).not.toHaveBeenCalled();
  });

  it("loads only the trusted catalog on an empty URL and renders idle without production requests", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });

    render(await StationSummaryPage({ searchParams: {} }));

    expect(screen.getByRole("status").textContent).toContain("Select scope and apply");
    expect((screen.getByLabelText("Line") as HTMLSelectElement).value).toBe("LINE_001");
    expect((screen.getByLabelText("Station / WS") as HTMLSelectElement).value).toBe("WS01");
    expect(fetchTrustedScopeCatalog).toHaveBeenCalledTimes(1);
    expect(fetchStationSummary).not.toHaveBeenCalled();
  });

  it("reports catalog failure without URL option injection or production requests", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: false, kind: "unavailable", message: "Scope catalog unavailable" });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_UNKNOWN",
          station_id: "WS_UNKNOWN",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByRole("alert").textContent).toContain("Scope catalog unavailable");
    expect(screen.queryByText("LINE_UNKNOWN")).toBeNull();
    expect(screen.queryByText("WS_UNKNOWN")).toBeNull();
    expect(fetchStationSummary).not.toHaveBeenCalled();
  });

  it("rejects unknown URL scope after catalog validation and before trusted data routes", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_UNKNOWN",
          station_id: "WS_UNKNOWN",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByText("INVALID_QUERY")).toBeTruthy();
    expect(screen.queryByText("LINE_UNKNOWN")).toBeNull();
    expect(screen.queryByText("WS_UNKNOWN")).toBeNull();
    expect((screen.getByLabelText("Line") as HTMLSelectElement).value).toBe("LINE_001");
    expect(fetchStationSummary).not.toHaveBeenCalled();
  });

  it("validates catalog membership before continuing to the existing trusted summary routes", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchStationSummary).mockResolvedValue({
      ok: true,
      quality: { ok: false, kind: "unavailable", message: "Quality source unavailable." },
      processMetrics: { ok: false, kind: "unavailable", message: "Process Metrics source unavailable." },
    });
    const query = {
      lineId: "LINE_001",
      stationId: "WS01",
      startTime: "2026-07-05T00:00:00+08:00",
      endTime: "2026-07-05T08:00:00+08:00",
    };

    render(await StationSummaryPage({ searchParams: { line_id: query.lineId, station_id: query.stationId, start_time: query.startTime, end_time: query.endTime } }));

    expect(fetchStationSummary).toHaveBeenCalledTimes(1);
    expect(fetchStationSummary).toHaveBeenCalledWith(query, "https://api.example.test");
  });
});
