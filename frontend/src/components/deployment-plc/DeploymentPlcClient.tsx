"use client";

import { useEffect, useMemo, useState } from "react";

import {
  fetchDeploymentOverview,
  postDeployment,
  type ActiveDeploymentConfig,
  type ActivationError,
  type ActivationResult,
  type ConnectionTestResult,
  type ConfirmationState,
  type DebugContract,
  type DebugScope,
  type DebugSignal,
  type DebugStation,
  type DeploymentCandidate,
  type DeploymentValidation,
  type LineOption,
  type SavedCandidate
} from "../../lib/deploymentPlc/apiClient";

const emptyCandidate: DeploymentCandidate = {
  host: "",
  port: 1102,
  rack: 0,
  slot: 1,
  connection_timeout_ms: 3000,
  poll_interval_ms: 500,
  line_config: "demo_3_station.yaml",
  debug_scope: { station_ids: [] },
  stations: [],
  write_allowlist: {
    mode: "READ_DONE_ONLY",
    edge_to_plc: [],
    parameter_writes_enabled: false,
    machine_control_writes_enabled: false,
    safety_writes_enabled: false,
    arbitrary_db_writes_enabled: false
  }
};

const confirmationStates: ConfirmationState[] = ["PLANNED", "CONFIRMED"];

function emptyDebugContract(): DebugContract {
  return {
    schema_version: "plc-debug-contract/v1",
    debug_scope: { station_ids: [] },
    stations: [],
    write_allowlist: {
      mode: "READ_DONE_ONLY",
      edge_to_plc: [],
      parameter_writes_enabled: false,
      machine_control_writes_enabled: false,
      safety_writes_enabled: false,
      arbitrary_db_writes_enabled: false
    }
  };
}

function cloneDebugContract(contract?: DebugContract): DebugContract {
  if (!contract) return emptyDebugContract();
  return JSON.parse(JSON.stringify(contract)) as DebugContract;
}

function scopeIds(contract?: DebugContract): string[] {
  const scope: DebugScope | undefined = contract?.debug_scope;
  return scope?.station_ids ?? contract?.stations.map((station) => station.station_id) ?? [];
}

type ConnectionField = "host" | "port" | "rack" | "slot" | "connection_timeout_ms" | "poll_interval_ms" | "line_config";

const fieldLabels: Record<ConnectionField, string> = {
  host: "PLC host / IP",
  port: "Port",
  rack: "Rack",
  slot: "Slot",
  connection_timeout_ms: "Connection timeout (ms)",
  poll_interval_ms: "Poll interval (ms)",
  line_config: "Line configuration"
};

