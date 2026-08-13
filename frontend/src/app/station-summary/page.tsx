import { StationSummaryCards } from "../../components/station-summary/StationSummaryCards";
import { ProcessMetricMatrix } from "../../components/station-summary/ProcessMetricMatrix";
import { StationSummaryQueryControls } from "../../components/station-summary/StationSummaryQueryControls";
import { StationSummaryStateMessage, type StationSummaryPageState } from "../../components/station-summary/StationSummaryStates";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../lib/acceptedStationEvents/apiOrigin";
import { fetchStationSummary } from "../../lib/stationSummary/apiClient";
import { validateStationSummaryQuery, type StationSummaryQuery } from "../../lib/stationSummary/query";
import { fetchTrustedScopeCatalog, type TrustedScopeCatalog } from "../../lib/stationSummary/scopeCatalog";
import { quickRangeAt } from "../../lib/stationSummary/timeWindow";
import { toStationSummaryViewModel, type StationSummaryViewModel } from "../../lib/stationSummary/viewModel";

type SearchParams = Record<string, string | string[] | undefined>;

type PageViewState =
  | StationSummaryPageState
  | { kind: "ready"; query: StationSummaryQuery; viewModel: StationSummaryViewModel };

const QUERY_KEYS = ["line_id", "station_id", "start_time", "end_time"] as const;

export const dynamic = "force-dynamic";

function singleParam(params: SearchParams, key: string): { ok: true; value: string | undefined } | { ok: false; reason: string } {
  const value = params[key];
  if (Array.isArray(value)) return { ok: false, reason: `${key} must be provided once` };
  return { ok: true, value };
}

function queryFromSearchParams(params: SearchParams): { ok: true; query?: StationSummaryQuery } | { ok: false; reason: string } {
  const keys = Object.keys(params);
  if (keys.length === 0) return { ok: true };
  if (keys.some((key) => !QUERY_KEYS.includes(key as (typeof QUERY_KEYS)[number]))) {
    return { ok: false, reason: "Only line_id, station_id, start_time, and end_time are supported" };
  }

  const line = singleParam(params, "line_id");
  const station = singleParam(params, "station_id");
  const start = singleParam(params, "start_time");
  const end = singleParam(params, "end_time");
  if (!line.ok) return line;
  if (!station.ok) return station;
  if (!start.ok) return start;
  if (!end.ok) return end;
  const query: StationSummaryQuery = {
    lineId: line.value ?? "",
    stationId: station.value ?? "",
    startTime: start.value ?? "",
    endTime: end.value ?? "",
  };
  const validation = validateStationSummaryQuery(query);
  return validation.ok ? validation : { ok: false, reason: validation.reason };
}

export function StationSummaryPageView({ state, catalog = null }: { state: PageViewState; catalog?: TrustedScopeCatalog | null }) {
  const query = state.kind === "ready" ? state.query : undefined;
  return (
    <main className="dashboard-shell station-summary-shell">
      <header className="station-summary-header">
        <p className="station-summary-eyebrow">Production insight · Read-only</p>
        <h1>Station Summary</h1>
        <p>Trusted production view for one station and time window. Unavailable or unsupported data remains explicit.</p>
      </header>
      <StationSummaryQueryControls catalog={catalog} query={query} defaultWindow={query ? undefined : quickRangeAt(new Date(), 8)} />
      {state.kind !== "ready" ? (
        <StationSummaryStateMessage state={state} />
      ) : (
        <div className="detail-grid">
          <StationSummaryCards quality={state.viewModel.quality} />
          <ProcessMetricMatrix panel={state.viewModel.processMetrics} />
        </div>
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
    return (
      <StationSummaryPageView
        state={{
          kind: "error",
          title: "Data source not configured",
          message: "The trusted API is not configured. No fallback or fabricated production values are shown.",
        }}
      />
    );
  }

  const catalogResult = await fetchTrustedScopeCatalog(resolution.origin);
  if (!catalogResult.ok) {
    return (
      <StationSummaryPageView
        catalog={null}
        state={{
          kind: "unavailable",
          title: "Scope catalog unavailable",
          message: "The trusted scope catalog could not be loaded. No URL-provided options or production values are shown.",
        }}
      />
    );
  }

  const submittedQuery = queryResult.query;
  if (!submittedQuery) {
    return (
      <StationSummaryPageView
        catalog={catalogResult.catalog}
        state={{ kind: "idle", title: "Select scope and apply", message: "Choose a trusted Line, Station / WS, and bounded time window before requesting production data." }}
      />
    );
  }

  const selectedLine = catalogResult.catalog.lines.find((line) => line.lineId === submittedQuery.lineId);
  const selectedStation = selectedLine?.stations.find((station) => station.stationId === submittedQuery.stationId);
  if (!selectedLine || !selectedStation) {
    return (
      <StationSummaryPageView
        catalog={catalogResult.catalog}
        state={{ kind: "invalid-query", message: "line_id and station_id must match the trusted scope catalog" }}
      />
    );
  }

  const result = await fetchStationSummary(submittedQuery, resolution.origin);
  if (!result.ok) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: result.kind === "invalid-query" ? "invalid-query" : "error", message: result.message }} />;
  }

  return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "ready", query: submittedQuery, viewModel: toStationSummaryViewModel(submittedQuery, result) }} />;
}
