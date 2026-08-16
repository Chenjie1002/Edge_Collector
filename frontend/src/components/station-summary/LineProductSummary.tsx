import { LineFlowSummary } from "./LineFlowSummary";
import { StationSummaryChart } from "./StationSummaryChart";
import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";

function percent(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${(value * 100).toFixed(1)}%`;
}

function seconds(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${value.toFixed(2)} s`;
}

export function LineProductSummary({ summary }: { summary: LineSummary }) {
  if (!summary.line || !summary.overview) return <LineFlowSummary summary={summary} />;

  const { line, overview } = summary;
  const production = summary.trends?.production ?? [];
  const cycleByStation = line.route.map((stationId) => ({
    stationId,
    points: (summary.trends?.cycleTime ?? [])
      .filter((point) => point.stationId === stationId)
      .map((point) => ({ label: point.bucketStart, value: point.averageCycleSeconds })),
  }));

  return (
    <div className="mes-product-stack">
      <section className="station-summary-panel mes-line-identity" aria-label="Line identity and runtime">
        <div>
          <p className="station-summary-panel-kicker">Active production line</p>
          <h2>{line.name}</h2>
          <p className="mes-muted-copy">{line.lineId} · {line.stationCount} stations · Entry {line.entryStationId} · Terminal {line.terminalStationId}</p>
        </div>
        <div className="mes-runtime-strip">
          <span><small>Profile</small><strong>{line.activeProfile}</strong></span>
          <span><small>Line runtime</small><strong data-status={line.runtimeStatus}>{line.runtimeStatus}</strong></span>
          <span><small>Collector</small><strong>{line.collectorState}</strong></span>
          <span><small>Connected stations</small><strong>{line.collectorConnectedStations}/{line.stationCount}</strong></span>
        </div>
        <div className="mes-route" aria-label="Configured production route">
          {line.route.map((stationId, index) => (
            <span key={stationId} className="mes-route-step">
              <strong>{stationId}</strong>{index < line.route.length - 1 ? <b aria-hidden="true">→</b> : null}
            </span>
          ))}
        </div>
        <p className="mes-window">Selected window · {summary.scope.startTime} → {summary.scope.endTime}</p>
        <p className="mes-caption">Runtime authority · {line.runtimeAuthority}</p>
      </section>

      <section className="mes-kpi-grid" aria-label="Line production KPIs">
        <div><span>Completed units</span><strong>{overview.completedUnits}</strong><small>terminal-completed cohort</small></div>
        <div><span>Final OK</span><strong>{overview.finalOk}</strong><small>terminal result</small></div>
        <div><span>Final NOK</span><strong>{overview.finalNok}</strong><small>terminal result</small></div>
        <div><span>Final yield</span><strong>{percent(overview.finalYield)}</strong><small>{overview.finalYield === null ? "Unavailable while route evidence is unreconciled" : "Final OK / completed units"}</small></div>
        <div><span>ACK pending</span><strong>{overview.ackPendingEvents}</strong><small>trusted cohort events</small></div>
        <div><span>Observed Avg CT</span><strong>{seconds(overview.averageCycleSeconds)}</strong><small>processed cycle_event samples</small></div>
        <div><span>Route conservation</span><strong data-status={overview.routeConservation}>{overview.routeConservation}</strong><small>Total = OK + NOK = Processed + Skipped</small></div>
        <div><span>Trace entry</span><strong><a href="/trace">Open Trace</a></strong><small>recent unit lifecycle</small></div>
      </section>

      <section className="mes-chart-grid">
        <article className="station-summary-panel mes-chart-panel">
          <header><div><p className="station-summary-panel-kicker">Production trend</p><h3>Terminal completions</h3></div><strong>{production.reduce((sum, point) => sum + point.completed, 0)}</strong></header>
          <StationSummaryChart
            ariaLabel="Terminal completed units trend"
            points={production.map((point) => ({ label: point.bucketStart, value: point.completed }))}
            xAxisLabel="Time"
            yAxisLabel="Completed units / bucket"
            unit="units"
            variant="line"
            emptyMessage="No trusted completed units in this window."
          />
        </article>
        <article className="station-summary-panel mes-chart-panel">
          <header><div><p className="station-summary-panel-kicker">CT trend</p><h3>Observed station cycle time</h3></div><span className="mes-caption">processed only</span></header>
          <div className="mes-station-trends">
            {cycleByStation.map(({ stationId, points }) => (
              <div key={stationId} className="mes-station-chart-row"><span>{stationId}</span><StationSummaryChart
                ariaLabel={`${stationId} cycle time trend`}
                points={points}
                xAxisLabel="Time"
                yAxisLabel="Cycle time"
                unit="s"
                variant="line"
                emptyMessage="No CT samples in this window."
              /></div>
            ))}
          </div>
        </article>
      </section>

      <LineFlowSummary summary={summary} />

      <section className="mes-chart-grid">
        <article className="station-summary-panel mes-distribution-panel">
          <header><div><p className="station-summary-panel-kicker">NOK accumulation</p><h3>Inherited NOK across route</h3></div></header>
          <StationSummaryChart
            ariaLabel="Inherited NOK across route"
            points={(summary.quality?.nokAccumulation ?? []).map((item) => ({ label: item.stationId, value: item.count }))}
            xAxisLabel="Station"
            yAxisLabel="Unit count"
            unit="units"
            emptyMessage="No inherited NOK data in this window."
          />
        </article>
        <article className="station-summary-panel mes-distribution-panel">
          <header><div><p className="station-summary-panel-kicker">New NOK by Station</p><h3>Defect origin</h3></div></header>
          <StationSummaryChart
            ariaLabel="New NOK by station"
            points={(summary.quality?.newNokByStation ?? []).map((item) => ({ label: item.stationId, value: item.count }))}
            xAxisLabel="Station"
            yAxisLabel="New NOK unit count"
            unit="units"
            emptyMessage="No new NOK data in this window."
          />
        </article>
      </section>

      <section className="mes-chart-grid">
        <article className="station-summary-panel mes-list-panel">
          <header><div><p className="station-summary-panel-kicker">NOK Code distribution</p><h3>Origin defect codes</h3></div></header>
          <StationSummaryChart
            ariaLabel="NOK code distribution"
            points={(summary.quality?.nokCodeDistribution ?? []).map((item) => ({ label: String(item.code), value: item.count }))}
            xAxisLabel="NOK Code"
            yAxisLabel="New NOK unit count"
            unit="units"
            emptyMessage="No new NOK code in this window."
          />
        </article>
        <article className="station-summary-panel mes-list-panel">
          <header><div><p className="station-summary-panel-kicker">Collector runtime status</p><h3>Latest station connectivity</h3></div></header>
          {(summary.collectorRuntime ?? []).length ? (
            <div className="mes-runtime-list">{summary.collectorRuntime?.map((row) => <div key={row.stationId}><strong>{row.stationId}</strong><span>{row.collectorState}</span><span>{row.plcConnectionState}</span><small>{row.updatedAt}</small></div>)}</div>
          ) : <p className="mes-empty">Collector runtime authority is unavailable.</p>}
        </article>
      </section>

      <section className="station-summary-panel mes-recent-panel">
        <header><div><p className="station-summary-panel-kicker">Recent completed units</p><h3>Terminal-completed cohort</h3></div><a href="/trace">Open Trace →</a></header>
        <div className="station-summary-table-scroll">
          <table className="accepted-events-table">
            <thead><tr><th>Unit</th><th>Result</th><th>Completed At</th><th>Defect Origin</th><th>Code</th><th>Trace</th></tr></thead>
            <tbody>
              {(summary.recentCompletedUnits ?? []).map((unit) => (
                <tr key={`${unit.unitId}-${unit.completedAt}`}><td><code>{unit.unitId}</code></td><td>{unit.result}</td><td>{unit.completedAt}</td><td>{unit.defectOriginStation ?? "—"}</td><td>{unit.defectCode ?? "—"}</td><td><a href={`/trace?q=${encodeURIComponent(unit.unitId)}`}>View</a></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
