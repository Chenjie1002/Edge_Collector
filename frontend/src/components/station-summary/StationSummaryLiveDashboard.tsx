"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { TrustedAcceptedEventsApiOrigin } from "../../lib/acceptedStationEvents/apiOrigin";
import { fetchStationSummary } from "../../lib/stationSummary/apiClient";
import { fetchLineSummary } from "../../lib/stationSummary/lineSummaryApi";
import type { LineSummaryMode, LineSummaryQuery } from "../../lib/stationSummary/lineSummaryQuery";
import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";
import { quickRangeAt, localMinuteToOffsetIso } from "../../lib/stationSummary/timeWindow";
import type { StationSummaryQuery } from "../../lib/stationSummary/query";
import { topologyMatchesCatalog, type ScopeLine } from "../../lib/stationSummary/scopeCatalog";
import { toStationSummaryViewModel, type StationSummaryViewModel } from "../../lib/stationSummary/viewModel";
import { LineProductSummary } from "./LineProductSummary";
import { ProcessMetricMatrix } from "./ProcessMetricMatrix";
import { StationDetailSummary } from "./StationDetailSummary";
import { StationSummaryCards } from "./StationSummaryCards";
import { STATION_SUMMARY_REFRESH_EVENT } from "./StationSummaryQueryControls";

type StationDetailState =
  | { kind: "ready"; viewModel: StationSummaryViewModel }
  | { kind: "unavailable"; message: string };

type Props = Readonly<{
  view: "line" | "station";
  query: LineSummaryQuery;
  summary: LineSummary;
  trustedApiOrigin?: TrustedAcceptedEventsApiOrigin;
  trustedScopeLine?: ScopeLine;
  lineTabHref: string;
  stationTabHref: string;
  stationDetail?: StationDetailState;
  stationDetailQuery?: StationSummaryQuery;
}>;

type RefreshState =
  | { kind: "current" }
  | { kind: "refreshing" }
  | { kind: "stale"; message: string };

const LIVE_HORIZON_HOURS = 8;

function nextLiveQuery(query: LineSummaryQuery): LineSummaryQuery {
  const window = quickRangeAt(new Date(), LIVE_HORIZON_HOURS);
  return {
    ...query,
    mode: "LIVE" as LineSummaryMode,
    startTime: localMinuteToOffsetIso(window.startLocal, "+08:00"),
    endTime: localMinuteToOffsetIso(window.endLocal, "+08:00"),
  };
}

function stationQueryFor(query: StationSummaryQuery | undefined, lineQuery: LineSummaryQuery): StationSummaryQuery | undefined {
  if (!query || !lineQuery.stationId) return undefined;
  return {
    ...query,
    lineId: lineQuery.lineId,
    startTime: lineQuery.startTime,
    endTime: lineQuery.endTime,
  };
}

