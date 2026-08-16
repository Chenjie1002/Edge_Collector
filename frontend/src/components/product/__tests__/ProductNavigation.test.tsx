import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ProductNavigation } from "../ProductNavigation";

describe("ProductNavigation", () => {
  it("provides reversible links to every first-level product surface", () => {
    render(<ProductNavigation />);

    const navigation = screen.getByRole("navigation", { name: "Primary product navigation" });
    expect(screen.getByRole("link", { name: "Edge MES" }).getAttribute("href")).toBe("/");
    expect(screen.getByRole("link", { name: "Dashboard" }).getAttribute("href")).toBe("/");
    expect(screen.getByRole("link", { name: "Station Summary" }).getAttribute("href")).toBe("/station-summary");
    expect(screen.getByRole("link", { name: "Accepted Events" }).getAttribute("href")).toBe("/accepted-events");
    expect(screen.getByRole("link", { name: "PLC Deployment" }).getAttribute("href")).toBe("/deployment/plc");
    expect(screen.getByRole("link", { name: "Trace" }).getAttribute("href")).toBe("http://127.0.0.1:8000/trace");
    expect(screen.getByRole("link", { name: "V-PLC" }).getAttribute("href")).toBe("http://127.0.0.1:8200/vplc");
    expect(navigation.querySelectorAll("a")).toHaveLength(7);
  });
});
