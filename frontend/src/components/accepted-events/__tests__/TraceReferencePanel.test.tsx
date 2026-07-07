import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TraceReferencePanel } from "../TraceReferencePanel";

describe("TraceReferencePanel", () => {
  it("renders only accepted fact identity and trace references", () => {
    render(
      <TraceReferencePanel
        reference={{
          unitId: "U-001",
          dmc: "DMC-001",
          cycleCounter: 301,
          sourceEventId: "PLC_001:WS01:301",
          eventTs: "2026-07-05T10:00:00Z",
          acceptedAt: "2026-07-05T10:00:01Z",
          factKey: "sha256:fact",
          contentFingerprint: "sha256:content",
          lineId: "LINE_001",
          plcId: "PLC_001",
          stationId: "WS01",
          profileId: "normal",
          configHash: "sha256:abc",
          configVersion: "2026.07.05.1"
        }}
      />
    );

    expect(screen.getByText("sha256:fact")).toBeTruthy();
    expect(screen.queryByText(/raw|debug|payload|work order|product/i)).toBeNull();
  });
});
