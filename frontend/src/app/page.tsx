import { resolveDashboardProductSurface } from "../lib/productSurfaces";

export const dynamic = "force-dynamic";

type ProductSurface = {
  href: string | null;
  eyebrow: string;
  title: string;
  description: string;
  action: string;
};

function resolveProductSurfaceHref(surface: "trace" | "vplc") {
  const resolution = resolveDashboardProductSurface(surface);
  return resolution.ok ? resolution.href : null;
}

export default function DashboardHomePage() {
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
    {
      href: "/deployment/plc",
      eyebrow: "Field deployment",
      title: "PLC Deployment Configuration",
      description: "Prepare and validate a candidate PLC connection and line selection. Active runtime configuration stays read-only, and Test Connection never writes to the PLC.",
      action: "Open PLC Deployment Configuration",
    },
    {
      href: resolveProductSurfaceHref("trace"),
      eyebrow: "Production traceability",
      title: "Trace",
      description:
        "Open the existing complete unit trace for DMC, payload, result, defect, skip, label, and the active configured route lineage.",
      action: "Open Trace",
    },
    {
      href: resolveProductSurfaceHref("vplc"),
      eyebrow: "Simulator / control",
      title: "V-PLC Console",
      description:
        "Operate the existing virtual PLC demo surface for profile, plan, station parameters, and controlled NOK simulation; this is not field PLC deployment configuration.",
      action: "Open V-PLC Console",
    },
  ] satisfies ProductSurface[];

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
            {surface.href ? (
              <a className="product-home-surface-link" href={surface.href}>
                {surface.action}
                <span aria-hidden="true">→</span>
              </a>
            ) : (
              <span className="product-home-surface-link" aria-disabled="true">
                Surface unavailable
              </span>
            )}
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
