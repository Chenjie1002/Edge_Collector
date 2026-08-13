type StationSummaryStateContent = { message: string; title?: string };

export type StationSummaryPageState =
  | ({ kind: "idle" } & StationSummaryStateContent)
  | ({ kind: "invalid-query" } & StationSummaryStateContent)
  | ({ kind: "loading"; priorDataNotice?: string } & StationSummaryStateContent)
  | ({ kind: "error" } & StationSummaryStateContent)
  | ({ kind: "unavailable" } & StationSummaryStateContent)
  | ({ kind: "malformed" } & StationSummaryStateContent);

function stateLabel(kind: StationSummaryPageState["kind"]): string {
  if (kind === "idle") return "IDLE";
  if (kind === "invalid-query") return "INVALID_QUERY";
  if (kind === "loading") return "LOADING";
  if (kind === "unavailable") return "UNAVAILABLE";
  if (kind === "malformed") return "MALFORMED";
  return "ERROR";
}

export function StationSummaryStateMessage({ state }: { state: StationSummaryPageState }) {
  return (
    <section
      className={`state-message station-summary-state-message state-${state.kind}`}
      role={state.kind === "loading" || state.kind === "idle" ? "status" : "alert"}
    >
      {state.title ? <p className="station-summary-state-code">{stateLabel(state.kind)}</p> : null}
      <h2>{state.title ?? stateLabel(state.kind)}</h2>
      <p>{state.message}</p>
      {state.kind === "loading" && state.priorDataNotice ? <p>{state.priorDataNotice}</p> : null}
    </section>
  );
}
