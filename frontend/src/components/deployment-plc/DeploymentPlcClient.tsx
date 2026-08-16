"use client";

import { useEffect, useMemo, useState } from "react";

import {
  fetchDeploymentOverview,
  postDeployment,
  type ActiveDeploymentConfig,
  type ActivationError,
  type ActivationResult,
  type ConnectionTestResult,
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
  line_config: "demo_3_station.yaml"
};

const fieldLabels: Record<keyof DeploymentCandidate, string> = {
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
      setCandidate({
        host: result.active.plc.host,
        port: result.active.plc.port,
        rack: result.active.plc.rack,
        slot: result.active.plc.slot,
        connection_timeout_ms: result.active.plc.connection_timeout_ms,
        poll_interval_ms: result.active.plc.poll_interval_ms,
        line_config: result.lineOptions.find((option) => option.active)?.file_name ?? "demo_3_station.yaml"
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

  function updateField(field: keyof DeploymentCandidate, value: string) {
    setCandidate((current) => ({
      ...current,
      [field]: ["port", "rack", "slot", "connection_timeout_ms", "poll_interval_ms"].includes(field)
        ? Number(value)
        : value
    }));
    setValidation(null);
    setConnectionTest(null);
    setSaved(null);
    setActivation(null);
    setActivationError(null);
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
            operations: connectionTest.operations
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
        {selectedLine ? <p className="deployment-help"><strong>{selectedLine.capability_label}</strong> · {selectedLine.station_count} stations / {selectedLine.plc_count} PLC{selectedLine.plc_count === 1 ? "" : "s"}. {selectedLine.ready_to_activate ? "This is the current R2 supported topology." : "This can be inspected and validated, but cannot be marked ready-to-activate in R2."}</p> : null}
        <div className="deployment-actions">
          <button type="button" onClick={() => void validate()} disabled={busy !== null}>{busy === "validate" ? "Validating…" : "Validate candidate"}</button>
          <button type="button" className="deployment-secondary-action" onClick={() => void testConnection()} disabled={busy !== null}>{busy === "test" ? "Testing…" : "Test Connection · Read-only"}</button>
          <button type="button" className="deployment-secondary-action" onClick={() => void save()} disabled={busy !== null}>{busy === "save" ? "Saving…" : "Save candidate"}</button>
        </div>
      </section>

      <section className="deployment-two-column">
        <section className="deployment-panel" aria-labelledby="validation-heading">
          <div className="deployment-panel-heading"><h2 id="validation-heading">Validation</h2><span className="deployment-status">{validation?.validation_state ?? "Not run"}</span></div>
          {validation?.errors.length ? <ul className="deployment-errors">{validation.errors.map((error) => <li key={`${error.field}-${error.message}`}><strong>{error.field}</strong>: {error.message}</li>)}</ul> : <p>{validation ? (validation.ready_to_activate ? "Candidate fields and the selected line configuration are valid." : validation.warnings[0]?.message ?? "Configuration is valid but not ready for the current runtime boundary.") : "Run validation before saving a candidate."}</p>}
          {validation?.candidate_hash ? <p className="deployment-hash">Candidate hash: {validation.candidate_hash}</p> : null}
        </section>

        <section className="deployment-panel" aria-labelledby="connection-heading">
          <div className="deployment-panel-heading"><h2 id="connection-heading">Test Result</h2><span className="deployment-status deployment-status-readonly">Read-only</span></div>
          {connectionTest ? <div className="deployment-test-result" role="status"><strong>{connectionTest.status}</strong><p>{connectionTest.message}</p><p>Operations: {connectionTest.operations.join(" → ")}</p><p>PLC writes performed: <strong>{connectionTest.writes_performed ? "YES" : "NO"}</strong></p></div> : <p>Use Test Connection to attempt a bounded session and runtime DB read. No write, ACK, control bit, or mode change is performed.</p>}
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

      {saved ? <section className="deployment-panel deployment-saved-panel" aria-labelledby="saved-heading"><p className="deployment-eyebrow">SAVED CANDIDATE</p><h2 id="saved-heading">{saved.status}</h2><p>Candidate {saved.candidate_id} is stored separately from the active mapping and requires controlled activation before it can affect Collector behavior.</p><p className="deployment-help">Confirm: activation changes the effective Active config only; it performs no PLC write (`writes_performed=false`). Collector reload remains a fixed host-operator action.</p><div className="deployment-actions"><a href={`/api/deployment/plc/candidates/${saved.candidate_id}`}>Export / retrieve candidate JSON</a>{saved.validation_state === "VALID" && saved.line.ready_to_activate ? <button type="button" onClick={() => void activateSavedCandidate()} disabled={busy !== null}>{busy === "activate" ? "Activating…" : "Activate Candidate"}</button> : null}</div></section> : null}
      {activationError ? <section className="deployment-panel" role="alert"><p className="deployment-eyebrow">ACTIVATION BLOCKED</p><h2>{activationError.status}</h2><p>{activationError.message ?? "The Candidate was not activated and the Active config was not changed."}</p>{activationError.fresh_connection_test ? <p>Fresh Test Connection: {activationError.fresh_connection_test.status} · PLC writes: {activationError.fresh_connection_test.writes_performed ? "YES" : "NO"}</p> : null}</section> : null}
      {activation ? <section className="deployment-panel deployment-saved-panel" aria-labelledby="activation-heading"><p className="deployment-eyebrow">ACTIVATION RESULT</p><h2 id="activation-heading">{activation.status}</h2><p>Active mapping changed only in the authorized connectivity fields: {activation.changed_fields.join(", ") || "none"}.</p><p>Active hash: <code>{activation.active_mapping_hash}</code> · previous hash: <code>{activation.previous_active_mapping_hash}</code></p><p>Fresh Test Connection: <strong>{activation.fresh_connection_test.status}</strong> · config mutation only; PLC writes remain disabled (`writes_performed=false`).</p><p>COLLECTOR_RESTART_REQUIRED — run the fixed Collector-only recreate under the host operator boundary, then refresh Active Mapping.</p>{activation.rollback_available ? <button type="button" className="deployment-secondary-action" onClick={() => void rollbackActive()} disabled={busy !== null}>{busy === "rollback" ? "Rolling back…" : "Rollback active mapping"}</button> : null}</section> : null}
    </main>
  );
}
