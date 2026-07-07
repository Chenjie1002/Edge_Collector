import type { NokDetailEvidence } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  evidence: NokDetailEvidence | null;
};

export function NokDetailEvidencePanel({ evidence }: Props) {
  if (!evidence) return <section className="evidence-panel">NOK/detail evidence absent / unknown</section>;

  const hasEvidence =
    evidence.nokCode ||
    evidence.nokOrigin ||
    evidence.nokDetailCode ||
    evidence.nokDetailSourceEventId ||
    evidence.nokDetailEvidenceFactKey;

  return (
    <section className="evidence-panel" aria-label="Accepted NOK detail evidence">
      <h2>NOK/detail evidence</h2>
      {!hasEvidence ? (
        <p>Accepted NOK/detail evidence absent / unknown.</p>
      ) : (
        <dl>
          <dt>Production result</dt>
          <dd>{evidence.productionResult}</dd>
          <dt>NOK code</dt>
          <dd>{evidence.nokCode ?? "absent / unknown"}</dd>
          <dt>NOK origin</dt>
          <dd>{evidence.nokOrigin ?? "absent / unknown"}</dd>
          <dt>Detail code</dt>
          <dd>{evidence.nokDetailCode ?? "absent / unknown"}</dd>
          <dt>Detail source event</dt>
          <dd>{evidence.nokDetailSourceEventId ?? "absent / unknown"}</dd>
          <dt>Evidence fact</dt>
          <dd>{evidence.nokDetailEvidenceFactKey ?? "absent / unknown"}</dd>
        </dl>
      )}
      <p className="reference-note">
        Fact reference {evidence.factKey}; source event {evidence.sourceEventId}.
      </p>
    </section>
  );
}
