import type { ProcessMetricsPanelViewModel } from "../../lib/stationSummary/viewModel";

type Props = {
  panel: ProcessMetricsPanelViewModel;
};

export function ProcessMetricMatrix({ panel }: Props) {
  return (
    <section className="evidence-panel" aria-label={panel.sourceLabel}>
      <h2>Process Metrics fixed matrix</h2>
      <p>Source: {panel.sourceLabel}</p>
      <p>Status: {panel.status}</p>
      <p>Scope: {panel.scopeLabel}</p>
      <p>Window: {panel.windowLabel}</p>
      <p>Reason: {panel.reason}</p>
      {panel.message ? <p role="alert">{panel.message}</p> : null}
      {panel.metrics.length > 0 ? (
        <table className="accepted-events-table">
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
                <td>{metric.status}</td>
                <td>{metric.reason}</td>
                <td>{metric.source}</td>
                <td>{metric.valueText}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </section>
  );
}
