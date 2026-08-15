const productSurfaces = [
  {
    href: "/station-summary",
    eyebrow: "Primary MVP view",
    title: "Station Summary",
    description: "Review one trusted station and bounded production window across Quality and Process Metrics, with unsupported authority kept explicit.",
    action: "Open station summary",
  },
  {
    href: "/accepted-events",
    eyebrow: "Accepted fact detail",
    title: "Accepted Events",
    description: "Inspect read-only accepted station-event facts and their bounded trace and NOK evidence without diagnostic or raw-data fallback.",
    action: "Open accepted events",
  },
] as const;

export default function DashboardHomePage() {
  return (
    <main className="dashboard-shell product-home-shell">
      <header className="product-home-header">
        <p className="product-home-eyebrow">Edge MES · Production truth</p>
        <h1>Production insight, from accepted facts.</h1>
        <p>
          Choose a read-only product surface. Trusted production data stays separate from unsupported, unavailable, and diagnostic-only information.
        </p>
      </header>

      <section className="product-home-surface-grid" aria-label="Dashboard product surfaces">
        {productSurfaces.map((surface) => (
          <article className="product-home-surface-card" key={surface.href}>
            <div className="product-home-surface-copy">
              <p className="product-home-surface-eyebrow">{surface.eyebrow}</p>
              <h2>{surface.title}</h2>
              <p>{surface.description}</p>
            </div>
            <a className="product-home-surface-link" href={surface.href}>
              {surface.action}
              <span aria-hidden="true">→</span>
            </a>
          </article>
        ))}
      </section>

      <footer className="product-home-policy" aria-label="Dashboard data policy">
        <span>Read-only</span>
        <span>Trusted API surfaces</span>
        <span>No fabricated fallback</span>
      </footer>
    </main>
  );
}
