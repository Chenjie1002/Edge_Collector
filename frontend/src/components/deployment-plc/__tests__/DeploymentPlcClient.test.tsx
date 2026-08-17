import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { DeploymentPlcClient } from "../DeploymentPlcClient";

const debugStations = [
  {
    station_id: "WS01",
    db_number: 101,
    station_order: 1,
    read_start: 0,
    read_length: 344,
    confirmation_state: "PLANNED",
    signals: [
      { field_name: "cycle_counter", address: "DB101.DBD2", type: "dint", direction: "PLC_TO_EDGE", group: "header", confirmation_state: "PLANNED" },
      { field_name: "read_done", address: "DB101.DBX6.1", type: "bool", direction: "READ_WRITE", group: "header", confirmation_state: "CONFIRMED" }
    ]
  },
  {
    station_id: "WS02",
    db_number: 102,
    station_order: 2,
    read_start: 0,
    read_length: 344,
    confirmation_state: "PLANNED",
    signals: [
      { field_name: "cycle_counter", address: "DB102.DBD2", type: "dint", direction: "PLC_TO_EDGE", group: "header", confirmation_state: "PLANNED" },
      { field_name: "read_done", address: "DB102.DBX6.1", type: "bool", direction: "READ_WRITE", group: "header", confirmation_state: "PLANNED" }
    ]
  },
  {
    station_id: "WS03",
    db_number: 103,
    station_order: 3,
    read_start: 0,
    read_length: 344,
    confirmation_state: "PLANNED",
    signals: [
      { field_name: "cycle_counter", address: "DB103.DBD2", type: "dint", direction: "PLC_TO_EDGE", group: "header", confirmation_state: "PLANNED" },
      { field_name: "read_done", address: "DB103.DBX6.1", type: "bool", direction: "READ_WRITE", group: "header", confirmation_state: "PLANNED" }
    ]
  }
];

const active = {
  authority: {
    kind: "active_runtime_mapping",
    source: "config/mapping.yaml",
    config_version: "2026.06.26-slice-a",
    content_sha256: "sha256:active"
  },
  line_id: "LINE_001",
  line_name: "Demo Assembly Line Runtime",
  plc: {
    plc_id: "PLC_001",
    host: "s7-plc-sim",
    port: 1102,
    rack: 0,
    slot: 1,
    connection_timeout_ms: 3000,
    poll_interval_ms: 500
  },
  active_station_count: 3,
  active_station_ids: ["WS01", "WS02", "WS03"],
  debug_contract: {
    schema_version: "plc-debug-contract/v1",
    stations: debugStations,
    write_allowlist: {
      mode: "READ_DONE_ONLY",
      edge_to_plc: [
        { station_id: "WS01", field_name: "read_done", address: "DB101.DBX6.1", type: "bool", direction: "EDGE_TO_PLC", confirmation_state: "CONFIRMED" },
        { station_id: "WS02", field_name: "read_done", address: "DB102.DBX6.1", type: "bool", direction: "EDGE_TO_PLC", confirmation_state: "PLANNED" },
        { station_id: "WS03", field_name: "read_done", address: "DB103.DBX6.1", type: "bool", direction: "EDGE_TO_PLC", confirmation_state: "PLANNED" }
      ],
      parameter_writes_enabled: false,
      machine_control_writes_enabled: false,
      safety_writes_enabled: false,
      arbitrary_db_writes_enabled: false
    }
  }
};

