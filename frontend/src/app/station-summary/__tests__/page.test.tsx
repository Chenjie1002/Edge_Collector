import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import StationSummaryPage, { StationSummaryPageView } from "../page";
import { fetchStationSummary } from "../../../lib/stationSummary/apiClient";
import { fetchLineSummary } from "../../../lib/stationSummary/lineSummaryApi";
import type { LineSummary } from "../../../lib/stationSummary/lineSummarySchema";
import {
  resolveTrustedAcceptedEventsApiOrigin,
  type TrustedAcceptedEventsApiOrigin,
} from "../../../lib/acceptedStationEvents/apiOrigin";
import { fetchTrustedScopeCatalog } from "../../../lib/stationSummary/scopeCatalog";

vi.mock("../../../lib/stationSummary/apiClient", () => ({
  fetchStationSummary: vi.fn(),
}));

vi.mock("../../../lib/stationSummary/lineSummaryApi", () => ({
  fetchLineSummary: vi.fn(),
}));

vi.mock("../../../lib/stationSummary/scopeCatalog", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../../../lib/stationSummary/scopeCatalog")>();
  return { ...actual, fetchTrustedScopeCatalog: vi.fn() };
});

vi.mock("../../../lib/acceptedStationEvents/apiOrigin", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../../../lib/acceptedStationEvents/apiOrigin")>();
  return { ...actual, resolveTrustedAcceptedEventsApiOrigin: vi.fn() };
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  vi.useRealTimers();
});

const catalog = {
  contractVersion: "production-scope-options/v1",
  timezone: "Asia/Shanghai",
  utcOffset: "+08:00",
  lines: [
    {
      lineId: "LINE_001",
      name: "Demo Assembly Line Runtime",
      stations: [
        { stationId: "WS01", name: "Screw Station", stationOrder: 1 },
        { stationId: "WS02", name: "EOL Test Station", stationOrder: 2 },
        { stationId: "WS03", name: "Pack Station", stationOrder: 3 },
      ],
    },
  ],
} as const;

const trustedTestApiOrigin: TrustedAcceptedEventsApiOrigin = "https://api.example.test" as TrustedAcceptedEventsApiOrigin;

