import type { ProcessMetricsPanelViewModel } from "../../lib/stationSummary/viewModel";

type Props = {
  panel: ProcessMetricsPanelViewModel;
};

export function ProcessMetricMatrix({ panel }: Props) {
  return (
    <section className="station-summary-panel station-summary-process-panel" aria-label={panel.sourceLabel}>
      <header className="station-summary-panel-heading">
        <div>
          <p className="station-summary-panel-kicker">Process metrics</p>
          <h2>Bounded authority matrix</h2>
        </div>
        <div className="station-summary-source-status">
          <span>{panel.sourceLabel}</span>
          <strong className="station-summary-status-badge" data-status={panel.status}>{panel.status}</strong>
        </div>
      </header>
      <dl className="station-summary-process-context">
        <div>
          <dt>Scope</dt>
          <dd>{panel.scopeLabel}</dd>
        </div>
        <div>
          <dt>Window</dt>
          <dd>{panel.windowLabel}</dd>
        </div>
        <div>
          <dt>Authority</dt>
          <dd>{panel.sourceAuthority}</dd>
        </div>
        <div>
          <dt>Reason</dt>
          <dd>{panel.reason}</dd>
        </div>
      </dl>
      {panel.message ? <p className="station-summary-panel-alert" role="alert">{panel.message}</p> : null}
      {panel.metrics.length > 0 ? (
        <div className="station-summary-table-scroll">
          <table className="accepted-events-table station-summary-metrics-table">
            <caption>Trusted Process Metrics fixed matrix</caption>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Unit</th>
                <th>Counting unit</th>
                <th>Status</th>
                <th>Reason</th>
                <th>Source</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {panel.metrics.map((metric) => (
                <tr key={metric.name}>
                  <td>{metric.name}</td>
                  <td>{metric.unit}</td>
                  <td>{metric.countingUnit}</td>
                  <td><span className="station-summary-status-badge station-summary-status-badge-small" data-status={metric.status}>{metric.status}</span></td>
                  <td>{metric.reason}</td>
                  <td>{metric.source}</td>
                  <td>{metric.valueText}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
