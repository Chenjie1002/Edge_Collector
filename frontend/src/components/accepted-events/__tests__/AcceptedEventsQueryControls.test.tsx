import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AcceptedEventsQueryControls } from "../AcceptedEventsQueryControls";

describe("AcceptedEventsQueryControls", () => {
  it("submits only bounded query fields and clears cursor on scope change", () => {
    const onSubmit = vi.fn();
    render(
      <AcceptedEventsQueryControls
        query={{
          lineId: "LINE_001",
          startTime: "2026-07-05T00:00:00Z",
          endTime: "2026-07-05T08:00:00Z",
          limit: 50,
          cursor: "opaque"
        }}
        onSubmit={onSubmit}
      />
    );

    fireEvent.change(screen.getByLabelText("Line ID"), { target: { value: "LINE_002" } });
    fireEvent.click(screen.getByRole("button", { name: "Apply query" }));

    expect(onSubmit).toHaveBeenCalledWith({
      lineId: "LINE_002",
      startTime: "2026-07-05T00:00:00Z",
      endTime: "2026-07-05T08:00:00Z",
      limit: 50
    });
  });
});