export function StationSummaryLiveDashboard({
  view,
  query,
  summary: initialSummary,
  trustedApiOrigin,
  trustedScopeLine,
  lineTabHref,
  stationTabHref,
  stationDetail: initialStationDetail,
  stationDetailQuery,
}: Props) {
  const [summary, setSummary] = useState(initialSummary);
  const [activeQuery, setActiveQuery] = useState(query);
  const [stationDetail, setStationDetail] = useState(initialStationDetail);
  const [refreshState, setRefreshState] = useState<RefreshState>({ kind: "current" });
  const inFlight = useRef(false);
  const mounted = useRef(true);

  useEffect(() => () => {
    mounted.current = false;
  }, []);

  const refresh = useCallback(async () => {
    if (query.mode !== "LIVE" || inFlight.current) return;
    if (!trustedApiOrigin) {
      setRefreshState({ kind: "stale", message: "Live refresh is unavailable; showing the last trusted data." });
      return;
    }

    inFlight.current = true;
    setRefreshState({ kind: "refreshing" });
    const nextQuery = nextLiveQuery(query);
    const nextStationQuery = stationQueryFor(stationDetailQuery, nextQuery);

    try {
      const [lineResult, stationResult] = await Promise.all([
        fetchLineSummary(nextQuery, trustedApiOrigin),
        nextStationQuery ? fetchStationSummary(nextStationQuery, trustedApiOrigin) : Promise.resolve(undefined),
      ]);

      if (!mounted.current) return;
      if (!lineResult.ok) {
        setRefreshState({ kind: "stale", message: lineResult.message });
        return;
      }
      if (stationResult && !stationResult.ok) {
        setRefreshState({ kind: "stale", message: stationResult.message });
        return;
      }
      if (!trustedScopeLine || !topologyMatchesCatalog(lineResult.summary, trustedScopeLine)) {
        setRefreshState({ kind: "stale", message: "Live refresh topology does not match the trusted scope; showing the last trusted data." });
        return;
      }

      setSummary(lineResult.summary);
      setActiveQuery(nextQuery);
      if (nextStationQuery && stationResult?.ok) {
        setStationDetail({ kind: "ready", viewModel: toStationSummaryViewModel(nextStationQuery, stationResult) });
      }
      setRefreshState({ kind: "current" });
    } catch {
      if (mounted.current) setRefreshState({ kind: "stale", message: "Live refresh failed; showing the last trusted data." });
    } finally {
      inFlight.current = false;
    }
  }, [query, stationDetailQuery, trustedApiOrigin, trustedScopeLine]);

  useEffect(() => {
    if (query.mode !== "LIVE") return undefined;
    const onRefreshRequest = () => {
      void refresh();
    };
    window.addEventListener(STATION_SUMMARY_REFRESH_EVENT, onRefreshRequest);
    return () => window.removeEventListener(STATION_SUMMARY_REFRESH_EVENT, onRefreshRequest);
  }, [query.mode, refresh]);

  const live = activeQuery.mode === "LIVE";
  const refreshMessage = refreshState.kind === "stale"
    ? `LIVE data stale · ${refreshState.message}`
    : refreshState.kind === "refreshing"
      ? "LIVE data refreshing…"
      : "LIVE data current";

  return (
    <section className="station-summary-results station-summary-live-region" data-region="station-summary-data" data-refresh-state={refreshState.kind} aria-label="Station summary results">
      {live ? (
        <div className={`station-summary-live-status station-summary-live-status-${refreshState.kind}`} role={refreshState.kind === "stale" ? "alert" : "status"} aria-live="polite">
          {refreshMessage}
        </div>
      ) : null}
      <nav className="mes-summary-tabs" aria-label="Production summary views">
        <a href={lineTabHref} aria-current={view === "line" ? "page" : undefined}>Line Summary</a>
        <a href={stationTabHref} aria-current={view === "station" ? "page" : undefined}>Station Detail</a>
      </nav>
      <header className="station-summary-results-heading">
        <div>
          <p className="station-summary-results-kicker">{view === "line" ? "Selected line" : "Selected station"}</p>
          <h2>{view === "line" ? activeQuery.lineId : "Station Detail"}</h2>
        </div>
        <div className="station-summary-window-state" data-mode={activeQuery.mode ?? "FIXED"}>
          <strong>{live ? "LIVE · Rolling 8h · refresh 10s" : "FIXED WINDOW"}</strong>
          <span>{activeQuery.startTime} → {activeQuery.endTime}</span>
        </div>
      </header>

      {view === "line" ? (
        <LineProductSummary summary={summary} />
      ) : activeQuery.stationId ? (
        <>
          <StationDetailSummary summary={summary} stationId={activeQuery.stationId} />
          <details className="station-summary-diagnostics-detail mes-diagnostics-block">
            <summary>Data diagnostics</summary>
            {stationDetail?.kind === "ready" ? (
              <div className="station-summary-secondary-detail-content">
                <StationSummaryCards quality={stationDetail.viewModel.quality} />
                <ProcessMetricMatrix panel={stationDetail.viewModel.processMetrics} />
              </div>
            ) : (
              <p className="station-summary-panel-alert" role="alert">{stationDetail?.message ?? "Accepted Events diagnostics are unavailable."}</p>
            )}
          </details>
        </>
      ) : null}
    </section>
  );
}
