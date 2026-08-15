import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import DashboardHomePage from "../page";

afterEach(() => cleanup());

describe("dashboard home page", () => {
  it("exposes the two existing read-only product surfaces without invented production values", () => {
    render(<DashboardHomePage />);

    expect(screen.getByRole("heading", { level: 1, name: "Production insight, from accepted facts." })).toBeTruthy();

    const stationSummary = screen.getByRole("link", { name: /Open station summary/i });
    const acceptedEvents = screen.getByRole("link", { name: /Open accepted events/i });
    expect(stationSummary.getAttribute("href")).toBe("/station-summary");
    expect(acceptedEvents.getAttribute("href")).toBe("/accepted-events");

    const policy = screen.getByLabelText("Dashboard data policy");
    expect(policy.textContent).toContain("Read-only");
    expect(policy.textContent).toContain("Trusted API surfaces");
    expect(policy.textContent).toContain("No fabricated fallback");
    expect(document.body.textContent).not.toMatch(/\b\d+(?:\.\d+)?%\b/);
  });
});
