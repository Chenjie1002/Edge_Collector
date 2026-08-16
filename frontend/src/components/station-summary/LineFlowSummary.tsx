import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";

function reconciliationMessage(summary: LineSummary): string {
  if (summary.cohort.errors.length === 0) return "The completed cohort could not be reconciled across the configured route.";
  return summary.cohort.errors.join(" ");
}

export function LineFlowSummary({ summary }: { summary: LineSummary }) {
  const status = summary.cohort.reconciliationStatus;
  return (
    <section className="station-summary-panel line-flow-summary" aria-label="Whole-line station summary">
      <header className="station-summary-panel-heading line-flow-summary-heading">
        <div>
          <p className="station-summary-panel-kicker">Completed production flow</p>
          <h2>{summary.scope.lineId}</h2>
        </div>
        <div className="line-flow-summary-status" aria-label="Route reconciliation status">
          <span>Completed cohort at terminal: {summary.cohort.unitCount}</span>
          <strong data-status={status}>Route conservation: {status}</strong>
        </div>
      </header>

      {status === "FAIL" ? (
        <p className="station-summary-panel-alert" role="alert">
          Flow reconciliation failed: {reconciliationMessage(summary)}
        </p>
      ) : null}

      <div className="station-summary-table-scroll">
        <table className="accepted-events-table station-summary-flow-table">
          <caption>
            One terminal-completed cohort across the configured route. NOK includes inherited upstream NOK; Skipped is process status SKIPPED.
          </caption>
          <thead>
            <tr>
              <th scope="col">Station</th>
              <th scope="col">Total</th>
              <th scope="col">OK</th>
              <th scope="col">NOK</th>
              <th scope="col">New NOK</th>
              <th scope="col">Skipped</th>
            </tr>
          </thead>
          <tbody>
            {summary.stations.map((station) => (
              <tr key={station.stationId} data-reconciliation-status={station.reconciliationStatus}>
                <th scope="row">{station.stationId}</th>
                <td>{station.total}</td>
                <td>{station.ok}</td>
                <td>{station.nok}</td>
                <td>{station.newNok}</td>
                <td>{station.skipped}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="line-flow-summary-footnote">Every station is checked against the same terminal-completed cohort: OK + NOK and PROCESSED + SKIPPED must each equal Total.</p>
    </section>
  );
}