export function DeploymentPlcClient() {
  const [active, setActive] = useState<ActiveDeploymentConfig | null>(null);
  const [lineOptions, setLineOptions] = useState<LineOption[]>([]);
  const [candidate, setCandidate] = useState<DeploymentCandidate>(emptyCandidate);
  const [loading, setLoading] = useState(true);
  const [pageError, setPageError] = useState<string | null>(null);
  const [validation, setValidation] = useState<DeploymentValidation | null>(null);
  const [connectionTest, setConnectionTest] = useState<ConnectionTestResult | null>(null);
  const [saved, setSaved] = useState<SavedCandidate | null>(null);
  const [activation, setActivation] = useState<ActivationResult | null>(null);
  const [activationError, setActivationError] = useState<ActivationError | null>(null);
  const [busy, setBusy] = useState<"validate" | "test" | "save" | "activate" | "rollback" | null>(null);

  useEffect(() => {
    let cancelled = false;
    void fetchDeploymentOverview().then((result) => {
      if (cancelled) return;
      setLoading(false);
      if (!result.ok) {
        setPageError(result.message);
        return;
      }
      setActive(result.active);
      setLineOptions(result.lineOptions);
      const initialContract = cloneDebugContract(result.active.debug_contract);
      setCandidate({
        host: result.active.plc.host,
        port: result.active.plc.port,
        rack: result.active.plc.rack,
        slot: result.active.plc.slot,
        connection_timeout_ms: result.active.plc.connection_timeout_ms,
        poll_interval_ms: result.active.plc.poll_interval_ms,
        line_config: result.lineOptions.find((option) => option.active)?.file_name ?? "demo_3_station.yaml",
        debug_scope: { station_ids: scopeIds(initialContract) },
        stations: initialContract.stations,
        write_allowlist: initialContract.write_allowlist
      });
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const selectedLine = useMemo(
    () => lineOptions.find((option) => option.file_name === candidate.line_config) ?? null,
    [candidate.line_config, lineOptions]
  );
  const activeContract = cloneDebugContract(active?.debug_contract);
  const enabledStationIds = useMemo(() => {
    if (selectedLine?.station_ids?.length) return selectedLine.station_ids;
    if (selectedLine?.active || candidate.line_config === active?.line_id) return active?.active_station_ids ?? [];
    return candidate.debug_scope.station_ids;
  }, [active?.active_station_ids, active?.line_id, candidate.debug_scope.station_ids, candidate.line_config, selectedLine]);
  const selectedScopeIds = candidate.debug_scope.station_ids;
  const fullScopeSelected = enabledStationIds.length > 0
    && selectedScopeIds.length === enabledStationIds.length
    && enabledStationIds.every((stationId) => selectedScopeIds.includes(stationId));

  function updateField(field: ConnectionField, value: string) {
    setCandidate((current) => {
      const next = {
        ...current,
        [field]: ["port", "rack", "slot", "connection_timeout_ms", "poll_interval_ms"].includes(field)
          ? Number(value)
          : value
      };
      if (field === "line_config") {
        const nextLine = lineOptions.find((option) => option.file_name === value);
        const nextIds = nextLine?.station_ids ?? [];
        if (nextIds.length) {
          next.debug_scope = { station_ids: nextIds };
          next.stations = current.stations.filter((station) => nextIds.includes(station.station_id));
          next.write_allowlist = {
            ...current.write_allowlist,
            edge_to_plc: current.write_allowlist.edge_to_plc.filter((entry) => nextIds.includes(entry.station_id))
          };
        }
      }
      return next;
    });
    clearCandidateResults();
  }

  function clearCandidateResults() {
    setValidation(null);
    setConnectionTest(null);
    setSaved(null);
    setActivation(null);
    setActivationError(null);
  }

  function updateScope(stationId: string, selected: boolean) {
    setCandidate((current) => {
      const currentIds = current.debug_scope.station_ids;
      const nextIds = selected
        ? [...currentIds, stationId]
        : currentIds.filter((item) => item !== stationId);
      const orderedIds = enabledStationIds.filter((item) => nextIds.includes(item));
      const activeStation = activeContract.stations.find((station) => station.station_id === stationId);
      const existingStation = current.stations.find((station) => station.station_id === stationId);
      const nextStations = current.stations.filter((station) => orderedIds.includes(station.station_id));
      if (selected && !existingStation && activeStation) {
        nextStations.push(JSON.parse(JSON.stringify(activeStation)) as DebugStation);
      }
      nextStations.sort((left, right) => orderedIds.indexOf(left.station_id) - orderedIds.indexOf(right.station_id));
      const nextAllowlist = {
        ...current.write_allowlist,
        edge_to_plc: current.write_allowlist.edge_to_plc.filter((entry) => orderedIds.includes(entry.station_id))
      };
      if (selected && activeStation && !nextAllowlist.edge_to_plc.some((entry) => entry.station_id === stationId)) {
        const readDone = activeStation.signals.find((signal) => signal.field_name === "read_done");
        if (readDone) {
          nextAllowlist.edge_to_plc.push({
            station_id: stationId,
            field_name: "read_done",
            address: readDone.address,
            type: readDone.type,
            direction: "EDGE_TO_PLC",
            confirmation_state: readDone.confirmation_state
          });
        }
      }
      return {
        ...current,
        debug_scope: { station_ids: orderedIds },
        stations: nextStations,
        write_allowlist: {
          ...nextAllowlist,
          edge_to_plc: nextAllowlist.edge_to_plc.sort((left, right) => orderedIds.indexOf(left.station_id) - orderedIds.indexOf(right.station_id))
        }
      };
    });
    clearCandidateResults();
  }

  function updateStation(index: number, patch: Partial<DebugStation>) {
    setCandidate((current) => ({
      ...current,
      stations: current.stations.map((station, stationIndex) =>
        stationIndex === index ? { ...station, ...patch } : station
      )
    }));
    setValidation(null);
    setConnectionTest(null);
    setSaved(null);
  }

  function updateSignal(stationIndex: number, signalIndex: number, patch: Partial<DebugSignal>) {
    setCandidate((current) => {
      const station = current.stations[stationIndex];
      const signal = station?.signals[signalIndex];
      const nextSignal = signal ? { ...signal, ...patch } : null;
      const nextStations = current.stations.map((item, currentStationIndex) =>
        currentStationIndex !== stationIndex
          ? item
          : {
              ...item,
              signals: item.signals.map((itemSignal, currentSignalIndex) =>
                currentSignalIndex === signalIndex ? { ...itemSignal, ...patch } : itemSignal
              )
            }
      );
      const nextAllowlist = nextSignal?.field_name === "read_done"
        ? {
            ...current.write_allowlist,
            edge_to_plc: current.write_allowlist.edge_to_plc.map((entry) =>
              entry.station_id === station.station_id
                ? {
                    ...entry,
                    address: nextSignal.address,
                    type: nextSignal.type,
                    confirmation_state: nextSignal.confirmation_state
                  }
                : entry
            )
          }
        : current.write_allowlist;
      return { ...current, stations: nextStations, write_allowlist: nextAllowlist };
    });
    setValidation(null);
    setConnectionTest(null);
    setSaved(null);
  }

  async function validate() {
    setBusy("validate");
    const result = await postDeployment<DeploymentValidation>("validate", candidate as unknown as Record<string, unknown>);
    setBusy(null);
    if (!result.ok) {
      if (result.value) setValidation(result.value);
      setPageError(result.message);
      return;
    }
    setPageError(null);
    setValidation(result.value);
  }

  async function testConnection() {
    setBusy("test");
    const result = await postDeployment<ConnectionTestResult>("test-connection", candidate as unknown as Record<string, unknown>);
    setBusy(null);
    if (!result.ok && !result.value) {
      setPageError(result.message);
      return;
    }
    setPageError(null);
    if (result.value) setConnectionTest(result.value);
  }

  async function save() {
    setBusy("save");
    const result = await postDeployment<SavedCandidate>("candidates", {
      ...candidate,
      last_connection_test: connectionTest
        ? {
            status: connectionTest.status,
            message: connectionTest.message,
            read_only: connectionTest.read_only,
            writes_performed: connectionTest.writes_performed,
            operations: connectionTest.operations,
            probed_station_ids: connectionTest.probed_station_ids,
            probed_ranges: connectionTest.probed_ranges,
            read_bytes: connectionTest.read_bytes
          }
        : null
    });
    setBusy(null);
    if (!result.ok) {
      setPageError(result.message);
      if (result.value && "errors" in result.value) setValidation(result.value as unknown as DeploymentValidation);
      return;
    }
    setPageError(null);
    setSaved(result.value);
    setActivation(null);
    setActivationError(null);
  }

  async function refreshActive() {
    const result = await fetchDeploymentOverview();
    if (result.ok) {
      setActive(result.active);
      setLineOptions(result.lineOptions);
    }
  }

  async function activateSavedCandidate() {
    if (!saved) return;
    setBusy("activate");
    const result = await postDeployment<ActivationResult | ActivationError>(`candidates/${saved.candidate_id}/activate`, {});
    setBusy(null);
    if (!result.ok) {
      setActivationError(result.value as ActivationError | undefined ?? null);
      setPageError(result.message);
      return;
    }
    setPageError(null);
    setActivationError(null);
    setActivation(result.value as ActivationResult);
    await refreshActive();
  }

  async function rollbackActive() {
    if (!activation) return;
    setBusy("rollback");
    const result = await postDeployment<ActivationResult>(`activations/${activation.activation_id}/rollback`, {});
    setBusy(null);
    if (!result.ok) {
      setPageError(result.message);
      return;
    }
    setActivation(null);
    setPageError(null);
    await refreshActive();
  }

  if (loading) {
    return <main className="dashboard-shell deployment-plc-shell"><p>Loading PLC deployment configuration…</p></main>;
  }

  if (!active || pageError && lineOptions.length === 0) {
    return (
      <main className="dashboard-shell deployment-plc-shell">
        <section className="deployment-state" role="alert">
          <p className="deployment-eyebrow">PLC Deployment Configuration</p>
          <h1>Configuration unavailable</h1>
          <p>{pageError ?? "The active configuration could not be loaded."}</p>
        </section>
      </main>
    );
  }

  return (
    <main className="dashboard-shell deployment-plc-shell">
      <header className="deployment-header">
        <div>
          <p className="deployment-eyebrow">Field deployment · configuration foundation</p>
          <h1>PLC Deployment Configuration</h1>
          <p>Prepare a candidate PLC connection and line selection without editing runtime YAML or changing the active Collector configuration.</p>
        </div>
        <div className="deployment-policy" aria-label="PLC deployment safety policy">
          <span>Active is read-only</span>
          <span>Test Connection is read-only</span>
          <span>Collector lifecycle is operator-controlled</span>
        </div>
      </header>

      {pageError ? <p className="deployment-inline-error" role="alert">{pageError}</p> : null}

      <section className="deployment-panel" aria-labelledby="active-configuration-heading">
        <div className="deployment-panel-heading">
          <div>
            <p className="deployment-eyebrow">ACTIVE</p>
            <h2 id="active-configuration-heading">Current active configuration</h2>
          </div>
          <span className="deployment-status deployment-status-active">Collector authority</span>
        </div>
        <dl className="deployment-details">
          <dt>Line</dt><dd>{active.line_id} · {active.line_name}</dd>
          <dt>Config version</dt><dd>{active.authority.config_version}</dd>
          <dt>Mapping hash</dt><dd>{active.authority.content_sha256}</dd>
          <dt>PLC</dt><dd>{active.plc.plc_id} · {active.plc.host}</dd>
          <dt>Port / rack / slot</dt><dd>{active.plc.port} / {active.plc.rack} / {active.plc.slot}</dd>
          <dt>Timeout / poll</dt><dd>{active.plc.connection_timeout_ms} ms / {active.plc.poll_interval_ms} ms</dd>
          <dt>Stations</dt><dd>{active.active_station_count} · {active.active_station_ids.join(", ")}</dd>
        </dl>
      </section>

      <section className="deployment-panel" aria-labelledby="active-contract-heading">
        <div className="deployment-panel-heading">
          <div>
            <p className="deployment-eyebrow">ACTIVE · READ-ONLY</p>
            <h2 id="active-contract-heading">Active Debug Communication Contract</h2>
          </div>
          <span className="deployment-status deployment-status-readonly">Active mapping</span>
        </div>
        <p className="deployment-help">The Active contract is an evidence surface only. It is not editable here and it remains separate from the Candidate contract.</p>
        <p className="deployment-write-policy"><strong>Write authority:</strong> Read_Done only. Parameter writes, machine-control writes, safety writes and arbitrary DB writes are disabled.</p>
        {activeContract.stations.length ? (
          <div className="deployment-contract-list">
            {activeContract.stations.map((station) => (
              <div className="deployment-contract-card" key={`active-${station.station_id}`}>
                <div className="deployment-contract-card-heading">
                  <h3>{station.station_id}</h3>
                  <span className="deployment-status">{station.confirmation_state}</span>
                </div>
                <p className="deployment-contract-range">DB{station.db_number} · bytes {station.read_start}–{station.read_start + station.read_length - 1} · {station.read_length} bytes</p>
                <div className="deployment-table-scroll">
                  <table className="deployment-contract-table">
                    <caption>{station.station_id} active signal map</caption>
                    <thead><tr><th>Field</th><th>PLC address</th><th>Type</th><th>Direction</th><th>Confirmation</th></tr></thead>
                    <tbody>{station.signals.map((signal) => <tr key={`${station.station_id}-${signal.field_name}`}>
                      <th scope="row">{signal.field_name}</th>
                      <td><code>{signal.address}</code></td>
                      <td>{signal.type}</td>
                      <td>{signal.field_name === "read_done" ? "Read_Done · READ_WRITE" : signal.direction}</td>
                      <td><span className="deployment-status">{signal.confirmation_state}</span></td>
                    </tr>)}</tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        ) : <p>No Debug Communication Contract was returned by this legacy-compatible Active endpoint.</p>}
      </section>

      <section className="deployment-panel" aria-labelledby="candidate-configuration-heading">
        <div className="deployment-panel-heading">
          <div>
            <p className="deployment-eyebrow">CANDIDATE</p>
            <h2 id="candidate-configuration-heading">Edit candidate connection</h2>
          </div>
          <span className="deployment-status deployment-status-candidate">Not active</span>
        </div>
        <div className="deployment-form-grid">
          <label>PLC host / IP<input aria-label={fieldLabels.host} value={candidate.host} onChange={(event) => updateField("host", event.target.value)} /></label>
          <label>Port<input aria-label={fieldLabels.port} type="number" value={candidate.port} onChange={(event) => updateField("port", event.target.value)} /></label>
          <label>Rack<input aria-label={fieldLabels.rack} type="number" value={candidate.rack} onChange={(event) => updateField("rack", event.target.value)} /></label>
          <label>Slot<input aria-label={fieldLabels.slot} type="number" value={candidate.slot} onChange={(event) => updateField("slot", event.target.value)} /></label>
          <label>Connection timeout (ms)<input aria-label={fieldLabels.connection_timeout_ms} type="number" value={candidate.connection_timeout_ms} onChange={(event) => updateField("connection_timeout_ms", event.target.value)} /></label>
          <label>Poll interval (ms)<input aria-label={fieldLabels.poll_interval_ms} type="number" value={candidate.poll_interval_ms} onChange={(event) => updateField("poll_interval_ms", event.target.value)} /></label>
          <label className="deployment-line-field">Line configuration<select aria-label={fieldLabels.line_config} value={candidate.line_config} onChange={(event) => updateField("line_config", event.target.value)}>
            {lineOptions.map((option) => <option key={option.file_name} value={option.file_name}>{option.file_name} · {option.capability_label}</option>)}
          </select></label>
        </div>
        {selectedLine ? <p className="deployment-help"><strong>{selectedLine.capability_label}</strong> · {selectedLine.station_count} stations / {selectedLine.plc_count} PLC{selectedLine.plc_count === 1 ? "" : "s"}. {selectedLine.ready_to_activate && fullScopeSelected ? "This is the current full-line supported topology." : selectedLine.ready_to_activate ? "The base line is supported, but the selected Debug Pilot scope is not full-line activation-ready." : "This can be inspected and validated, but cannot be marked ready-to-activate in the current runtime boundary."}</p> : null}
        <div className="deployment-scope-panel" aria-label="Debug Pilot station scope">
          <div>
            <p className="deployment-eyebrow">DEBUG PILOT SCOPE</p>
            <strong>Debug Pilot Scope: {selectedScopeIds.length} / {enabledStationIds.length}</strong>
            <p className="deployment-help">Select only the stations needed for this local debug run. Unselected stations are not part of the effective candidate mapping.</p>
          </div>
          <div className="deployment-scope-options">
            {enabledStationIds.map((stationId) => (
              <label key={stationId}>
                <input
                  type="checkbox"
                  aria-label={`Debug Pilot ${stationId}`}
                  checked={selectedScopeIds.includes(stationId)}
                  onChange={(event) => updateScope(stationId, event.target.checked)}
                />
                {stationId}
              </label>
            ))}
          </div>
          <div className="deployment-readiness-grid" aria-label="Candidate readiness">
            <span>Debug Ready: <strong>{validation ? (validation.debug_ready ? "READY" : "NOT READY") : "NOT VALIDATED"}</strong></span>
            <span>Full-line activation: <strong>{fullScopeSelected ? "REQUIRES FULL VALIDATION" : "NOT READY"}</strong></span>
          </div>
        </div>
        <div className="deployment-contract-editor" aria-labelledby="candidate-contract-heading">
          <div className="deployment-contract-card-heading">
            <div>
              <p className="deployment-eyebrow">CANDIDATE · EDITABLE</p>
              <h3 id="candidate-contract-heading">Debug Communication Contract</h3>
            </div>
            <span className="deployment-status deployment-status-candidate">Candidate / not active</span>
          </div>
          <p className="deployment-write-policy"><strong>Write allowlist:</strong> Read_Done only. The disabled write categories below cannot be enabled by this FV1A contract.</p>
          {candidate.stations.length ? (
            <div className="deployment-contract-list">
            {candidate.stations.map((station, stationIndex) => selectedScopeIds.includes(station.station_id) ? (
                <div className="deployment-contract-card" key={`candidate-${station.station_id}`}>
                  <div className="deployment-contract-card-heading">
                    <div>
                      <h4>{station.station_id}</h4>
                      <p className="deployment-contract-range">Station identity is seeded from the selected line; DB/range remain candidate-editable.</p>
                    </div>
                    <label className="deployment-compact-field">Confirmation
                      <select aria-label={`${station.station_id} confirmation state`} value={station.confirmation_state} onChange={(event) => updateStation(stationIndex, { confirmation_state: event.target.value as ConfirmationState })}>
                        {confirmationStates.map((state) => <option key={state} value={state}>{state}</option>)}
                      </select>
                    </label>
                  </div>
                  <div className="deployment-contract-range-grid">
                    <label>Station DB<input aria-label={`${station.station_id} DB number`} type="number" value={station.db_number} onChange={(event) => updateStation(stationIndex, { db_number: Number(event.target.value) })} /></label>
                    <label>Read start<input aria-label={`${station.station_id} read start`} type="number" value={station.read_start} onChange={(event) => updateStation(stationIndex, { read_start: Number(event.target.value) })} /></label>
                    <label>Read length<input aria-label={`${station.station_id} read length`} type="number" value={station.read_length} onChange={(event) => updateStation(stationIndex, { read_length: Number(event.target.value) })} /></label>
                  </div>
                  <div className="deployment-table-scroll">
                    <table className="deployment-contract-table deployment-contract-edit-table">
                      <caption>{station.station_id} candidate signal map</caption>
                      <thead><tr><th>Field</th><th>PLC address</th><th>Type</th><th>Direction</th><th>Unit / description</th><th>Confirmation</th></tr></thead>
                      <tbody>{station.signals.map((signal, signalIndex) => <tr key={`${station.station_id}-${signal.field_name}`}>
                        <th scope="row"><code>{signal.field_name}</code></th>
                        <td><input aria-label={`${station.station_id} ${signal.field_name} address`} value={signal.address} onChange={(event) => updateSignal(stationIndex, signalIndex, { address: event.target.value })} /></td>
                        <td><select aria-label={`${station.station_id} ${signal.field_name} type`} value={signal.type} onChange={(event) => updateSignal(stationIndex, signalIndex, { type: event.target.value })}><option value="bool">bool</option><option value="word">word</option><option value="dint">dint</option><option value="real">real</option><option value="unix_time_seconds">unix_time_seconds</option><option value="string">string</option></select></td>
                        <td><select aria-label={`${station.station_id} ${signal.field_name} direction`} value={signal.direction} onChange={(event) => updateSignal(stationIndex, signalIndex, { direction: event.target.value as DebugSignal["direction"] })}><option value="PLC_TO_EDGE">PLC_TO_EDGE</option><option value="READ_WRITE">READ_WRITE</option><option value="EDGE_TO_PLC">EDGE_TO_PLC</option></select>{signal.field_name === "read_done" ? <small>Read_Done only</small> : null}</td>
                        <td><input aria-label={`${station.station_id} ${signal.field_name} unit`} value={signal.unit ?? ""} onChange={(event) => updateSignal(stationIndex, signalIndex, { unit: event.target.value })} /><input aria-label={`${station.station_id} ${signal.field_name} description`} value={signal.description ?? ""} onChange={(event) => updateSignal(stationIndex, signalIndex, { description: event.target.value })} /></td>
                        <td><select aria-label={`${station.station_id} ${signal.field_name} confirmation state`} value={signal.confirmation_state} onChange={(event) => updateSignal(stationIndex, signalIndex, { confirmation_state: event.target.value as ConfirmationState })}>{confirmationStates.map((state) => <option key={state} value={state}>{state}</option>)}</select></td>
                      </tr>)}</tbody>
                    </table>
                  </div>
                </div>
              ) : null)}
            </div>
          ) : <p className="deployment-inline-error">No candidate station mappings are available. Load an Active contract from the API before saving.</p>}
          <div className="deployment-write-allowlist" aria-label="Candidate write allowlist">
            <strong>Read_Done only</strong>
            <span>Mode: {candidate.write_allowlist.mode}</span>
            <span>Allowed entries: {candidate.write_allowlist.edge_to_plc.map((entry) => `${entry.station_id} · ${entry.address}`).join(", ") || "none"}</span>
            <label><input type="checkbox" checked={false} disabled readOnly /> Parameter writes disabled</label>
            <label><input type="checkbox" checked={false} disabled readOnly /> Machine-control writes disabled</label>
            <label><input type="checkbox" checked={false} disabled readOnly /> Safety writes disabled</label>
            <label><input type="checkbox" checked={false} disabled readOnly /> Arbitrary DB writes disabled</label>
          </div>
        </div>
        <div className="deployment-actions">
          <button type="button" onClick={() => void validate()} disabled={busy !== null}>{busy === "validate" ? "Validating…" : "Validate candidate"}</button>
          <button type="button" className="deployment-secondary-action" onClick={() => void testConnection()} disabled={busy !== null}>{busy === "test" ? "Testing…" : "Test Connection · Read-only"}</button>
          <button type="button" className="deployment-secondary-action" onClick={() => void save()} disabled={busy !== null}>{busy === "save" ? "Saving…" : "Save candidate"}</button>
        </div>
      </section>

      <section className="deployment-two-column">
        <section className="deployment-panel" aria-labelledby="validation-heading">
          <div className="deployment-panel-heading"><h2 id="validation-heading">Validation</h2><span className="deployment-status">{validation?.validation_state ?? "Not run"}</span></div>
          {validation ? <div className="deployment-readiness-grid" aria-label="Validation readiness">
            <span>Debug Ready: <strong>{validation.debug_ready ? "READY" : "NOT READY"}</strong></span>
            <span>Full-line activation: <strong>{validation.ready_to_activate ? "READY" : "NOT READY"}</strong></span>
          </div> : null}
          {validation?.errors.length ? <ul className="deployment-errors">{validation.errors.map((error) => <li key={`${error.field}-${error.message}`}><strong>{error.field}</strong>: {error.message}</li>)}</ul> : <p>{validation ? (validation.ready_to_activate ? "Candidate fields and the selected line configuration are valid." : validation.warnings[0]?.message ?? "Configuration is valid but not ready for the current runtime boundary.") : "Run validation before saving a candidate."}</p>}
          {validation?.candidate_hash ? <p className="deployment-hash">Candidate hash: {validation.candidate_hash}</p> : null}
        </section>

        <section className="deployment-panel" aria-labelledby="connection-heading">
          <div className="deployment-panel-heading"><h2 id="connection-heading">Test Result</h2><span className="deployment-status deployment-status-readonly">Read-only</span></div>
          {connectionTest ? <div className="deployment-test-result" role="status"><strong>{connectionTest.status}</strong><p>{connectionTest.message}</p><p>Probed stations: {connectionTest.probed_station_ids?.join(", ") || "none"}</p><p>Operations: {connectionTest.operations.join(" → ")}</p><p>PLC writes performed: <strong>{connectionTest.writes_performed ? "YES" : "NO"}</strong></p></div> : <p>Use Test Connection to attempt bounded reads of the selected station DB/ranges. No write, ACK, control bit, or mode change is performed.</p>}
        </section>
      </section>

      <section className="deployment-panel" aria-labelledby="diff-heading">
        <div className="deployment-panel-heading"><div><p className="deployment-eyebrow">DIFF</p><h2 id="diff-heading">Active vs candidate</h2></div><span className="deployment-status">Separate identities</span></div>
        <ul className="deployment-diff-list">
          <li><span>PLC host</span><code>{active.plc.host}</code><span>→</span><code>{candidate.host || "(empty)"}</code></li>
          <li><span>Port</span><code>{active.plc.port}</code><span>→</span><code>{candidate.port}</code></li>
          <li><span>Rack / slot</span><code>{active.plc.rack} / {active.plc.slot}</code><span>→</span><code>{candidate.rack} / {candidate.slot}</code></li>
          <li><span>Line</span><code>{active.line_id}</code><span>→</span><code>{selectedLine?.line_id ?? candidate.line_config}</code></li>
        </ul>
      </section>

      {saved ? <section className="deployment-panel deployment-saved-panel" aria-labelledby="saved-heading"><p className="deployment-eyebrow">SAVED CANDIDATE</p><h2 id="saved-heading">{saved.status}</h2><p>Candidate {saved.candidate_id} is stored separately from the active mapping. A partial Debug Pilot candidate remains debug-only and cannot affect the full-line Collector configuration.</p><p className="deployment-help">Confirm: activation changes the effective Active config only; it performs no PLC write (`writes_performed=false`). Collector reload remains a fixed host-operator action.</p><div className="deployment-actions"><a href={`/api/deployment/plc/candidates/${saved.candidate_id}`}>Export / retrieve candidate JSON</a>{saved.validation_state === "VALID" && (saved.ready_to_activate ?? saved.line.ready_to_activate) ? <button type="button" onClick={() => void activateSavedCandidate()} disabled={busy !== null}>{busy === "activate" ? "Activating…" : "Activate Candidate"}</button> : null}</div></section> : null}
      {activationError ? <section className="deployment-panel" role="alert"><p className="deployment-eyebrow">ACTIVATION BLOCKED</p><h2>{activationError.status}</h2><p>{activationError.message ?? "The Candidate was not activated and the Active config was not changed."}</p>{activationError.fresh_connection_test ? <p>Fresh Test Connection: {activationError.fresh_connection_test.status} · PLC writes: {activationError.fresh_connection_test.writes_performed ? "YES" : "NO"}</p> : null}</section> : null}
      {activation ? <section className="deployment-panel deployment-saved-panel" aria-labelledby="activation-heading"><p className="deployment-eyebrow">ACTIVATION RESULT</p><h2 id="activation-heading">{activation.status}</h2><p>Active mapping changed only in the authorized connectivity fields: {activation.changed_fields.join(", ") || "none"}.</p><p>Active hash: <code>{activation.active_mapping_hash}</code> · previous hash: <code>{activation.previous_active_mapping_hash}</code></p><p>Fresh Test Connection: <strong>{activation.fresh_connection_test.status}</strong> · config mutation only; PLC writes remain disabled (`writes_performed=false`).</p><p>COLLECTOR_RESTART_REQUIRED — run the fixed Collector-only recreate under the host operator boundary, then refresh Active Mapping.</p>{activation.rollback_available ? <button type="button" className="deployment-secondary-action" onClick={() => void rollbackActive()} disabled={busy !== null}>{busy === "rollback" ? "Rolling back…" : "Rollback active mapping"}</button> : null}</section> : null}
    </main>
  );
}
