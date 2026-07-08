import { cleanup, render, screen } from "@testing-library/react";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import AcceptedEventsPage, { AcceptedEventsPageView } from "../page";
import { fetchAcceptedStationEvents } from "../../../lib/acceptedStationEvents/apiClient";

vi.mock("../../../lib/acceptedStationEvents/apiClient", () => ({
  fetchAcceptedStationEvents: vi.fn()
}));

afterEach(() => {
  cleanup();
});

describe("accepted events page", () => {
  it("renders invalid query, loading, empty, error, and unavailable as distinct states", () => {
    const states = ["invalid-query", "loading", "empty", "error", "unavailable"] as const;

    for (const state of states) {
      const { unmount } = render(<AcceptedEventsPageView state={{ kind: state, message: state }} />);
      expect(screen.getAllByText(state).length).toBeGreaterThan(0);
      unmount();
    }
  });

  it("does not render prior data as fresh production truth during loading or error", () => {
    render(
      <AcceptedEventsPageView
        state={{
          kind: "loading",
          message: "loading",
          priorDataNotice: "Prior accepted facts are hidden while this request is loading."
        }}
      />
    );

    expect(screen.getByText(/hidden while this request is loading/i)).toBeTruthy();
    expect(screen.queryByRole("table")).toBeNull();
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
