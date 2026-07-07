"use client";

import { useState } from "react";
import { clearCursorForScopeChange, type AcceptedStationEventsQuery } from "../../lib/acceptedStationEvents/query";

type Props = {
  query: AcceptedStationEventsQuery;
  onSubmit?: (query: AcceptedStationEventsQuery) => void;
};

const limitChoices = [25, 50, 100, 250, 500];

export function AcceptedEventsQueryControls({ query, onSubmit }: Props) {
  const [draft, setDraft] = useState(query);

  function update<K extends keyof AcceptedStationEventsQuery>(key: K, value: AcceptedStationEventsQuery[K]) {
    setDraft((current) => ({ ...current, [key]: value }));
  }

  return (
    <form
      className="query-controls"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit?.(clearCursorForScopeChange(query, draft));
      }}
    >
      <label>
        Line ID
        <input value={draft.lineId} onChange={(event) => update("lineId", event.target.value)} />
      </label>
      <label>
        Start time
        <input value={draft.startTime} onChange={(event) => update("startTime", event.target.value)} />
      </label>
      <label>
        End time
        <input value={draft.endTime} onChange={(event) => update("endTime", event.target.value)} />
      </label>
      <label>
        Limit
        <select value={draft.limit} onChange={(event) => update("limit", Number(event.target.value))}>
          {limitChoices.map((choice) => (
            <option key={choice} value={choice}>
              {choice}
            </option>
          ))}
        </select>
      </label>
      <button type="submit">Apply query</button>
    </form>
  );
}
