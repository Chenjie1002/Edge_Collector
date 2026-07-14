import { cleanup, render, screen } from "@testing-library/react";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import AcceptedEventsPage, { AcceptedEventsPageView } from "../page";
import { fetchAcceptedStationEvents } from "../../../lib/acceptedStationEvents/apiClient";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../../lib/acceptedStationEvents/apiOrigin";
import type { AcceptedStationEventsEnvelope } from "../../../lib/acceptedStationEvents/schema";
import { toAcceptedEventsViewModel } from "../../../lib/acceptedStationEvents/viewModel";

vi.mock("../../../lib/acceptedStationEvents/apiClient", () => ({
  fetchAcceptedStationEvents: vi.fn()
}));

vi.mock("../../../lib/acceptedStationEvents/apiOrigin", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../../../lib/acceptedStationEvents/apiOrigin")>();
  const success = actual.resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: "https://accepted-api.example",
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production"
  });
  return { ...actual, resolveTrustedAcceptedEventsApiOrigin: vi.fn(() => success) };
});

afterEach(() => {
  vi.restoreAllMocks();
  cleanup();
  vi.mocked(fetchAcceptedStationEvents).mockReset();
  vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReset();
});

const readyQuery = {
  lineId: "LINE_001",
  startTime: "2026-07-05T00:00:00Z",
  endTime: "2026-07-05T08:00:00Z",
  limit: 50
};

const staleProductionValues = [
  "sha256:stale-fact",
  "DMC-STALE-001",
  "PLC_001:WS01:stale",
  "stale-nok-origin",
  "stale-config-version"
];

async function trustedResolution(origin = "https://accepted-api.example", profile = "production") {
  const actual = await vi.importActual<typeof import("../../../lib/acceptedStationEvents/apiOrigin")>(
    "../../../lib/acceptedStationEvents/apiOrigin"
  );
  const resolution = actual.resolveTrustedAcceptedEventsApiOrigin({
    EDGE_MES_DASHBOARD_API_ORIGIN: origin,
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: profile
  });
  if (!resolution.ok) throw new Error("test resolver fixture must succeed");
  return resolution;
}

function readyEnvelope(profileId: string): AcceptedStationEventsEnvelope {
  return {
    items: [
      {
        line_id: "LINE_001",
        plc_id: "PLC_001",
        station_id: "WS01",
        station_type: "ASSEMBLY",
        profile_id: profileId,
        config_hash: "sha256:transport-profile-config",
        config_version: "transport-profile-config-version",
        event_type: "station_result",
        production_result: "ok",
        unit_id: "UNIT-TRANSPORT-001",
        dmc: "DMC-TRANSPORT-001",
        cycle_counter: 302,
        source_event_id: "PLC_001:WS01:transport-profile",
        event_ts: "2026-07-05T11:00:00Z",
        accepted_at: "2026-07-05T11:00:01Z",
        fact_key: "sha256:transport-profile-fact",
        content_fingerprint: "sha256:transport-profile-content",
        nok_code: null,
        nok_origin: null,
        nok_detail_code: null,
        nok_detail_source_event_id: null,
        nok_detail_evidence_fact_key: null
      }
    ],
    page: { next_cursor: null, limit: 50 }
  };
}

function staleReadyState() {
  return {
    kind: "ready" as const,
    query: readyQuery,
    viewModel: toAcceptedEventsViewModel({
      items: [
        {
          line_id: "LINE_001",
          plc_id: "PLC_001",
          station_id: "WS01",
          station_type: "ASSEMBLY",
          profile_id: "normal",
          config_hash: "sha256:stale-config",
          config_version: "stale-config-version",
          event_type: "station_result",
          production_result: "nok",
          unit_id: "UNIT-STALE-001",
          dmc: "DMC-STALE-001",
          cycle_counter: 301,
          source_event_id: "PLC_001:WS01:stale",
          event_ts: "2026-07-05T10:00:00Z",
          accepted_at: "2026-07-05T10:00:01Z",
          fact_key: "sha256:stale-fact",
          content_fingerprint: "sha256:stale-content",
          nok_code: 100,
          nok_origin: "stale-nok-origin",
          nok_detail_code: null,
          nok_detail_source_event_id: null,
          nok_detail_evidence_fact_key: null
        }
      ],
      page: { next_cursor: null, limit: 50 }
    })
  };
}