const lineSummary: LineSummary = {
  contractVersion: "production-line-summary/v1",
  scope: {
    lineId: "LINE_001",
    startTime: "2026-07-05T00:00:00Z",
    endTime: "2026-07-05T08:00:00Z",
    cohortBasis: "terminal_completed",
  },
  topology: { entryStationId: "WS01", terminalStationId: "WS03", stations: ["WS01", "WS02", "WS03"] },
  cohort: { unitCount: 3, reconciliationStatus: "PASS", errors: [] },
  stations: [
    { stationId: "WS01", total: 3, ok: 2, nok: 1, newNok: 1, skipped: 0, processed: 3, reconciliationStatus: "PASS", evidenceCount: 3, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
    { stationId: "WS02", total: 3, ok: 2, nok: 1, newNok: 0, skipped: 1, processed: 2, reconciliationStatus: "PASS", evidenceCount: 3, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
    { stationId: "WS03", total: 3, ok: 2, nok: 1, newNok: 0, skipped: 1, processed: 2, reconciliationStatus: "PASS", evidenceCount: 3, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
  ],
};

describe("station summary page", () => {
  it("defaults to a live rolling dashboard for the trusted default line", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-08-16T08:00:00Z"));
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });

    render(await StationSummaryPage({ searchParams: {} }));

    expect(fetchLineSummary).toHaveBeenCalledWith(
      {
        lineId: "LINE_001",
        mode: "LIVE",
        startTime: "2026-08-16T08:00:00+08:00",
        endTime: "2026-08-16T16:00:00+08:00",
      },
      trustedTestApiOrigin,
    );
    expect(screen.getByText("LIVE · Rolling 8h · refresh 10s")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Line Summary" }).getAttribute("href")).toContain("mode=LIVE");
    expect(screen.getByRole("link", { name: "Line Summary" }).getAttribute("href")).not.toContain("start_time");
  });

  it("recomputes the LIVE rolling window when the dashboard is refreshed", async () => {
    vi.useFakeTimers();
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });

    vi.setSystemTime(new Date("2026-08-16T08:00:00Z"));
    render(await StationSummaryPage({ searchParams: { line_id: "LINE_001", mode: "LIVE" } }));
    expect(fetchLineSummary).toHaveBeenLastCalledWith(
      {
        lineId: "LINE_001",
        mode: "LIVE",
        startTime: "2026-08-16T08:00:00+08:00",
        endTime: "2026-08-16T16:00:00+08:00",
      },
      trustedTestApiOrigin,
    );

    vi.mocked(fetchLineSummary).mockClear();
    vi.setSystemTime(new Date("2026-08-16T08:10:00Z"));
    render(await StationSummaryPage({ searchParams: { line_id: "LINE_001", mode: "LIVE" } }));
    expect(fetchLineSummary).toHaveBeenLastCalledWith(
      {
        lineId: "LINE_001",
        mode: "LIVE",
        startTime: "2026-08-16T08:10:00+08:00",
        endTime: "2026-08-16T16:10:00+08:00",
      },
      trustedTestApiOrigin,
    );
  });

  it("marks an explicitly submitted start and end as a fixed window", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_001",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByText("FIXED WINDOW")).toBeTruthy();
    expect(screen.queryByText("LIVE · Rolling 8h · refresh 10s")).toBeNull();
    expect(screen.getByRole("link", { name: "Line Summary" }).getAttribute("href")).toContain("mode=FIXED");
  });

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

    expect(screen.getByRole("main").classList.contains("station-summary-shell")).toBe(true);
    expect(screen.getByRole("heading", { level: 1, name: "Station Summary" })).toBeTruthy();
    expect(screen.getByText(/whole selected line/i)).toBeTruthy();
    expect(screen.queryByLabelText("Trusted Process Metrics route")).toBeNull();
  });

  it("rejects a partial fixed query before resolving the origin or fetching production data", async () => {
    render(await StationSummaryPage({ searchParams: { line_id: "LINE_001", start_time: "2026-07-05T00:00:00+08:00" } }));

    expect(screen.getByText("INVALID_QUERY")).toBeTruthy();
    expect(fetchLineSummary).not.toHaveBeenCalled();
    expect(resolveTrustedAcceptedEventsApiOrigin).not.toHaveBeenCalled();
  });

  it("loads the trusted default line as a live whole-line dashboard on an empty URL", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });

    render(await StationSummaryPage({ searchParams: {} }));

    expect(screen.getByText("LIVE · Rolling 8h · refresh 10s")).toBeTruthy();
    expect((screen.getByLabelText("Line") as HTMLSelectElement).value).toBe("LINE_001");
    expect((screen.getByLabelText("Station detail (optional)") as HTMLSelectElement).value).toBe("");
    expect(fetchLineSummary).toHaveBeenCalledTimes(1);
    expect(fetchStationSummary).not.toHaveBeenCalled();
  });

  it("validates the selected line against the trusted catalog before the line-summary route", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_UNKNOWN",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByText("INVALID_QUERY")).toBeTruthy();
    expect(screen.queryByText("LINE_UNKNOWN")).toBeNull();
    expect(fetchLineSummary).not.toHaveBeenCalled();
  });

  it("renders the whole-line route in order without requiring a station detail query", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });
    const query = {
      lineId: "LINE_001",
      mode: "FIXED" as const,
      startTime: "2026-07-05T00:00:00+08:00",
      endTime: "2026-07-05T08:00:00+08:00",
    };

    render(await StationSummaryPage({ searchParams: { line_id: query.lineId, start_time: query.startTime, end_time: query.endTime } }));

    expect(fetchLineSummary).toHaveBeenCalledWith(query, trustedTestApiOrigin);
    expect(fetchStationSummary).not.toHaveBeenCalled();
    expect(screen.getByText("Completed cohort at terminal: 3")).toBeTruthy();
    expect(screen.getByText("Route conservation: PASS")).toBeTruthy();
    expect(screen.getAllByRole("rowheader").map((cell) => cell.textContent)).toEqual(["WS01", "WS02", "WS03"]);
    expect(screen.queryByText("Trusted Process Metrics fixed matrix")).toBeNull();
  });

  it("renders Line Summary and Station Detail as separate product tabs", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });

    render(
      await StationSummaryPage({
        searchParams: {
          line_id: "LINE_001",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByRole("link", { name: "Line Summary" }).getAttribute("aria-current")).toBe("page");
    expect(screen.getByRole("link", { name: "Station Detail" })).toBeTruthy();
    expect(screen.getByText("Completed cohort at terminal: 3")).toBeTruthy();
  });

  it("keeps whole-line metrics out of the Station Detail tab", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });
    vi.mocked(fetchStationSummary).mockResolvedValue({
      ok: true,
      quality: { ok: false, kind: "unavailable", message: "Quality source unavailable." },
      processMetrics: { ok: false, kind: "unavailable", message: "Process Metrics source unavailable." },
    });

    render(
      await StationSummaryPage({
        searchParams: {
          view: "station",
          line_id: "LINE_001",
          station_id: "WS02",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    expect(screen.getByRole("link", { name: "Station Detail" }).getAttribute("aria-current")).toBe("page");
    expect(screen.queryByText("Completed cohort at terminal: 3")).toBeNull();
    expect(screen.queryByText("Route conservation: PASS")).toBeNull();
    expect(screen.getByRole("heading", { level: 2, name: "WS02" })).toBeTruthy();
    expect(screen.getByText("Processed")).toBeTruthy();
    expect(screen.getByText("Skipped")).toBeTruthy();
    expect(screen.getByText("New NOK")).toBeTruthy();
  });

  it("keeps developer contract metadata behind a collapsed Data diagnostics disclosure", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({ ok: true, origin: trustedTestApiOrigin });
    vi.mocked(fetchTrustedScopeCatalog).mockResolvedValue({ ok: true, catalog });
    vi.mocked(fetchLineSummary).mockResolvedValue({ ok: true, summary: lineSummary });
    vi.mocked(fetchStationSummary).mockResolvedValue({
      ok: true,
      quality: { ok: false, kind: "unavailable", message: "Quality source unavailable." },
      processMetrics: { ok: false, kind: "unavailable", message: "Process Metrics source unavailable." },
    });

    render(
      await StationSummaryPage({
        searchParams: {
          view: "station",
          line_id: "LINE_001",
          station_id: "WS01",
          start_time: "2026-07-05T00:00:00+08:00",
          end_time: "2026-07-05T08:00:00+08:00",
        },
      }),
    );

    const diagnosticsSummary = screen.getByText("Data diagnostics");
    const diagnostics = diagnosticsSummary.closest("details");
    expect(diagnostics?.open).toBe(false);
    expect(screen.getByText("Bounded authority matrix")).toBeTruthy();
  });
});
