import { AcceptedEventsTable } from "../../components/accepted-events/AcceptedEventsTable";
import { AcceptedEventsQueryControls } from "../../components/accepted-events/AcceptedEventsQueryControls";
import { AcceptedEventsStateMessage, type AcceptedEventsPageState } from "../../components/accepted-events/AcceptedEventsStates";
import { NokDetailEvidencePanel } from "../../components/accepted-events/NokDetailEvidencePanel";
import { PageSummaryStrip } from "../../components/accepted-events/PageSummaryStrip";
import { TraceReferencePanel } from "../../components/accepted-events/TraceReferencePanel";
import { fetchAcceptedStationEvents } from "../../lib/acceptedStationEvents/apiClient";
import { validateAcceptedStationEventsQuery, type AcceptedStationEventsQuery } from "../../lib/acceptedStationEvents/query";
import { toAcceptedEventsViewModel, type AcceptedEventsViewModel } from "../../lib/acceptedStationEvents/viewModel";

type SearchParams = Record<string, string | string[] | undefined>;

type PageViewState =
  | AcceptedEventsPageState
  | {
      kind: "ready";
      query: AcceptedStationEventsQuery;
      viewModel: AcceptedEventsViewModel;
    };

const DEFAULT_LIMIT = 50;

export const dynamic = "force-dynamic";

function firstParam(params: SearchParams, key: string): string | undefined {
  const value = params[key];
  return Array.isArray(value) ? value[0] : value;
}

function queryFromSearchParams(params: SearchParams): AcceptedStationEventsQuery {
  const limit = Number(firstParam(params, "limit") ?? DEFAULT_LIMIT);
  return {
    lineId: firstParam(params, "line_id") ?? "",
    startTime: firstParam(params, "start_time") ?? "",
    endTime: firstParam(params, "end_time") ?? "",
    limit,
    cursor: firstParam(params, "cursor")
  };
}

export function AcceptedEventsPageView({ state }: { state: PageViewState }) {
  if (state.kind !== "ready") {
    return (
      <main className="dashboard-shell">
        <h1>Accepted events</h1>
        <AcceptedEventsStateMessage state={state} />
      </main>
    );
  }

  return (
    <main className="dashboard-shell">
      <header>
        <h1>Accepted events</h1>
        <p>Read-only accepted station-event facts from the bounded query scope.</p>
      </header>
      <AcceptedEventsQueryControls query={state.query} />
      <PageSummaryStrip summary={state.viewModel.summary} />
      {state.viewModel.rows.length === 0 ? (
        <AcceptedEventsStateMessage state={{ kind: "empty", message: "No accepted facts returned for the current bounded scope." }} />
      ) : (
        <AcceptedEventsTable rows={state.viewModel.rows} selectedFactKey={state.viewModel.rows[0]?.factKey} />
      )}
      <div className="detail-grid">
        <NokDetailEvidencePanel evidence={state.viewModel.selectedEvidence} />
        <TraceReferencePanel reference={state.viewModel.selectedReference} />
      </div>
    </main>
  );
}

export default async function AcceptedEventsPage({
  searchParams
}: {
  searchParams?: SearchParams | Promise<SearchParams>;
}) {
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const query = queryFromSearchParams(resolvedSearchParams);
  const validation = validateAcceptedStationEventsQuery(query);
  if (!validation.ok) {
    return <AcceptedEventsPageView state={{ kind: "invalid-query", message: validation.reason }} />;
  }

  const result = await fetchAcceptedStationEvents(validation.query);
  if (!result.ok) {
    return <AcceptedEventsPageView state={{ kind: result.kind, message: result.message }} />;
  }

  return (
    <AcceptedEventsPageView
      state={{
        kind: "ready",
        query: validation.query,
        viewModel: toAcceptedEventsViewModel(result.envelope)
      }}
    />
  );
}
