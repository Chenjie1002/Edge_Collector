import type { TraceReference } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  reference: TraceReference | null;
};

export function TraceReferencePanel({ reference }: Props) {
  if (!reference) return <section className="trace-panel">Trace references absent / unknown</section>;

  return (
    <section className="trace-panel" aria-label="Accepted fact trace references">
      <h2>Trace references</h2>
      <dl>
        <dt>Unit</dt>
        <dd>{reference.unitId ?? "unknown"}</dd>
        <dt>DMC</dt>
        <dd>{reference.dmc ?? "unknown"}</dd>
        <dt>Cycle counter</dt>
        <dd>{reference.cycleCounter ?? "unknown"}</dd>
        <dt>Source event</dt>
        <dd>{reference.sourceEventId}</dd>
        <dt>Event time</dt>
        <dd>{reference.eventTs}</dd>
        <dt>Accepted fact timestamp</dt>
        <dd>{reference.acceptedAt}</dd>
        <dt>Fact key</dt>
        <dd>{reference.factKey}</dd>
        <dt>Content fingerprint</dt>
        <dd>{reference.contentFingerprint}</dd>
        <dt>Line / PLC / station</dt>
        <dd>
          {reference.lineId} / {reference.plcId} / {reference.stationId}
        </dd>
        <dt>Profile / config</dt>
        <dd>
          {reference.profileId} / {reference.configVersion} / {reference.configHash}
        </dd>
      </dl>
    </section>
  );
}
