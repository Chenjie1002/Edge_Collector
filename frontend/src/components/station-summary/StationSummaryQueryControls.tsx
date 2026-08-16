"use client";

import { useState } from "react";
import type { LineSummaryQuery } from "../../lib/stationSummary/lineSummaryQuery";
import type { TrustedScopeCatalog } from "../../lib/stationSummary/scopeCatalog";
import {
  localMinuteToOffsetIso,
  offsetIsoToLocalMinute,
  quickRangeAt,
  validateLocalWindow,
  type LocalWindow,
} from "../../lib/stationSummary/timeWindow";

type Props = {
  catalog?: TrustedScopeCatalog | null;
  query?: LineSummaryQuery;
  defaultWindow?: LocalWindow;
};

function initialWindow(query: LineSummaryQuery | undefined, defaultWindow: LocalWindow | undefined): LocalWindow {
  if (query) {
    try {
      return {
        startLocal: offsetIsoToLocalMinute(query.startTime),
        endLocal: offsetIsoToLocalMinute(query.endTime),
      };
    } catch {
      // The server validates submitted queries; malformed values never become options.
    }
  }
  return defaultWindow ?? quickRangeAt(new Date(), 8);
}

export function StationSummaryQueryControls({ catalog = null, query, defaultWindow }: Props) {
  const lines = catalog?.lines ?? [];
  const requestedLine = query ? lines.find((line) => line.lineId === query.lineId) : undefined;
  const firstLine = requestedLine ?? lines[0];
  const requestedStation = query?.stationId && firstLine ? firstLine.stations.find((station) => station.stationId === query.stationId) : undefined;
  const defaults = initialWindow(query, defaultWindow);
  const [lineId, setLineId] = useState(firstLine?.lineId ?? "");
  const [stationId, setStationId] = useState(requestedStation?.stationId ?? "");
  const [startLocal, setStartLocal] = useState(defaults.startLocal);
  const [endLocal, setEndLocal] = useState(defaults.endLocal);

  const selectedLine = lines.find((line) => line.lineId === lineId);
  const stations = selectedLine?.stations ?? [];
  const windowValidation = validateLocalWindow(startLocal, endLocal);
  const canApply = Boolean(catalog && selectedLine && windowValidation.ok);
  const startTime = windowValidation.ok ? localMinuteToOffsetIso(startLocal, "+08:00") : "";
  const endTime = windowValidation.ok ? localMinuteToOffsetIso(endLocal, "+08:00") : "";

  function chooseLine(nextLineId: string) {
    setLineId(nextLineId);
    setStationId("");
  }

  function chooseQuickRange(hours: 1 | 8 | 24) {
    const nextWindow = quickRangeAt(new Date(), hours);
    setStartLocal(nextWindow.startLocal);
    setEndLocal(nextWindow.endLocal);
  }

  return (
    <form
      className="query-controls station-summary-query-controls"
      action="/station-summary"
      method="get"
      aria-label="Station summary scope query"
    >
      <div className="station-summary-scope-heading">
        <h2>Scope</h2>
        <p>Select a trusted line and bounded production window. Station detail is optional.</p>
      </div>
      <div className="station-summary-scope-fields">
        <label htmlFor="station-summary-line-id">
          Line
          <select
            id="station-summary-line-id"
            name="line_id"
            value={lineId}
            onChange={(event) => chooseLine(event.target.value)}
            disabled={!catalog || lines.length === 0}
            required
          >
            <option value="" disabled>
              {catalog ? "Select line" : "Unavailable"}
            </option>
            {lines.map((line) => (
              <option key={line.lineId} value={line.lineId}>
                {line.name} ({line.lineId})
              </option>
            ))}
          </select>
        </label>
        <label htmlFor="station-summary-station-id">
          Station detail (optional)
          <select
            id="station-summary-station-id"
            name="station_id"
            value={stationId}
            onChange={(event) => setStationId(event.target.value)}
            disabled={!selectedLine || stations.length === 0}
          >
            <option value="">
              {selectedLine ? "Whole line (default)" : "Unavailable"}
            </option>
            {stations.map((station) => (
              <option key={station.stationId} value={station.stationId}>
                {station.name} ({station.stationId})
              </option>
            ))}
          </select>
        </label>
        <div className="station-summary-scope-time-fields">
          <label htmlFor="station-summary-start-time">
            Start time
            <input
              id="station-summary-start-time"
              type="datetime-local"
              value={startLocal}
              onChange={(event) => setStartLocal(event.target.value)}
              required
              step={60}
              disabled={!catalog}
            />
          </label>
          <label htmlFor="station-summary-end-time">
            End time
            <input
              id="station-summary-end-time"
              type="datetime-local"
              value={endLocal}
              onChange={(event) => setEndLocal(event.target.value)}
              required
              step={60}
              disabled={!catalog}
            />
          </label>
        </div>
        <div className="station-summary-scope-presets" aria-label="Quick ranges">
          <span className="station-summary-scope-presets-label">Quick range</span>
          <div className="station-summary-scope-preset-buttons">
            <button type="button" onClick={() => chooseQuickRange(1)} disabled={!catalog}>
              Last 1h
            </button>
            <button type="button" onClick={() => chooseQuickRange(8)} disabled={!catalog}>
              Last 8h
            </button>
            <button type="button" onClick={() => chooseQuickRange(24)} disabled={!catalog}>
              Last 24h
            </button>
          </div>
          <span className="station-summary-scope-timezone">Plant time: Asia/Shanghai (UTC+08:00)</span>
          {!windowValidation.ok ? <span className="station-summary-scope-validation">{windowValidation.reason}</span> : null}
        </div>
        <input type="hidden" name="start_time" value={startTime} disabled={!canApply} readOnly />
        <input type="hidden" name="end_time" value={endTime} disabled={!canApply} readOnly />
        <button className="station-summary-scope-apply" type="submit" disabled={!canApply}>
          Apply
        </button>
      </div>
    </form>
  );
}
