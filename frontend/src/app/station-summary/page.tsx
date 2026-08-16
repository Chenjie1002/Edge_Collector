import { LineFlowSummary } from "../../components/station-summary/LineFlowSummary";
import { StationSummaryCards } from "../../components/station-summary/StationSummaryCards";
import { ProcessMetricMatrix } from "../../components/station-summary/ProcessMetricMatrix";
import { StationSummaryQueryControls } from "../../components/station-summary/StationSummaryQueryControls";
import { StationSummaryStateMessage, type StationSummaryPageState } from "../../components/station-summary/StationSummaryStates";
import { resolveTrustedAcceptedEventsApiOrigin } from "../../lib/acceptedStationEvents/apiOrigin";
import { fetchStationSummary } from "../../lib/stationSummary/apiClient";
import { fetchLineSummary } from "../../lib/stationSummary/lineSummaryApi";
import { validateLineSummaryQuery, type LineSummaryQuery } from "../../lib/stationSummary/lineSummaryQuery";
import type { LineSummary } from "../../lib/stationSummary/lineSummarySchema";
import { validateStationSummaryQuery, type StationSummaryQuery } from "../../lib/stationSummary/query";
import { fetchTrustedScopeCatalog, type TrustedScopeCatalog } from "../../lib/stationSummary/scopeCatalog";
import { quickRangeAt } from "../../lib/stationSummary/timeWindow";
import { toStationSummaryViewModel, type StationSummaryViewModel } from "../../lib/stationSummary/viewModel";

type SearchParams = Record<string, string | string[] | undefined>;

type StationDetailState =
  | { kind: "ready"; viewModel: StationSummaryViewModel }
  | { kind: "unavailable"; message: string };

type PageViewState =
  | StationSummaryPageState
  | {
      kind: "ready";
      query: LineSummaryQuery;
      summary: LineSummary;
      stationDetail?: StationDetailState;
    };

const QUERY_KEYS = ["line_id", "station_id", "start_time", "end_time"] as const;

export const dynamic = "force-dynamic";

function singleParam(params: SearchParams, key: string): { ok: true; value: string | undefined } | { ok: false; reason: string } {
  const value = params[key];
  if (Array.isArray(value)) return { ok: false, reason: `${key} must be provided once` };
  return { ok: true, value };
}

function queryFromSearchParams(params: SearchParams): { ok: true; query?: LineSummaryQuery } | { ok: false; reason: string } {
  const keys = Object.keys(params);
  if (keys.length === 0) return { ok: true };
  if (keys.some((key) => !QUERY_KEYS.includes(key as (typeof QUERY_KEYS)[number]))) {
    return { ok: false, reason: "Only line_id, optional station_id, start_time, and end_time are supported" };
  }

  const line = singleParam(params, "line_id");
  const station = singleParam(params, "station_id");
  const start = singleParam(params, "start_time");
  const end = singleParam(params, "end_time");
  if (!line.ok) return line;
  if (!station.ok) return station;
  if (!start.ok) return start;
  if (!end.ok) return end;
  const validation = validateLineSummaryQuery({
    lineId: line.value ?? "",
    stationId: station.value ?? undefined,
    startTime: start.value ?? "",
    endTime: end.value ?? "",
  });
  return validation.ok ? validation : { ok: false, reason: validation.reason };
}

function topologyMatchesCatalog(summary: LineSummary, line: TrustedScopeCatalog["lines"][number]): boolean {
  const catalogStationIds = line.stations.map((station) => station.stationId);
  return (
    summary.scope.lineId === line.lineId &&
    summary.topology.stations.length === catalogStationIds.length &&
    summary.topology.stations.every((stationId, index) => stationId === catalogStationIds[index])
  );
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

export function StationSummaryPageView({ state, catalog = null }: { state: PageViewState; catalog?: TrustedScopeCatalog | null }) {
  const query = state.kind === "ready" ? state.query : undefined;
  return (
    <main className="dashboard-shell station-summary-shell">
      <header className="station-summary-header">
        <div className="station-summary-header-copy">
          <p className="station-summary-eyebrow">Production flow · Trusted read-only</p>
          <h1>Station Summary</h1>
          <p>Trusted production view for the whole selected line and bounded time window. Every station is compared with the same terminal-completed cohort.</p>
        </div>
        <div className="station-summary-header-policy" aria-label="Station summary data policy">
          <span>Whole-line cohort</span>
          <span>No fabricated fallback</span>
        </div>
      </header>
      <StationSummaryQueryControls catalog={catalog} query={query} defaultWindow={query ? undefined : quickRangeAt(new Date(), 8)} />
      {state.kind !== "ready" ? (
        <StationSummaryStateMessage state={state} />
      ) : (
        <section className="station-summary-results" aria-label="Station summary results">
          <header className="station-summary-results-heading">
            <div>
              <p className="station-summary-results-kicker">Selected line</p>
              <h2>{state.query.lineId}</h2>
            </div>
            <p>{state.query.startTime} → {state.query.endTime}</p>
          </header>
          <LineFlowSummary summary={state.summary} />
          {state.query.stationId ? (
            <details className="station-summary-secondary-detail">
              <summary>Station detail (optional): {state.query.stationId}</summary>
              {state.stationDetail?.kind === "ready" ? (
                <div className="station-summary-secondary-detail-content">
                  <StationSummaryCards quality={state.stationDetail.viewModel.quality} />
                  <details className="station-summary-diagnostics-detail">
                    <summary>Data diagnostics</summary>
                    <ProcessMetricMatrix panel={state.stationDetail.viewModel.processMetrics} />
                  </details>
                </div>
              ) : (
                <p className="station-summary-panel-alert" role="alert">{state.stationDetail?.message ?? "Optional station detail is unavailable."}</p>
              )}
            </details>
          ) : null}
        </section>
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
        state={{ kind: "idle", title: "Select line and apply", message: "Choose a trusted Line and bounded time window before requesting the whole-line production cohort." }}
      />
    );
  }

  const selectedLine = catalogResult.catalog.lines.find((line) => line.lineId === submittedQuery.lineId);
  const selectedStation = submittedQuery.stationId && selectedLine?.stations.find((station) => station.stationId === submittedQuery.stationId);
  if (!selectedLine || (submittedQuery.stationId && !selectedStation)) {
    return (
      <StationSummaryPageView
        catalog={catalogResult.catalog}
        state={{ kind: "invalid-query", message: "line_id and optional station_id must match the trusted scope catalog" }}
      />
    );
  }

  const result = await fetchLineSummary(submittedQuery, resolution.origin);
  if (!result.ok) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: result.kind === "invalid-query" ? "invalid-query" : result.kind, message: result.message }} />;
  }
  if (!topologyMatchesCatalog(result.summary, selectedLine)) {
    return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "malformed", message: "The line summary topology does not match the trusted scope catalog." }} />;
  }

  let stationDetail: StationDetailState | undefined;
  const detailQuery = stationDetailQuery(submittedQuery);
  if (detailQuery) {
    const detailResult = await fetchStationSummary(detailQuery, resolution.origin);
    stationDetail = detailResult.ok
      ? { kind: "ready", viewModel: toStationSummaryViewModel(detailQuery, detailResult) }
      : { kind: "unavailable", message: detailResult.message };
  }

  return <StationSummaryPageView catalog={catalogResult.catalog} state={{ kind: "ready", query: submittedQuery, summary: result.summary, stationDetail }} />;
}
