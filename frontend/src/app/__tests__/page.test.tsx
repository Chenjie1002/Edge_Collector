import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import DashboardHomePage from "../page";

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
});

describe("dashboard home page", () => {
  it("exposes the two existing read-only product surfaces without invented production values", () => {
    render(<DashboardHomePage />);

    expect(screen.getByRole("heading", { level: 1, name: "Production insight, from accepted facts." })).toBeTruthy();

    const stationSummary = screen.getByRole("link", { name: /Open station summary/i });
    const acceptedEvents = screen.getByRole("link", { name: /Open accepted events/i });
    expect(stationSummary.getAttribute("href")).toBe("/station-summary");
    expect(acceptedEvents.getAttribute("href")).toBe("/accepted-events");

    vi.stubEnv("EDGE_MES_DASHBOARD_TRACE_ORIGIN", "http://127.0.0.1:8000");
    vi.stubEnv("EDGE_MES_DASHBOARD_VPLC_ORIGIN", "http://127.0.0.1:8200");
    cleanup();
    render(<DashboardHomePage />);

    expect(screen.getByRole("link", { name: /Open Trace/i }).getAttribute("href")).toBe(
      "http://127.0.0.1:8000/trace"
    );
    expect(screen.getByRole("link", { name: /Open V-PLC Console/i }).getAttribute("href")).toBe(
      "http://127.0.0.1:8200/vplc"
    );
    expect(document.body.textContent).toMatch(/production traceability/i);
    expect(document.body.textContent).toMatch(/not field PLC deployment configuration/i);

    const policy = screen.getByLabelText("Dashboard data policy");
    expect(policy.textContent).toContain("Read-only");
    expect(policy.textContent).toContain("Trusted API surfaces");
    expect(policy.textContent).toContain("No fabricated fallback");
    expect(document.body.textContent).not.toMatch(/\b\d+(?:\.\d+)?%\b/);
  });
});
