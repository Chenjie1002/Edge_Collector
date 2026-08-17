export type ConfirmationState = "PLANNED" | "CONFIRMED";

export type DebugSignal = {
  field_name: string;
  address: string;
  type: string;
  direction: "PLC_TO_EDGE" | "READ_WRITE" | "EDGE_TO_PLC";
  group?: "header" | "payload";
  unit?: string;
  description?: string;
  max_length?: number;
  required?: boolean;
  confirmation_state: ConfirmationState;
};

export type DebugStation = {
  station_id: string;
  db_number: number;
  station_order?: number;
  read_start: number;
  read_length: number;
  confirmation_state: ConfirmationState;
  signals: DebugSignal[];
};

export type DebugWriteAllowlist = {
  mode: "READ_DONE_ONLY";
  edge_to_plc: Array<{
    station_id: string;
    field_name: "read_done";
    address: string;
    type: string;
    direction: "EDGE_TO_PLC";
    confirmation_state: ConfirmationState;
  }>;
  parameter_writes_enabled: false;
  machine_control_writes_enabled: false;
  safety_writes_enabled: false;
  arbitrary_db_writes_enabled: false;
};

export type DebugContract = {
  schema_version?: "plc-debug-contract/v1";
  stations: DebugStation[];
  write_allowlist: DebugWriteAllowlist;
};

export type DeploymentCandidate = {
  host: string;
  port: number;
  rack: number;
  slot: number;
  connection_timeout_ms: number;
  poll_interval_ms: number;
  line_config: string;
  stations: DebugStation[];
  write_allowlist: DebugWriteAllowlist;
};

export type ActiveDeploymentConfig = {
  authority: {
    kind: "active_runtime_mapping";
    source: string;
    config_version: string;
    content_sha256: string;
  };
  line_id: string;
  line_name: string;
  plc: {
    plc_id: string;
    host: string;
    port: number;
    rack: number;
    slot: number;
    connection_timeout_ms: number;
    poll_interval_ms: number;
  };
  active_station_count: number;
  active_station_ids: string[];
  debug_contract?: DebugContract;
  debug_contract_hash?: string;
  engineering_rows?: Array<Record<string, unknown>>;
  engineering_export?: string;
  activation: ActivationRecord | null;
  rollback_available: boolean;
};

export type ActivationRecord = {
  activation_id: string;
  candidate_id: string;
  previous_active_mapping_hash: string;
  active_mapping_hash: string;
  changed_fields: string[];
  status: "ACTIVATED_RESTART_REQUIRED" | "ROLLED_BACK";
  backup_path: string;
  activation_record_path: string;
  fresh_connection_test: Pick<ConnectionTestResult, "status" | "read_only" | "writes_performed" | "operations">;
  writes_performed: false;
  rollback_available: boolean;
};

export type LineOption = {
  file_name: string;
  line_id: string;
  name: string;
  station_count: number;
  plc_count: number;
  config_hash: string;
  capability:
    | "CURRENTLY_SUPPORTED"
    | "CONFIG_VALID_RUNTIME_NOT_YET_SUPPORTED"
    | "CONFIG_VALID_MULTI_PLC_RUNTIME_NOT_YET_SUPPORTED";
  capability_label: string;
  ready_to_activate: boolean;
  active: boolean;
};

export type DeploymentValidation = {
  validation_state: "VALID" | "VALID_RUNTIME_NOT_SUPPORTED" | "INVALID";
  ready_to_activate: boolean;
  errors: Array<{ field: string; message: string }>;
  warnings: Array<{ field: string; message: string }>;
  active_mapping_hash: string;
  candidate_hash?: string;
  candidate?: DeploymentCandidate;
  debug_contract_hash?: string;
  engineering_rows?: Array<Record<string, unknown>>;
  engineering_export?: string;
  line?: LineOption;
};

