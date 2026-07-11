import { cleanup, render, screen } from "@testing-library/react";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import AcceptedEventsPage, { AcceptedEventsPageView } from "../page";
import { fetchAcceptedStationEvents } from "../../../lib/acceptedStationEvents/apiClient";
import { toAcceptedEventsViewModel } from "../../../lib/acceptedStationEvents/viewModel";

vi.mock("../../../lib/acceptedStationEvents/apiClient", () => ({
  fetchAcceptedStationEvents: vi.fn()
}));

afterEach(() => {
  cleanup();
  vi.mocked(fetchAcceptedStationEvents).mockReset();
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
  "STALE_DETAIL",
  "stale-config-version"
];

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
          nok_code: "STALE_NOK",
          nok_origin: "accepted-fact",
          nok_detail_code: "STALE_DETAIL",
          nok_detail_source_event_id: "PLC_001:WS01:stale-detail",
          nok_detail_evidence_fact_key: "sha256:stale-detail-fact"
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
    expect(summary.textContent).toContain("Result mixnone");
    expect(summary.textContent).toContain("Station mixnone");
    expect(summary.textContent).not.toMatch(/nok: 1|WS01: 1/);
    expect(screen.queryByRole("table")).toBeNull();
    expect(screen.queryByLabelText("Accepted NOK detail evidence")).toBeNull();
    expect(screen.queryByLabelText("Accepted fact trace references")).toBeNull();
    for (const value of staleProductionValues) {
      expect(screen.queryByText(value)).toBeNull();
    }
  });

  it("renders a client error as a non-ready page without production surfaces", async () => {
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
    fetchMock.mockClear();

    render(await AcceptedEventsPage({ searchParams }));

    expect(screen.getByText("invalid-query")).toBeTruthy();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("fails closed for invalid URL limit without fetching, stale rows, or cursor decoding", async () => {
    const fetchMock = vi.mocked(fetchAcceptedStationEvents);
    fetchMock.mockClear();

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
    expect(screen.queryByRole("table")).toBeNull();
    expect(screen.queryByText(/opaque\.api\.owned\.cursor|decoded|mutated|constructed/i)).toBeNull();
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
