import { StationSummaryQueryControls } from "../../components/station-summary/StationSummaryQueryControls";
import { StationSummaryLiveDashboard } from "../../components/station-summary/StationSummaryLiveDashboard";
import { StationSummaryStateMessage, type StationSummaryPageState } from "../../components/station-summary/StationSummaryStates";
import { resolveTrustedAcceptedEventsApiOrigin, type TrustedAcceptedEventsApiOrigin } from "../../lib/acceptedStationEvents/apiOrigin";
import { fetchStationSummary } from "../../lib/stationSummary/apiClient";
import { fetchLineSummary } from "../../lib/stationSummary/lineSummaryApi";
import { validateLineSummaryQuery, type LineSummaryMode, type LineSummaryQuery } from "../../lib/stationSummary/lineSummaryQuery";
import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";
import { validateStationSummaryQuery, type StationSummaryQuery } from "../../lib/stationSummary/query";
import { fetchTrustedScopeCatalog, topologyMatchesCatalog, type TrustedScopeCatalog } from "../../lib/stationSummary/scopeCatalog";
import { localMinuteToOffsetIso, quickRangeAt } from "../../lib/stationSummary/timeWindow";
import { toStationSummaryViewModel, type StationSummaryViewModel } from "../../lib/stationSummary/viewModel";

type SearchParams = Record<string, string | string[] | undefined>;
type ProductView = "line" | "station";

type StationDetailState =
  | { kind: "ready"; viewModel: StationSummaryViewModel }
  | { kind: "unavailable"; message: string };

type PageViewState =
  | StationSummaryPageState
  | {
      kind: "ready";
      view: ProductView;
      query: LineSummaryQuery;
      summary: LineSummary;
      stationDetail?: StationDetailState;
    };

const QUERY_KEYS = ["view", "mode", "line_id", "station_id", "start_time", "end_time"] as const;
const LIVE_HORIZON_HOURS = 8;

export const dynamic = "force-dynamic";

function singleParam(params: SearchParams, key: string): { ok: true; value: string | undefined } | { ok: false; reason: string } {
  const value = params[key];
  if (Array.isArray(value)) return { ok: false, reason: `${key} must be provided once` };
  return { ok: true, value };
}

function rollingLineQuery(lineId: string, stationId?: string): LineSummaryQuery {
  const window = quickRangeAt(new Date(), LIVE_HORIZON_HOURS);
  return {
    lineId,
    mode: "LIVE",
    startTime: localMinuteToOffsetIso(window.startLocal, "+08:00"),
    endTime: localMinuteToOffsetIso(window.endLocal, "+08:00"),
    ...(stationId ? { stationId } : {}),
  };
}

function queryFromSearchParams(params: SearchParams): { ok: true; query?: LineSummaryQuery; view: ProductView } | { ok: false; reason: string } {
  const keys = Object.keys(params);
  if (keys.some((key) => !QUERY_KEYS.includes(key as (typeof QUERY_KEYS)[number]))) {
    return { ok: false, reason: "Only view, mode, line_id, optional station_id, start_time, and end_time are supported" };
  }
  const rawView = singleParam(params, "view");
  if (!rawView.ok) return rawView;
  const view = rawView.value ?? "line";
  if (view !== "line" && view !== "station") return { ok: false, reason: "view must be line or station" };
  if (keys.length === 0 || (keys.length === 1 && keys[0] === "view")) return { ok: true, view };

  const line = singleParam(params, "line_id");
  const station = singleParam(params, "station_id");
  const mode = singleParam(params, "mode");
  const start = singleParam(params, "start_time");
  const end = singleParam(params, "end_time");
  if (!line.ok) return line;
  if (!station.ok) return station;
  if (!mode.ok) return mode;
  if (!start.ok) return start;
  if (!end.ok) return end;
  const hasStart = Boolean(start.value);
  const hasEnd = Boolean(end.value);
  if (hasStart !== hasEnd) return { ok: false, reason: "start_time and end_time must be submitted together" };

  const requestedMode = mode.value;
  const effectiveMode: LineSummaryMode | "INVALID" = requestedMode
    ? requestedMode === "LIVE" || requestedMode === "FIXED"
      ? requestedMode
      : "INVALID"
    : hasStart
      ? "FIXED"
      : "LIVE";
  if (effectiveMode === "INVALID") return { ok: false, reason: "mode must be LIVE or FIXED" };
  if (effectiveMode === "LIVE" && (hasStart || hasEnd)) {
    return { ok: false, reason: "LIVE mode cannot include a fixed start_time or end_time" };
  }
  if (effectiveMode === "LIVE") {
    return { ok: true, query: rollingLineQuery(line.value ?? "", station.value ?? undefined), view };
  }
  const validation = validateLineSummaryQuery({
    lineId: line.value ?? "",
    stationId: station.value ?? undefined,
    startTime: start.value ?? "",
    endTime: end.value ?? "",
    mode: "FIXED",
  });
  return validation.ok ? { ok: true, query: validation.query, view } : { ok: false, reason: validation.reason };
}

function stationDetailQuery(query: LineSummaryQuery): StationSummaryQuery | undefined {
  if (!query.stationId) return undefined;
  const validation = validateStationSummaryQuery({
    lineId: query.lineId,
    stationId: query.stationId,
    startTime: query.startTime,
    endTime: query.endTime,
  });
  return validation.ok ? validation.query : undefined;
}

