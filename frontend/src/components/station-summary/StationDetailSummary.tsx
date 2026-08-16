import type { LineSummary, LineSummaryStation } from "../../lib/stationSummary/lineSummarySchema";
import { StationSummaryChart } from "./StationSummaryChart";

function rate(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${(value * 100).toFixed(1)}%`;
}

function seconds(value: number | null | undefined): string {
  return value === null || value === undefined ? "—" : `${value.toFixed(2)} s`;
}

export function StationDetailSummary({ summary, stationId }: { summary: LineSummary; stationId: string }) {
  const station = summary.stations.find((candidate) => candidate.stationId === stationId);
  if (!station) return <p className="station-summary-panel-alert" role="alert">Selected station is not present in the trusted route.</p>;

  const runtime = summary.collectorRuntime?.find((candidate) => candidate.stationId === stationId);
  const cycleTrend = (summary.trends?.cycleTime ?? []).filter((point) => point.stationId === stationId);
  const activity = station.activityTrend ?? [];
  const localNokRate = station.localNokRate ?? (station.processed > 0 ? station.newNok / station.processed : null);

  return (
    <div className="mes-product-stack" aria-label={`${stationId} station-local detail`}>
      <section className="station-summary-panel mes-station-identity">
        <div><p className="station-summary-panel-kicker">Station-local production</p><h2>{stationId}</h2><p className="mes-muted-copy">Only station-local metrics are shown in this tab.</p></div>
        <div className="mes-runtime-strip">
          <span><small>Station runtime</small><strong>{runtime?.stationStatus ?? "UNAVAILABLE"}</strong></span>
          <span><small>Collector</small><strong>{runtime?.collectorState ?? "UNAVAILABLE"}</strong></span>
          <span><small>PLC connection</small><strong>{runtime?.plcConnectionState ?? "UNAVAILABLE"}</strong></span>
        </div>
      </section>

      <section className="mes-kpi-grid mes-station-kpis" aria-label={`${stationId} station KPIs`}>
        <div><span>Processed</span><strong>{station.processed}</strong><small>process_status = PROCESSED</small></div>
        <div><span>Skipped</span><strong>{station.skipped}</strong><small>process_status = SKIPPED</small></div>
        <div><span>New NOK</span><strong>{station.newNok}</strong><small>first NOK at this station</small></div>
        <div><span>Local NOK rate</span><strong>{rate(localNokRate)}</strong><small>New NOK / Processed</small></div>
        <div><span>Station Avg CT</span><strong>{seconds(station.averageCycleSeconds)}</strong><small>processed cycle_event samples</small></div>
        <div><span>Observed records</span><strong>{station.evidenceCount}</strong><small>trusted cohort station evidence</small></div>
      </section>

      <section className="mes-chart-grid">
        <article className="station-summary-panel mes-chart-panel">
          <header><div><p className="station-summary-panel-kicker">Station process/event trend</p><h3>Processed vs Skipped</h3></div><span className="mes-caption">New NOK retained in bucket metadata</span></header>
          <div className="mes-station-chart-pair">
            <StationSummaryChart
              ariaLabel={`${station.stationId} processed event trend`}
              points={activity.map((point) => ({ label: point.bucketStart, value: point.processed }))}
              xAxisLabel="Time"
              yAxisLabel="Processed station events"
              unit="events"
              emptyMessage="No processed station events in this window."
              variant="line"
            />
            <StationSummaryChart
              ariaLabel={`${station.stationId} skipped event trend`}
              points={activity.map((point) => ({ label: point.bucketStart, value: point.skipped }))}
              xAxisLabel="Time"
              yAxisLabel="Skipped station events"
              unit="events"
              emptyMessage="No skipped station events in this window."
              variant="line"
            />
          </div>
        </article>
        <article className="station-summary-panel mes-chart-panel">
          <header><div><p className="station-summary-panel-kicker">Station CT trend</p><h3>Observed cycle time</h3></div><strong>{seconds(station.averageCycleSeconds)}</strong></header>
          <StationSummaryChart
            ariaLabel={`${station.stationId} observed cycle time trend`}
            points={cycleTrend.map((point) => ({ label: point.bucketStart, value: point.averageCycleSeconds }))}
            xAxisLabel="Time"
            yAxisLabel="Cycle time"
            unit="s"
            emptyMessage="No processed CT samples in this window."
            variant="line"
          />
        </article>
      </section>

      <section className="mes-chart-grid">
        <article className="station-summary-panel mes-list-panel">
          <header><div><p className="station-summary-panel-kicker">Station NOK code</p><h3>Local defect origin codes</h3></div></header>
          <StationSummaryChart
            ariaLabel={`${station.stationId} NOK code distribution`}
            points={(station.nokCodes ?? []).map((item) => ({ label: String(item.code), value: item.count }))}
            xAxisLabel="NOK Code"
            yAxisLabel="New NOK unit count"
            unit="units"
            emptyMessage="No new local NOK code in this window."
          />
        </article>
        <article className="station-summary-panel mes-list-panel">
          <header><div><p className="station-summary-panel-kicker">Station reconciliation</p><h3>Local evidence quality</h3></div><strong data-status={station.reconciliationStatus}>{station.reconciliationStatus}</strong></header>
          <dl className="mes-compact-dl"><dt>Missing</dt><dd>{station.missingUnitCount}</dd><dt>Duplicate</dt><dd>{station.duplicateUnitCount}</dd><dt>Invalid</dt><dd>{station.invalidRecordCount}</dd></dl>
        </article>
      </section>

      <section className="station-summary-panel mes-recent-panel">
        <header><div><p className="station-summary-panel-kicker">Station recent records</p><h3>{stationId} · selected cohort</h3></div></header>
        <div className="station-summary-table-scroll">
          <table className="accepted-events-table">
            <thead><tr><th>Unit</th><th>Result</th><th>Process</th><th>Cycle</th><th>Completed At</th><th>Defect</th></tr></thead>
            <tbody>{(station.recentRecords ?? []).map((row) => <tr key={`${row.unitId}-${row.completedAt}`}><td><code>{row.unitId}</code></td><td>{row.result}</td><td>{row.processStatus}</td><td>{seconds(row.cycleSeconds)}</td><td>{row.completedAt}</td><td>{row.defectCode ?? "—"}</td></tr>)}</tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
