import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { StationSummaryQueryControls } from "../StationSummaryQueryControls";

afterEach(() => {
  cleanup();
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
      ],
    },
    {
      lineId: "LINE_002",
      name: "Second Line",
      stations: [{ stationId: "WS10", name: "Pack Station", stationOrder: 1 }],
    },
  ],
} as const;

describe("StationSummaryQueryControls", () => {
  it("schedules a ten-second refresh for a LIVE query", () => {
    vi.useFakeTimers();
    const intervalSpy = vi.spyOn(window, "setInterval");

    render(
      <StationSummaryQueryControls
        catalog={catalog}
        query={{
          lineId: "LINE_001",
          stationId: undefined,
          startTime: "2026-07-05T00:00:00+08:00",
          endTime: "2026-07-05T08:00:00+08:00",
          mode: "LIVE",
        } as never}
      />,
    );

    expect(intervalSpy).toHaveBeenCalledWith(expect.any(Function), 10_000);
  });

  it("does not schedule automatic refresh for a FIXED query", () => {
    vi.useFakeTimers();
    const intervalSpy = vi.spyOn(window, "setInterval");

    render(
      <StationSummaryQueryControls
        catalog={catalog}
        query={{
          lineId: "LINE_001",
          stationId: undefined,
          startTime: "2026-07-05T00:00:00+08:00",
          endTime: "2026-07-05T08:00:00+08:00",
          mode: "FIXED",
        } as never}
      />,
    );

    expect(intervalSpy).not.toHaveBeenCalledWith(expect.any(Function), 10_000);
  });

  it("renders a whole-line query with optional station drill-down and plant-local datetime controls", () => {
    render(
      <StationSummaryQueryControls
        catalog={catalog}
        query={{
          lineId: "LINE_001",
          stationId: undefined,
          startTime: "2026-07-05T00:00:00+08:00",
          endTime: "2026-07-05T08:00:00+08:00",
        }}
      />,
    );

    const form = screen.getByRole("form", { name: "Station summary scope query" });
    expect(form.getAttribute("method")).toBe("get");
    expect(form.getAttribute("action")).toBe("/station-summary");
    expect(form.classList.contains("query-controls")).toBe(true);
    expect(form.classList.contains("station-summary-query-controls")).toBe(true);
    expect(screen.getByRole("heading", { level: 2, name: "Scope" })).toBeTruthy();

    const line = screen.getByLabelText("Line") as HTMLSelectElement;
    const station = screen.getByLabelText("Station detail (optional)") as HTMLSelectElement;
    const start = screen.getByLabelText("Start time") as HTMLInputElement;
    const end = screen.getByLabelText("End time") as HTMLInputElement;
    expect([line.name, station.name, start.name, end.name]).toEqual(["line_id", "station_id", "", ""]);
    expect([line.value, station.value, start.value, end.value]).toEqual([
      "LINE_001",
      "",
      "2026-07-05T00:00",
      "2026-07-05T08:00",
    ]);
    expect(Array.from(form.querySelectorAll("[name]"), (element) => element.getAttribute("name"))).toEqual([
      "line_id",
      "station_id",
      "mode",
      "view",
      "start_time",
      "end_time",
    ]);
    expect((form.querySelector('input[name="start_time"]') as HTMLInputElement).value).toBe("2026-07-05T00:00:00+08:00");
    expect((form.querySelector('input[name="end_time"]') as HTMLInputElement).value).toBe("2026-07-05T08:00:00+08:00");
    expect(start.type).toBe("datetime-local");
    expect(end.type).toBe("datetime-local");
    expect(screen.getByText("Plant time: Asia/Shanghai (UTC+08:00)")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Last 1h" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Last 8h" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Last 24h" })).toBeTruthy();

    const apply = screen.getByRole("button", { name: "Apply fixed window" }) as HTMLButtonElement;
    expect(apply.classList.contains("station-summary-scope-apply")).toBe(true);
    expect(apply.parentElement?.classList.contains("station-summary-scope-fields")).toBe(true);
    expect(apply.disabled).toBe(false);
  });

  it("keeps station drill-down optional when the line changes", () => {
    render(<StationSummaryQueryControls catalog={catalog} />);

    const line = screen.getByLabelText("Line") as HTMLSelectElement;
    const station = screen.getByLabelText("Station detail (optional)") as HTMLSelectElement;
    expect(line.value).toBe("LINE_001");
    expect(station.value).toBe("");

    fireEvent.change(line, { target: { value: "LINE_002" } });

    expect(station.value).toBe("");
    expect(Array.from(station.options).map((option) => option.value)).toEqual(["", "WS10"]);
  });

  it("disables trusted controls and Apply without a catalog", () => {
    render(<StationSummaryQueryControls />);

    expect((screen.getByLabelText("Line") as HTMLSelectElement).disabled).toBe(true);
    expect((screen.getByLabelText("Station detail (optional)") as HTMLSelectElement).disabled).toBe(true);
    expect((screen.getByLabelText("Start time") as HTMLInputElement).disabled).toBe(true);
    expect((screen.getByLabelText("End time") as HTMLInputElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "Refresh LIVE" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.queryByPlaceholderText("LINE_001")).toBeNull();
  });

  it("keeps Apply disabled for a non-positive or oversized local window", () => {
    render(<StationSummaryQueryControls catalog={catalog} />);
    fireEvent.change(screen.getByLabelText("Window mode"), { target: { value: "FIXED" } });
    const start = screen.getByLabelText("Start time");
    const end = screen.getByLabelText("End time");
    const apply = screen.getByRole("button", { name: "Apply fixed window" }) as HTMLButtonElement;

    fireEvent.change(start, { target: { value: "2026-07-01T08:00" } });
    fireEvent.change(end, { target: { value: "2026-07-01T08:00" } });
    expect(apply.disabled).toBe(true);

    fireEvent.change(end, { target: { value: "2026-08-01T08:01" } });
    expect(apply.disabled).toBe(true);
  });

  it("allows LIVE mode even after an invalid fixed-window edit", () => {
    render(<StationSummaryQueryControls catalog={catalog} />);

    fireEvent.change(screen.getByLabelText("Window mode"), { target: { value: "FIXED" } });
    fireEvent.change(screen.getByLabelText("Start time"), { target: { value: "2026-07-01T08:00" } });
    fireEvent.change(screen.getByLabelText("End time"), { target: { value: "2026-07-01T08:00" } });
    fireEvent.change(screen.getByLabelText("Window mode"), { target: { value: "LIVE" } });

    expect((screen.getByRole("button", { name: "Refresh LIVE" }) as HTMLButtonElement).disabled).toBe(false);
    expect((screen.getByLabelText("Start time") as HTMLInputElement).disabled).toBe(true);
  });
});