function detailCompanionReadyState() {
  return {
    kind: "ready" as const,
    query: readyQuery,
    viewModel: toAcceptedEventsViewModel({
      items: [
        {
          line_id: "LINE_001",
          plc_id: "PLC_001",
          station_id: "WS02",
          station_type: "ASSEMBLY",
          profile_id: "normal",
          config_hash: "sha256:detail-config",
          config_version: "detail-config-version",
          event_type: "station_nok",
          production_result: null,
          unit_id: null,
          dmc: "",
          cycle_counter: 401,
          source_event_id: "PLC_001:WS02:401-detail",
          event_ts: "2026-07-05T12:00:00Z",
          accepted_at: "2026-07-05T12:00:01Z",
          fact_key: "sha256:first-detail-fact",
          content_fingerprint: "sha256:first-detail-content",
          nok_code: 200,
          nok_origin: "station_nok",
          nok_detail_code: 201,
          nok_detail_source_event_id: "PLC_001:WS02:401",
          nok_detail_evidence_fact_key: "sha256:upstream-outcome-fact"
        },
        {
          line_id: "LINE_001",
          plc_id: "PLC_001",
          station_id: "WS02",
          station_type: "ASSEMBLY",
          profile_id: "normal",
          config_hash: "sha256:detail-config",
          config_version: "detail-config-version",
          event_type: "station_result",
          production_result: "nok",
          unit_id: "U-SECOND",
          dmc: "DMC-SECOND",
          cycle_counter: 402,
          source_event_id: "PLC_001:WS02:402",
          event_ts: "2026-07-05T12:00:02Z",
          accepted_at: "2026-07-05T12:00:03Z",
          fact_key: "sha256:second-outcome-fact",
          content_fingerprint: "sha256:second-outcome-content",
          nok_code: 202,
          nok_origin: "station_result",
          nok_detail_code: null,
          nok_detail_source_event_id: null,
          nok_detail_evidence_fact_key: null
        }
      ],
      page: { next_cursor: null, limit: 50 }
    })
  };
}

function emptyReadyState() {
  return {
    kind: "ready" as const,
    query: readyQuery,
    viewModel: toAcceptedEventsViewModel({ items: [], page: { next_cursor: null, limit: 50 } })
  };
}

function expectPriorProductionTruthToBeRemoved() {
  expect(screen.queryByRole("table")).toBeNull();
  expect(screen.queryByLabelText("Accepted events page summary")).toBeNull();
  expect(screen.queryByLabelText("Accepted NOK detail evidence")).toBeNull();
  expect(screen.queryByLabelText("Accepted fact trace references")).toBeNull();

  for (const value of staleProductionValues) {
    expect(screen.queryByText(value)).toBeNull();
  }
}

