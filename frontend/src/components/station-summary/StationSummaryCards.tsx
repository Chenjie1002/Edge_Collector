import type { QualitySummaryViewModel } from "../../lib/stationSummary/viewModel";

type Props = {
  quality: QualitySummaryViewModel;
};

function countText(quality: QualitySummaryViewModel, key: "ok" | "nok" | "denominator"): string {
  return quality.counts ? String(quality.counts[key]) : "No numeric value authorized";
}

export function StationSummaryCards({ quality }: Props) {
  return (
    <section className="station-summary-panel station-summary-quality-panel" aria-label="Trusted Quality route summary">
      <header className="station-summary-panel-heading">
        <div>
          <p className="station-summary-panel-kicker">Quality</p>
          <h2>Accepted production quality</h2>
        </div>
        <div className="station-summary-source-status">
          <span>{quality.sourceLabel}</span>
          <strong className="station-summary-status-badge" data-status={quality.status}>{quality.status}</strong>
        </div>
      </header>
      <div className="summary-strip station-summary-quality-grid">
        <div>
          <span>OK</span>
          <strong>{countText(quality, "ok")}</strong>
          <small>{quality.scopeLabel}</small>
        </div>
        <div>
          <span>NOK</span>
          <strong>{countText(quality, "nok")}</strong>
          <small>{quality.dataSufficiency ? `Data sufficiency: ${quality.dataSufficiency}` : "No source value"}</small>
        </div>
        <div>
          <span>Denominator</span>
          <strong>{countText(quality, "denominator")}</strong>
          <small>{quality.windowLabel}</small>
        </div>
        <div>
          <span>Quality rate</span>
          <strong>{quality.qualityRateText}</strong>
          <small>{quality.message ?? "Only an explicitly authorized numeric rate is shown."}</small>
        </div>
      </div>
    </section>
  );
}
