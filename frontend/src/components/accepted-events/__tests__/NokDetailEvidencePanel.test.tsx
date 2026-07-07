import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { NokDetailEvidencePanel } from "../NokDetailEvidencePanel";

describe("NokDetailEvidencePanel", () => {
  it("shows absent or unknown detail instead of synthetic diagnostic detail", () => {
    render(
      <NokDetailEvidencePanel
        evidence={{
          productionResult: "ok",
          nokCode: null,
          nokOrigin: null,
          nokDetailCode: null,
          nokDetailSourceEventId: null,
          nokDetailEvidenceFactKey: null,
          factKey: "sha256:fact",
          sourceEventId: "PLC_001:WS01:301"
        }}
      />
    );

    expect(screen.getByText(/absent \/ unknown/i)).toBeTruthy();
    expect(screen.queryByText(/adapter|raw|decoder|diagnostic/i)).toBeNull();
  });
});
