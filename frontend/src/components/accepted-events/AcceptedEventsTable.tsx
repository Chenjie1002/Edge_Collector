import type { AcceptedEventRow } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  rows: AcceptedEventRow[];
  selectedFactKey?: string;
};

export function AcceptedEventsTable({ rows, selectedFactKey }: Props) {
  if (rows.length === 0) return null;

  return (
    <table className="accepted-events-table">
      <caption>Accepted station-event facts</caption>
      <thead>
        <tr>
          <th>Station</th>
          <th>Type</th>
          <th>Event</th>
          <th>Result</th>
          <th>Event time</th>
          <th>Accepted fact timestamp</th>
          <th>Unit</th>
          <th>DMC</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.factKey} className={row.factKey === selectedFactKey ? "is-selected" : undefined}>
            <td>
              <strong>{row.stationId}</strong>
            </td>
            <td>{row.stationType}</td>
            <td>{row.eventType}</td>
            <td>{row.productionResult}</td>
            <td>
              <span>{row.eventTs.label}</span>
              <strong>{row.eventTs.value}</strong>
            </td>
            <td>
              <span>{row.acceptedAt.label}</span>
              <strong>{row.acceptedAt.value}</strong>
            </td>
            <td>{row.unitId ?? "unknown"}</td>
            <td>{row.dmc ?? "unknown"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
