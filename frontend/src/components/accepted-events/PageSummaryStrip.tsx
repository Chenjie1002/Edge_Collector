import type { PageSummary } from "../../lib/acceptedStationEvents/viewModel";

type Props = {
  summary: PageSummary;
};

function renderCounts(counts: Record<string, number>) {
  return Object.entries(counts)
    .map(([key, count]) => `${key}: ${count}`)
    .join(" / ");
}

export function PageSummaryStrip({ summary }: Props) {
  return (
    <section className="summary-strip" aria-label="Accepted events page summary">
      <div>
        <span>{summary.label}</span>
        <strong>{summary.totalAcceptedFacts}</strong>
        <small>accepted facts</small>
      </div>
      <div>
        <span>Result mix</span>
        <strong>{renderCounts(summary.byResult) || "none"}</strong>
      </div>
      <div>
        <span>Station mix</span>
        <strong>{renderCounts(summary.byStation) || "none"}</strong>
      </div>
    </section>
  );
}