describe("accepted events page", () => {
  it("renders invalid query, loading, empty, error, and unavailable as distinct states", () => {
    const states = ["invalid-query", "loading", "empty", "error", "unavailable"] as const;

    for (const state of states) {
      const { unmount } = render(<AcceptedEventsPageView state={{ kind: state, message: state }} />);
      expect(screen.getAllByText(state).length).toBeGreaterThan(0);
      unmount();
    }
  });

  it("clears prior production truth when ready rerenders to loading", () => {
    const { rerender } = render(<AcceptedEventsPageView state={staleReadyState()} />);

    rerender(
      <AcceptedEventsPageView
        state={{
          kind: "loading",
          message: "loading",
          priorDataNotice: "Prior accepted facts are hidden while this request is loading."
        }}
      />
    );

    expect(screen.getByText(/hidden while this request is loading/i)).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it("clears prior production truth when ready rerenders to error", () => {
    const { rerender } = render(<AcceptedEventsPageView state={staleReadyState()} />);

    rerender(<AcceptedEventsPageView state={{ kind: "error", message: "distinct stale-data error" }} />);

    expect(screen.getByText("error")).toBeTruthy();
    expect(screen.getByText("distinct stale-data error")).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it("clears prior production truth when ready rerenders to unavailable", () => {
    const { rerender } = render(<AcceptedEventsPageView state={staleReadyState()} />);

    rerender(<AcceptedEventsPageView state={{ kind: "unavailable", message: "distinct unavailable state" }} />);

    expect(screen.getByText("unavailable")).toBeTruthy();
    expect(screen.getByText("distinct unavailable state")).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it("clears prior production truth when ready rerenders to invalid-query", () => {
    const { rerender } = render(<AcceptedEventsPageView state={staleReadyState()} />);

    rerender(<AcceptedEventsPageView state={{ kind: "invalid-query", message: "distinct invalid query state" }} />);

    expect(screen.getByText("invalid-query")).toBeTruthy();
    expect(screen.getByText("distinct invalid query state")).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it("clears selected truth and renders current zero-count summary when ready becomes empty", () => {
    const { rerender } = render(<AcceptedEventsPageView state={staleReadyState()} />);

    rerender(<AcceptedEventsPageView state={emptyReadyState()} />);

    expect(screen.getByText("No accepted facts returned for the current bounded scope.")).toBeTruthy();
    const summary = screen.getByLabelText("Accepted events page summary");
    expect(summary.textContent).toContain("Current page only");
    expect(summary.textContent).toContain("0");
    expect(summary.textContent).toContain("Production result mix (station_result only)none");
    expect(summary.textContent).toContain("Station mixnone");
    expect(summary.textContent).not.toMatch(/nok: 1|WS01: 1/);
    expect(screen.queryByRole("table")).toBeNull();
    expect(screen.queryByLabelText("Accepted NOK detail evidence")).toBeNull();
    expect(screen.queryByLabelText("Accepted fact trace references")).toBeNull();
    for (const value of staleProductionValues) {
      expect(screen.queryByText(value)).toBeNull();
    }
  });

  it("keeps the response-owned profile_id in ready trace data without transport-profile UI leakage", () => {
    render(<AcceptedEventsPageView state={staleReadyState()} />);

    const trace = screen.getByLabelText("Accepted fact trace references");
    expect(trace.textContent).toContain("normal / stale-config-version / sha256:stale-config");
    expect(trace.textContent).not.toContain("production");
    expect(trace.textContent).not.toContain("container");
    expect(trace.textContent).not.toContain("local");
  });

  it("binds table selection, NOK detail, and trace to the first response fact while result mix counts station_result only", () => {
    const { container } = render(<AcceptedEventsPageView state={detailCompanionReadyState()} />);

    const rows = container.querySelectorAll("tbody tr");
    expect(rows).toHaveLength(2);
    expect(rows[0]?.className).toBe("is-selected");
    expect(rows[1]?.className).toBe("");

    const evidence = screen.getByLabelText("Accepted NOK detail evidence");
    const trace = screen.getByLabelText("Accepted fact trace references");
    const summary = screen.getByLabelText("Accepted events page summary");

    expect(screen.getAllByText("Not applicable — NOK detail companion").length).toBeGreaterThanOrEqual(1);
    expect(evidence.textContent).toContain("station_nok detail companion");
    expect(evidence.textContent).toContain("Fact reference sha256:first-detail-fact");
    expect(evidence.textContent).toContain("sha256:upstream-outcome-fact");
    expect(trace.textContent).toContain("sha256:first-detail-fact");
    expect(trace.textContent).not.toContain("sha256:second-outcome-fact");
    expect(summary.textContent).toContain("2accepted facts");
    expect(summary.textContent).toContain("Production result mix (station_result only)nok: 1");
    expect(summary.textContent).not.toContain("unknown");
  });

  it("renders a client error as a non-ready page without production surfaces", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue(await trustedResolution());
    vi.mocked(fetchAcceptedStationEvents).mockResolvedValue({
      ok: false,
      kind: "error",
      message: "distinct client error message"
    });

    render(await AcceptedEventsPage({ searchParams: { line_id: "LINE_001", start_time: readyQuery.startTime, end_time: readyQuery.endTime } }));

    expect(screen.getByText("error")).toBeTruthy();
    expect(screen.getByText("distinct client error message")).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it("renders source unavailable as a non-ready page without production surfaces", async () => {
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue(await trustedResolution());
    vi.mocked(fetchAcceptedStationEvents).mockResolvedValue({
      ok: false,
      kind: "unavailable",
      message: "distinct source unavailable message"
    });

    render(await AcceptedEventsPage({ searchParams: { line_id: "LINE_001", start_time: readyQuery.startTime, end_time: readyQuery.endTime } }));

    expect(screen.getByText("unavailable")).toBeTruthy();
    expect(screen.getByText("distinct source unavailable message")).toBeTruthy();
    expectPriorProductionTruthToBeRemoved();
  });

  it.each([
    ["line_id", { start_time: "2026-07-05T00:00:00Z", end_time: "2026-07-05T08:00:00Z" }],
    ["start_time", { line_id: "LINE_001", end_time: "2026-07-05T08:00:00Z" }],
    ["end_time", { line_id: "LINE_001", start_time: "2026-07-05T00:00:00Z" }]
  ])("renders invalid query before request when %s is missing", async (_field, searchParams) => {
    const fetchMock = vi.mocked(fetchAcceptedStationEvents);
    const resolverMock = vi.mocked(resolveTrustedAcceptedEventsApiOrigin);
    fetchMock.mockClear();
    resolverMock.mockClear();

    render(await AcceptedEventsPage({ searchParams }));

    expect(screen.getByText("invalid-query")).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(resolverMock).not.toHaveBeenCalled();
  });

  it("fails closed for invalid URL limit without fetching, stale rows, or cursor decoding", async () => {
    const fetchMock = vi.mocked(fetchAcceptedStationEvents);
    const resolverMock = vi.mocked(resolveTrustedAcceptedEventsApiOrigin);
    fetchMock.mockClear();
    resolverMock.mockClear();

    render(
      await AcceptedEventsPage({
        searchParams: {
          line_id: "LINE_001",
          start_time: "2026-07-05T00:00:00Z",
          end_time: "2026-07-05T08:00:00Z",
          limit: "NaN",
          cursor: "opaque.api.owned.cursor"
        }
      })
    );

    expect(screen.getByText("invalid-query")).toBeTruthy();
    expect(screen.getByText(/limit must be between 1 and 500/i)).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(resolverMock).not.toHaveBeenCalled();
    expect(screen.queryByRole("table")).toBeNull();
    expect(screen.queryByText(/opaque\.api\.owned\.cursor|decoded|mutated|constructed/i)).toBeNull();
  });

  it("renders a configuration failure as a safe generic error without requesting production truth", async () => {
    const rawOrigin = "https://unsafe.example/secret-path";
    const rawProfile = "unsafe-profile";
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue({
      ok: false,
      code: "ORIGIN_NON_CANONICAL",
      message: "Accepted events service is not configured."
    });

    render(await AcceptedEventsPage({ searchParams: { line_id: "LINE_001", start_time: readyQuery.startTime, end_time: readyQuery.endTime } }));

    expect(screen.getByText("error")).toBeTruthy();
    expect(screen.getByText("Accepted events service is not configured.")).toBeTruthy();
    expect(screen.queryByText("ORIGIN_NON_CANONICAL")).toBeNull();
    expect(screen.queryByText(rawOrigin)).toBeNull();
    expect(screen.queryByText(rawProfile)).toBeNull();
    expect(vi.mocked(fetchAcceptedStationEvents)).not.toHaveBeenCalled();
    expect(fetchSpy).not.toHaveBeenCalled();
    expectPriorProductionTruthToBeRemoved();
  });

  it("passes the resolver-issued brand exactly once to the client after valid query validation", async () => {
    const resolution = await trustedResolution();
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue(resolution);
    vi.mocked(fetchAcceptedStationEvents).mockResolvedValue({
      ok: false,
      kind: "error",
      message: "client fixture result"
    });

    render(await AcceptedEventsPage({ searchParams: { line_id: "LINE_001", start_time: readyQuery.startTime, end_time: readyQuery.endTime } }));

    expect(resolveTrustedAcceptedEventsApiOrigin).toHaveBeenCalledTimes(1);
    expect(fetchAcceptedStationEvents).toHaveBeenCalledTimes(1);
    expect(vi.mocked(fetchAcceptedStationEvents).mock.calls[0]?.[1]).toBe(resolution.origin);
  });

  it.each([
    ["local", "http://127.0.0.1:8000"],
    ["container", "http://api:8000"],
    ["production", "https://accepted-api.example"]
  ] as const)("keeps response-owned profile_id isolated from the %s transport profile", async (transportProfile, origin) => {
    const responseProfileId = "accepted-fact-profile-42";
    const resolution = await trustedResolution(origin, transportProfile);
    vi.mocked(resolveTrustedAcceptedEventsApiOrigin).mockReturnValue(resolution);
    vi.mocked(fetchAcceptedStationEvents).mockResolvedValue({ ok: true, envelope: readyEnvelope(responseProfileId) });

    render(await AcceptedEventsPage({ searchParams: { line_id: "LINE_001", start_time: readyQuery.startTime, end_time: readyQuery.endTime } }));

    expect(resolveTrustedAcceptedEventsApiOrigin).toHaveBeenCalledTimes(1);
    expect(fetchAcceptedStationEvents).toHaveBeenCalledTimes(1);
    expect(vi.mocked(fetchAcceptedStationEvents).mock.calls[0]).toHaveLength(2);
    expect(vi.mocked(fetchAcceptedStationEvents).mock.calls[0]?.[0]).toEqual(readyQuery);
    expect(vi.mocked(fetchAcceptedStationEvents).mock.calls[0]?.[1]).toBe(resolution.origin);

    expect(screen.getByRole("table")).toBeTruthy();
    expect(screen.getByLabelText("Accepted events page summary").textContent).toContain("1");
    const trace = screen.getByLabelText("Accepted fact trace references");
    expect(trace.textContent).toContain(responseProfileId);
    expect(trace.textContent).not.toContain(transportProfile);
  });

  it("does not import forbidden backend, runtime, deploy, or Grafana surfaces", () => {
    const root = join(process.cwd(), "src");
    const files: string[] = [];
    const visit = (directory: string) => {
      for (const entry of readdirSync(directory)) {
        const path = join(directory, entry);
        if (statSync(path).isDirectory()) visit(path);
        else if (/\.(ts|tsx)$/.test(path) && !path.includes(`${join("src", "app", "accepted-events", "__tests__")}`)) {
          files.push(path);
        }
      }
    };

    visit(root);

    for (const file of files) {
      const source = readFileSync(file, "utf8");
      expect(source).not.toMatch(/api\/app\/|accepted_station_events|app\/db|storage\.py|docker|grafana/i);
    }
  });

  it("exports the page component", () => {
    expect(AcceptedEventsPage).toBeTypeOf("function");
  });
});
