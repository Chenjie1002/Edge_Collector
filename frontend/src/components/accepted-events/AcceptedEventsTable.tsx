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
          <tr
            key={row.factKey}
            className={row.factKey === selectedFactKey ? "is-selected" : undefined}
            data-fact-key={row.factKey}
          >
            <td>
              <strong>{row.stationId.text}</strong>
            </td>
            <td>{row.stationType.text}</td>
            <td>{row.eventType.text}</td>
            <td>{row.productionResult.text}</td>
            <td>
              <span>{row.eventTs.label}</span>
              <strong>{row.eventTs.text}</strong>
            </td>
            <td>
              <span>{row.acceptedAt.label}</span>
              <strong>{row.acceptedAt.text}</strong>
            </td>
            <td>{row.unitId.text}</td>
            <td>{row.dmc.text}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
