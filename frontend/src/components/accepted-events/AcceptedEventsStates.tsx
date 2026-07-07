export type AcceptedEventsPageState =
  | { kind: "invalid-query"; message: string }
  | { kind: "loading"; message: string; priorDataNotice?: string }
  | { kind: "empty"; message: string }
  | { kind: "error"; message: string }
  | { kind: "unavailable"; message: string };

export function AcceptedEventsStateMessage({ state }: { state: AcceptedEventsPageState }) {
  return (
    <section className={`state-message state-${state.kind}`} role={state.kind === "loading" ? "status" : "alert"}>
      <h2>{state.kind}</h2>
      <p>{state.message}</p>
      {state.kind === "empty" ? <p>No accepted facts in this bounded scope.</p> : null}
      {state.kind === "loading" && state.priorDataNotice ? <p>{state.priorDataNotice}</p> : null}
    </section>
  );
}