const lineOptions = [
  {
    file_name: "demo_3_station.yaml",
    line_id: "LINE_001",
    name: "Demo 3",
    station_count: 3,
    plc_count: 1,
    config_hash: "sha256:line3",
    capability: "CURRENTLY_SUPPORTED",
    capability_label: "CURRENTLY SUPPORTED",
    ready_to_activate: true,
    active: true
  },
  {
    file_name: "demo_10_station.yaml",
    line_id: "LINE_DEMO_10",
    name: "Demo 10",
    station_count: 10,
    plc_count: 1,
    config_hash: "sha256:line10",
    capability: "CONFIG_VALID_RUNTIME_NOT_YET_SUPPORTED",
    capability_label: "CONFIG VALID / RUNTIME NOT YET SUPPORTED",
    ready_to_activate: false,
    active: false
  },
  {
    file_name: "stress_20_station.yaml",
    line_id: "LINE_STRESS_20",
    name: "Stress 20",
    station_count: 20,
    plc_count: 2,
    config_hash: "sha256:line20",
    capability: "CONFIG_VALID_MULTI_PLC_RUNTIME_NOT_YET_SUPPORTED",
    capability_label: "CONFIG VALID / MULTI-PLC RUNTIME NOT YET SUPPORTED",
    ready_to_activate: false,
    active: false
  }
];

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("PLC deployment configuration page", () => {
  it("renders active config, candidate fields, honest line capability, and read-only safety state", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => {
        if (url.endsWith("/active")) return Promise.resolve(new Response(JSON.stringify(active), { status: 200 }));
        if (url.endsWith("/line-options")) return Promise.resolve(new Response(JSON.stringify({ items: lineOptions }), { status: 200 }));
        return Promise.resolve(new Response(JSON.stringify({}), { status: 200 }));
      })
    );

    render(<DeploymentPlcClient />);

    expect(await screen.findByRole("heading", { level: 1, name: "PLC Deployment Configuration" })).toBeTruthy();
    expect(screen.getByText("2026.06.26-slice-a")).toBeTruthy();
    expect((screen.getByLabelText("PLC host / IP") as HTMLInputElement).value).toBe("s7-plc-sim");
    expect((screen.getByLabelText("Port") as HTMLInputElement).value).toBe("1102");
    expect(screen.getAllByText(/CURRENTLY SUPPORTED/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/RUNTIME NOT YET SUPPORTED/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/MULTI-PLC RUNTIME NOT YET SUPPORTED/).length).toBeGreaterThan(0);
    expect(screen.getByRole("button", { name: /Test Connection · Read-only/i })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Apply|Restart/i })).toBeNull();
    expect(screen.getByRole("heading", { level: 2, name: "Active Debug Communication Contract" })).toBeTruthy();
    expect(screen.getAllByText("DB101.DBX6.1").length).toBeGreaterThan(0);
    expect(screen.getAllByText("DB101.DBD2").length).toBeGreaterThan(0);
    expect(screen.getAllByText("PLANNED").length).toBeGreaterThan(0);
    expect(screen.getAllByText("CONFIRMED").length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Read_Done only/i).length).toBeGreaterThan(0);
    expect((screen.getByLabelText("WS01 DB number") as HTMLInputElement).value).toBe("101");
  });

  it("shows saved candidate as not active and exposes retrieval", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/active")) return Promise.resolve(new Response(JSON.stringify(active), { status: 200 }));
      if (url.endsWith("/line-options")) return Promise.resolve(new Response(JSON.stringify({ items: lineOptions }), { status: 200 }));
      if (url.endsWith("/candidates")) {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              candidate_id: "candidate-001",
              created_at: "2026-08-16T01:00:00Z",
              status: "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION",
              candidate_hash: "sha256:candidate",
              active_mapping_hash: "sha256:active",
              validation_state: "VALID",
              candidate: active.plc,
              line: lineOptions[0],
              last_connection_test: null,
              retrieval_path: "/api/v2/deployment/plc/candidates/candidate-001"
            }),
            { status: 200 }
          )
        );
      }
      void init;
      return Promise.resolve(new Response(JSON.stringify({}), { status: 200 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<DeploymentPlcClient />);
    await screen.findByRole("heading", { level: 1, name: "PLC Deployment Configuration" });
    await waitFor(() => expect((screen.getByLabelText("PLC host / IP") as HTMLInputElement).value).toBe("s7-plc-sim"));

    fireEvent.change(screen.getByLabelText("WS01 DB number"), { target: { value: "109" } });

    screen.getByRole("button", { name: "Save candidate" }).click();

    expect(await screen.findByRole("heading", { level: 2, name: /NOT ACTIVE \/ REQUIRES CONTROLLED ACTIVATION/i })).toBeTruthy();
    expect(screen.getByRole("link", { name: /Export \/ retrieve candidate JSON/i }).getAttribute("href")).toBe(
      "/api/deployment/plc/candidates/candidate-001"
    );
    const saveCall = fetchMock.mock.calls.find(([url, init]) => url.endsWith("/candidates") && init?.method === "POST");
    expect(saveCall).toBeTruthy();
    const savedBody = JSON.parse(String(saveCall?.[1]?.body));
    expect(savedBody.stations[0].db_number).toBe(109);
    expect(savedBody.stations[0].signals.some((signal: { address: string }) => signal.address === "DB101.DBX6.1")).toBe(true);
    expect(savedBody.write_allowlist.mode).toBe("READ_DONE_ONLY");
  });

  it("renders field-level validation errors returned by the API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string, init?: RequestInit) => {
        if (url.endsWith("/active")) return Promise.resolve(new Response(JSON.stringify(active), { status: 200 }));
        if (url.endsWith("/line-options")) return Promise.resolve(new Response(JSON.stringify({ items: lineOptions }), { status: 200 }));
        if (url.endsWith("/validate") && init?.method === "POST") {
          return Promise.resolve(new Response(JSON.stringify({
            validation_state: "INVALID",
            ready_to_activate: false,
            active_mapping_hash: "sha256:active",
            errors: [{ field: "port", message: "port must be between 1 and 65535." }],
            warnings: []
          }), { status: 422 }));
        }
        return Promise.resolve(new Response(JSON.stringify({}), { status: 200 }));
      })
    );

    render(<DeploymentPlcClient />);
    await screen.findByRole("heading", { level: 1, name: "PLC Deployment Configuration" });
    screen.getByRole("button", { name: "Validate candidate" }).click();

    expect(await screen.findByText(/port must be between 1 and 65535/i)).toBeTruthy();
  });

  it("activates a saved candidate and makes the collector restart boundary explicit", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/active")) return Promise.resolve(new Response(JSON.stringify(active), { status: 200 }));
      if (url.endsWith("/line-options")) return Promise.resolve(new Response(JSON.stringify({ items: lineOptions }), { status: 200 }));
      if (url.endsWith("/candidates") && init?.method === "POST") {
        return Promise.resolve(new Response(JSON.stringify({
          candidate_id: "candidate-001",
          created_at: "2026-08-16T01:00:00Z",
          status: "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION",
          candidate_hash: "sha256:candidate",
          active_mapping_hash: "sha256:active",
          validation_state: "VALID",
          candidate: { ...active.plc, line_config: "demo_3_station.yaml" },
          line: lineOptions[0],
          last_connection_test: null,
          retrieval_path: "/api/v2/deployment/plc/candidates/candidate-001"
        }), { status: 200 }));
      }
      if (url.endsWith("/candidates/candidate-001/activate") && init?.method === "POST") {
        return Promise.resolve(new Response(JSON.stringify({
          activation_id: "activation-001",
          candidate_id: "candidate-001",
          previous_active_mapping_hash: "sha256:active",
          active_mapping_hash: "sha256:activated",
          changed_fields: ["connection_timeout_ms"],
          status: "ACTIVATED_RESTART_REQUIRED",
          fresh_connection_test: { status: "CONNECTED_AND_READABLE", read_only: true, writes_performed: false, operations: ["connect", "db_read", "disconnect"] },
          writes_performed: false,
          rollback_available: true
        }), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify({}), { status: 200 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<DeploymentPlcClient />);
    await screen.findByRole("heading", { level: 1, name: "PLC Deployment Configuration" });
    screen.getByRole("button", { name: "Save candidate" }).click();

    expect(await screen.findByRole("button", { name: /Activate Candidate/i })).toBeTruthy();
    screen.getByRole("button", { name: /Activate Candidate/i }).click();

    expect(await screen.findByText(/COLLECTOR_RESTART_REQUIRED/i)).toBeTruthy();
    expect(screen.getByText(/config mutation only; PLC writes remain disabled/i)).toBeTruthy();
  });
});
