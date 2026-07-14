import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AcceptedEventsTable } from "../AcceptedEventsTable";
import type { AcceptedEventRow } from "../../../lib/acceptedStationEvents/viewModel";

const row: AcceptedEventRow = {
  factKey: "sha256:fact",
  lineId: "LINE_001",
  stationId: "WS01",
  stationType: "ASSEMBLY",
  eventType: "station_result",
  productionResult: "ok",
  eventTs: { label: "Event time", value: "2026-07-05T10:00:00Z" },
  acceptedAt: { label: "Accepted fact timestamp", value: "2026-07-05T10:00:01Z" },
  unitId: "U-001",
  dmc: "DMC-001"
};

describe("AcceptedEventsTable", () => {
  it("renders accepted fact rows without forbidden freshness or fallback labels", () => {
    render(<AcceptedEventsTable rows={[row]} selectedFactKey={row.factKey} />);

    expect(screen.getByText("WS01")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "WS01" })).toBeNull();
    expect(screen.getAllByText("Accepted fact timestamp").length).toBeGreaterThan(0);
    expect(screen.queryByText(/freshness|ACK|read_done|work order|product/i)).toBeNull();
  });
});
