import type { TraceReference } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  reference: TraceReference | null;
};

export function TraceReferencePanel({ reference }: Props) {
  if (!reference) return <section className="trace-panel">Trace references not available.</section>;

  return (
    <section className="trace-panel" aria-label="Accepted fact trace references">
      <h2>Trace references</h2>
      <dl>
        <dt>Unit</dt>
        <dd>{reference.unitId.text}</dd>
        <dt>DMC</dt>
        <dd>{reference.dmc.text}</dd>
        <dt>Cycle counter</dt>
        <dd>{reference.cycleCounter.text}</dd>
        <dt>Source event</dt>
        <dd>{reference.sourceEventId.text}</dd>
        <dt>Event time</dt>
        <dd>{reference.eventTs.text}</dd>
        <dt>Accepted fact timestamp</dt>
        <dd>{reference.acceptedAt.text}</dd>
        <dt>Fact key</dt>
        <dd>{reference.factKeyDisplay.text}</dd>
        <dt>Content fingerprint</dt>
        <dd>{reference.contentFingerprint.text}</dd>
        <dt>Line / PLC / station</dt>
        <dd>
          {reference.lineId.text} / {reference.plcId.text} / {reference.stationId.text}
        </dd>
        <dt>Profile / config</dt>
        <dd>
          {reference.profileId.text} / {reference.configVersion.text} / {reference.configHash.text}
        </dd>
      </dl>
    </section>
  );
}
