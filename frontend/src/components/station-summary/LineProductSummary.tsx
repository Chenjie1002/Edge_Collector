import { LineFlowSummary } from "./LineFlowSummary";
import { STATION_COLORS, stationColorFor, StationSummaryChart, type StationSummaryChartSeries } from "./StationSummaryChart";
import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";

function percent(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${(value * 100).toFixed(1)}%`;
}

function seconds(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${value.toFixed(2)} s`;
}

function stationSeries(summary: LineSummary, kind: "cycle" | "production"): readonly StationSummaryChartSeries[] {
  const route = summary.line?.route ?? summary.topology.stations;
  return route.map((stationId, index) => ({
    id: stationId,
    label: stationId,
    color: stationColorFor(stationId, index),
    points: kind === "cycle"
      ? (summary.trends?.cycleTime ?? [])
        .filter((point) => point.stationId === stationId)
        .map((point) => ({ label: point.bucketStart, value: point.averageCycleSeconds }))
      : (summary.trends?.productionByStation ?? [])
        .filter((point) => point.stationId === stationId)
        .map((point) => ({ label: point.bucketStart, value: point.completed })),
  }));
}

export function LineProductSummary({ summary }: { summary: LineSummary }) {
  if (!summary.line || !summary.overview) return <LineFlowSummary summary={summary} />;

  const { line, overview } = summary;
  const stationProduction = stationSeries(summary, "production");
  const stationCycle = stationSeries(summary, "cycle");
  const okNokSeries: readonly StationSummaryChartSeries[] = [
    {
      id: "OK",
      label: "OK",
      color: STATION_COLORS[0],
      points: line.route.map((stationId) => ({
        label: stationId,
        value: summary.stations.find((station) => station.stationId === stationId)?.ok ?? 0,
      })),
    },
    {
      id: "NOK",
      label: "NOK",
      color: STATION_COLORS[1],
      points: line.route.map((stationId) => ({
        label: stationId,
        value: summary.stations.find((station) => station.stationId === stationId)?.nok ?? 0,
      })),
    },
  ];
  const newNokTotal = summary.stations.reduce((total, station) => total + station.newNok, 0);

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
        <div><span>Completed units</span><strong>{overview.completedUnits}</strong><small>terminal-completed cohort · Terminal OK {overview.finalOk}</small></div>
        <div><span>Final yield</span><strong>{percent(overview.finalYield)}</strong><small>terminal OK / completed units</small></div>
        <div><span>Average CT</span><strong>{seconds(overview.averageCycleSeconds)}</strong><small>processed cycle_event samples</small></div>
        <div><span>ACK pending</span><strong>{overview.ackPendingEvents}</strong><small>trusted terminal cohort events</small></div>
        <div><span>Collector online stations</span><strong>{line.collectorConnectedStations}/{line.stationCount}</strong><small>{line.collectorState}</small></div>
        <div><span>NOK events / new NOK</span><strong>{overview.finalNok} / {newNokTotal}</strong><small>terminal NOK / route defect origins</small></div>
      </section>

      <details className="mes-route-evidence">
        <summary><span>Route evidence</span><strong>Route conservation: {overview.routeConservation}</strong></summary>
        <LineFlowSummary summary={summary} />
      </details>

      <section className="mes-chart-grid mes-trend-grid" aria-label="Line trend charts">
        <article className="station-summary-panel mes-chart-panel" data-panel="cycle-time-trend">
          <header><div><p className="station-summary-panel-kicker">Cycle time</p><h3>Cycle Time Trend</h3></div><span className="mes-caption">seconds · processed events</span></header>
          <StationSummaryChart
            ariaLabel="Cycle Time Trend"
            series={stationCycle}
            xAxisLabel="Time"
            yAxisLabel="Cycle time"
            unit="s"
            variant="line"
            emptyMessage="No trusted processed CT samples in this window."
          />
        </article>
        <article className="station-summary-panel mes-chart-panel" data-panel="production-trend">
          <header><div><p className="station-summary-panel-kicker">Production</p><h3>Production Trend</h3></div><span className="mes-caption">units / bucket · all route stations</span></header>
          <StationSummaryChart
            ariaLabel="Production Trend"
            series={stationProduction}
            xAxisLabel="Time"
            yAxisLabel="Units / bucket"
            unit="units"
            variant="line"
            emptyMessage="No trusted completed units in this window."
          />
        </article>
      </section>

      <section className="mes-dashboard-distribution-grid" aria-label="Line distribution and runtime">
        <article className="station-summary-panel mes-distribution-panel" data-panel="ok-nok-by-station">
          <header><div><p className="station-summary-panel-kicker">Quality by station</p><h3>OK/NOK by Station</h3></div><span className="mes-caption">terminal cohort · stacked</span></header>
          <StationSummaryChart
            ariaLabel="OK/NOK by Station"
            series={okNokSeries}
            xAxisLabel="Station"
            yAxisLabel="Units"
            unit="units"
            variant="stacked-bar"
            emptyMessage="No station quality data in this window."
          />
        </article>
        <article className="station-summary-panel mes-distribution-panel" data-panel="nok-code-distribution">
          <header><div><p className="station-summary-panel-kicker">Defect codes</p><h3>NOK Code Distribution</h3></div><span className="mes-caption">new NOK origins</span></header>
          <StationSummaryChart
            ariaLabel="NOK Code Distribution"
            points={(summary.quality?.nokCodeDistribution ?? []).map((item) => ({ label: String(item.code), value: item.count }))}
            xAxisLabel="NOK Code"
            yAxisLabel="NOK units"
            unit="units"
            emptyMessage="No trusted NOK codes in this window."
          />
        </article>
        <article className="station-summary-panel mes-list-panel" data-panel="collector-runtime-status">
          <header><div><p className="station-summary-panel-kicker">Collector</p><h3>Collector Runtime Status</h3></div><span className="mes-caption">runtime authority</span></header>
          {(summary.collectorRuntime ?? []).length ? (
            <div className="mes-runtime-list">
              {summary.collectorRuntime?.map((row) => (
                <div key={row.stationId}>
                  <strong>{row.stationId}</strong>
                  <span>{row.collectorState}</span>
                  <span>{row.plcConnectionState}</span>
                  <small>{row.updatedAt}</small>
                </div>
              ))}
            </div>
          ) : <p className="mes-empty">Collector runtime authority is unavailable.</p>}
        </article>
      </section>

      <section className="station-summary-panel mes-recent-panel" data-panel="recent-trace">
        <header><div><p className="station-summary-panel-kicker">Recent trace</p><h3>Recent Trace Records</h3></div><a href="/trace">Open Trace →</a></header>
        <div className="station-summary-table-scroll">
          <table className="accepted-events-table">
            <thead><tr><th>Unit / DMC</th><th>Terminal Result</th><th>Completed At</th><th>Defect Origin</th><th>Code</th><th>Trace</th></tr></thead>
            <tbody>
              {(summary.recentCompletedUnits ?? []).map((unit) => (
                <tr key={`${unit.unitId}-${unit.completedAt}`}>
                  <td><code>{unit.unitId}</code><small className="mes-table-subvalue">{unit.labelCode ?? "—"}</small></td>
                  <td>{unit.result}</td>
                  <td>{unit.completedAt}</td>
                  <td>{unit.defectOriginStation ?? "—"}</td>
                  <td>{unit.defectCode ?? "—"}</td>
                  <td><a href={`/trace?q=${encodeURIComponent(unit.unitId)}`}>View</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