export type ConnectionTestResult = DeploymentValidation & {
  status:
    | "CONNECTED_AND_READABLE"
    | "CONNECTION_REFUSED"
    | "TIMEOUT"
    | "RACK_SLOT_REJECTED"
    | "RUNTIME_DB_UNREADABLE"
    | "CONFIG_NOT_RUNTIME_SUPPORTED"
    | "INVALID_CONFIGURATION";
  read_only: boolean;
  writes_performed: boolean;
  operations: string[];
  message?: string;
  read_bytes?: number;
};

export type SavedCandidate = {
  candidate_id: string;
  created_at: string;
  status: "NOT ACTIVE / REQUIRES CONTROLLED ACTIVATION";
  candidate_hash: string;
  active_mapping_hash: string;
  validation_state: DeploymentValidation["validation_state"];
  candidate: DeploymentCandidate;
  debug_contract_hash?: string;
  engineering_rows?: Array<Record<string, unknown>>;
  engineering_export?: string;
  line: LineOption;
  last_connection_test: Pick<ConnectionTestResult, "status" | "message" | "read_only" | "writes_performed" | "operations"> | null;
  retrieval_path: string;
};

export type ActivationResult = {
  activation_id: string;
  candidate_id: string;
  previous_active_mapping_hash: string;
  active_mapping_hash: string;
  changed_fields: string[];
  status: "ACTIVATED_RESTART_REQUIRED";
  fresh_connection_test: Pick<ConnectionTestResult, "status" | "read_only" | "writes_performed" | "operations">;
  writes_performed: false;
  rollback_available: boolean;
  backup_path?: string;
  activation_record_path?: string;
};

export type ActivationError = {
  status: "STALE_CANDIDATE" | "FRESH_TEST_FAILED" | "CANDIDATE_NOT_READY" | "UNSUPPORTED_TOPOLOGY" | "CANDIDATE_IDENTITY_MISMATCH";
  candidate_id: string;
  writes_performed: false;
  fresh_connection_test?: ConnectionTestResult;
  message?: string;
};

export type DeploymentOverviewResult =
  | { ok: true; active: ActiveDeploymentConfig; lineOptions: LineOption[] }
  | { ok: false; message: string };

const endpoint = "/api/deployment/plc";

export async function fetchDeploymentOverview(fetchImpl: typeof fetch = fetch): Promise<DeploymentOverviewResult> {
  try {
    const [activeResponse, optionsResponse] = await Promise.all([
      fetchImpl(`${endpoint}/active`, { cache: "no-store", credentials: "same-origin" }),
      fetchImpl(`${endpoint}/line-options`, { cache: "no-store", credentials: "same-origin" })
    ]);
    if (!activeResponse.ok || !optionsResponse.ok) {
      return { ok: false, message: "Active PLC configuration or line options are unavailable." };
    }
    const active = (await activeResponse.json()) as ActiveDeploymentConfig;
    const options = (await optionsResponse.json()) as { items?: LineOption[] };
    if (!Array.isArray(options.items) || options.items.length === 0) {
      return { ok: false, message: "No valid line configuration options are available." };
    }
    return { ok: true, active, lineOptions: options.items };
  } catch {
    return { ok: false, message: "PLC deployment configuration service is unavailable." };
  }
}
export async function postDeployment<T>(
  action: "validate" | "test-connection" | "candidates" | `candidates/${string}/activate` | `activations/${string}/rollback`,
  payload: Record<string, unknown>,
  fetchImpl: typeof fetch = fetch
): Promise<{ ok: true; value: T } | { ok: false; message: string; value?: T }> {
  try {
    const response = await fetchImpl(`${endpoint}/${action}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify(payload)
    });
    const value = (await response.json()) as T;
    if (!response.ok) return { ok: false, message: "The PLC deployment action was rejected.", value };
    return { ok: true, value };
  } catch {
    return { ok: false, message: "The PLC deployment action could not be completed." };
  }
}
