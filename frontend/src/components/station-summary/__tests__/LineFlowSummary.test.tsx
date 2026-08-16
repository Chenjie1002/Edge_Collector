import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { LineSummary } from "../../../lib/stationSummary/lineSummarySchema";
import { LineFlowSummary } from "../LineFlowSummary";

const summary: LineSummary = {
  contractVersion: "production-line-summary/v1",
  scope: {
    lineId: "LINE_001",
    startTime: "2026-08-16T10:00:00Z",
    endTime: "2026-08-16T11:00:00Z",
    cohortBasis: "terminal_completed",
  },
  topology: {
    entryStationId: "WS01",
    terminalStationId: "WS03",
    stations: ["WS01", "WS02", "WS03"],
  },
  cohort: {
    unitCount: 2,
    reconciliationStatus: "PASS",
    errors: [],
  },
  stations: [
    { stationId: "WS01", total: 2, ok: 1, nok: 1, newNok: 1, skipped: 0, processed: 2, reconciliationStatus: "PASS", evidenceCount: 2, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
    { stationId: "WS02", total: 2, ok: 1, nok: 1, newNok: 0, skipped: 1, processed: 1, reconciliationStatus: "PASS", evidenceCount: 2, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
    { stationId: "WS03", total: 2, ok: 1, nok: 1, newNok: 0, skipped: 1, processed: 1, reconciliationStatus: "PASS", evidenceCount: 2, missingUnitCount: 0, duplicateUnitCount: 0, invalidRecordCount: 0, resultCompatibility: "native_nok_process_status_split" },
  ],
};

describe("LineFlowSummary", () => {
  it("renders the terminal-completed cohort and every station in route order", () => {
    render(<LineFlowSummary summary={summary} />);

    expect(screen.getByText("Completed cohort at terminal: 2")).toBeTruthy();
    expect(screen.getByText("Route conservation: PASS")).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "Station" })).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "Total" })).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "OK" })).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "NOK" })).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "New NOK" })).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "Skipped" })).toBeTruthy();

    const rows = screen.getAllByRole("row");
    expect(rows).toHaveLength(4);
    expect(rows.slice(1).map((row) => within(row).getByRole("rowheader").textContent)).toEqual(["WS01", "WS02", "WS03"]);
    expect(screen.getByRole("table").textContent).not.toContain("Bypassed");
  });

  it("makes a failed route reconciliation explicit and human-readable", () => {
    render(
      <LineFlowSummary
        summary={{
          ...summary,
          cohort: {
            unitCount: 2,
            reconciliationStatus: "FAIL",
            errors: ["1 completed units are missing trusted WS02 station evidence"],
          },
          stations: summary.stations.map((station) => station.stationId === "WS02" ? { ...station, reconciliationStatus: "FAIL", missingUnitCount: 1 } : station),
        }}
      />,
    );

    expect(screen.getByText("Route conservation: FAIL")).toBeTruthy();
    expect(screen.getByRole("alert").textContent).toContain("Flow reconciliation failed");
    expect(screen.getByRole("alert").textContent).toContain("WS02 station evidence");
  });
});
