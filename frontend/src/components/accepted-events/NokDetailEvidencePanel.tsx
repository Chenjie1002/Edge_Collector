import type { NokDetailEvidence } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  evidence: NokDetailEvidence | null;
};

export function NokDetailEvidencePanel({ evidence }: Props) {
  if (!evidence) return <section className="evidence-panel">NOK/detail evidence not available.</section>;

  return (
    <section className="evidence-panel" aria-label="Accepted NOK detail evidence">
      <h2>NOK/detail evidence</h2>
      <dl>
        <dt>Row role</dt>
        <dd>{evidence.rowRole}</dd>
        <dt>Event type</dt>
        <dd>{evidence.eventType.text}</dd>
        <dt>Production result</dt>
        <dd>{evidence.productionResult.text}</dd>
        <dt>NOK code</dt>
        <dd>{evidence.nokCode.text}</dd>
        <dt>NOK origin</dt>
        <dd>{evidence.nokOrigin.text}</dd>
        <dt>Detail code</dt>
        <dd>{evidence.nokDetailCode.text}</dd>
        <dt>Detail source event</dt>
        <dd>{evidence.nokDetailSourceEventId.text}</dd>
        <dt>Evidence fact</dt>
        <dd>{evidence.nokDetailEvidenceFactKey.text}</dd>
      </dl>
      <p className="reference-note">
        Fact reference {evidence.factKey}; source event {evidence.sourceEventId.text}.
      </p>
    </section>
  );
}