function tabHref(view: ProductView, query: LineSummaryQuery, summary: LineSummary): string {
  const params = new URLSearchParams({
    view,
    mode: query.mode ?? "FIXED",
    line_id: query.lineId,
  });
  if ((query.mode ?? "FIXED") === "FIXED") {
    params.set("start_time", query.startTime);
    params.set("end_time", query.endTime);
  }
  const stationId = query.stationId ?? summary.topology.entryStationId;
  if (stationId) params.set("station_id", stationId);
  return `/station-summary?${params.toString()}`;
}

export function StationSummaryPageView({ state, catalog = null, trustedApiOrigin }: { state: PageViewState; catalog?: TrustedScopeCatalog | null; trustedApiOrigin?: TrustedAcceptedEventsApiOrigin }) {
  const query = state.kind === "ready" ? state.query : undefined;
  const view = state.kind === "ready" ? state.view : "line";
  return (
    <main className="dashboard-shell station-summary-shell">
      <header className="station-summary-header">
        <div className="station-summary-header-copy">
          <p className="station-summary-eyebrow">Production overview · Trusted read-only</p>
          <h1>Station Summary</h1>
          <p>MES production surface for the whole selected line using terminal-completed accounting, with a separate station-local process detail view. No fabricated KPI fallback.</p>
        </div>
        <div className="station-summary-header-policy" aria-label="Station summary data policy">
          <span>Terminal cohort</span>
          <span>Result / process status separated</span>
        </div>
      </header>
      <StationSummaryQueryControls catalog={catalog} query={query} view={view} defaultWindow={query ? undefined : quickRangeAt(new Date(), 8)} />
      {state.kind !== "ready" ? (
        <StationSummaryStateMessage state={state} />
      ) : (
        <StationSummaryLiveDashboard
          view={state.view}
          query={state.query}
          summary={state.summary}
          trustedApiOrigin={trustedApiOrigin}
          trustedScopeLine={catalog?.lines.find((line) => line.lineId === state.query.lineId)}
          lineTabHref={tabHref("line", state.query, state.summary)}
          stationTabHref={tabHref("station", state.query, state.summary)}
          stationDetail={state.stationDetail}
          stationDetailQuery={state.view === "station" ? stationDetailQuery(state.query) : undefined}
        />
      )}
    </main>
  );
}

export default async function StationSummaryPage({ searchParams }: { searchParams?: SearchParams | Promise<SearchParams> }) {
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const queryResult = queryFromSearchParams(resolvedSearchParams);
  if (!queryResult.ok) return <StationSummaryPageView state={{ kind: "invalid-query", message: queryResult.reason }} />;

  const resolution = resolveTrustedAcceptedEventsApiOrigin();
  if (!resolution.ok) {
    return <StationSummaryPageView state={{ kind: "error", title: "Data source not configured", message: "The trusted API is not configured. No fallback or fabricated production values are shown." }} />;
  }

  const catalogResult = await fetchTrustedScopeCatalog(resolution.origin);
  if (!catalogResult.ok) {
    return <StationSummaryPageView catalog={null} state={{ kind: "unavailable", title: "Scope catalog unavailable", message: "The trusted scope catalog could not be loaded. No URL-provided options or production values are shown." }} />;
  }

  const submittedQuery = queryResult.query ?? (catalogResult.catalog.lines[0] ? rollingLineQuery(catalogResult.catalog.lines[0].lineId) : undefined);
  if (!submittedQuery) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "idle", title: "Select line and apply", message: "Choose a trusted Line before requesting production data." }} />;
  }

  const selectedLine = catalogResult.catalog.lines.find((line) => line.lineId === submittedQuery.lineId);
  if (!selectedLine) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "invalid-query", message: "line_id must match the trusted scope catalog" }} />;
  }

  const effectiveQuery: LineSummaryQuery = queryResult.view === "station" && !submittedQuery.stationId
    ? { ...submittedQuery, stationId: selectedLine.stations[0]?.stationId }
    : submittedQuery;
  const selectedStation = effectiveQuery.stationId && selectedLine.stations.find((station) => station.stationId === effectiveQuery.stationId);
  if (effectiveQuery.stationId && !selectedStation) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "invalid-query", message: "station_id must match the trusted scope catalog" }} />;
  }

  const result = await fetchLineSummary(effectiveQuery, resolution.origin);
  if (!result.ok) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: result.kind === "invalid-query" ? "invalid-query" : result.kind, message: result.message }} />;
  }
  if (!topologyMatchesCatalog(result.summary, selectedLine)) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "malformed", message: "The line summary topology does not match the trusted scope catalog." }} />;
  }

  let stationDetail: StationDetailState | undefined;
  if (queryResult.view === "station") {
    const detailQuery = stationDetailQuery(effectiveQuery);
    if (detailQuery) {
      const detailResult = await fetchStationSummary(detailQuery, resolution.origin);
      stationDetail = detailResult.ok
        ? { kind: "ready", viewModel: toStationSummaryViewModel(detailQuery, detailResult) }
        : { kind: "unavailable", message: detailResult.message };
    }
  }

  return <StationSummaryPageView catalog={catalogResult.catalog} trustedApiOrigin={resolution.origin} state={{ kind: "ready", view: queryResult.view, query: effectiveQuery, summary: result.summary, stationDetail }} />;
}
