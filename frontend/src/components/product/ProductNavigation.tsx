import { resolveDashboardProductSurface } from "../../lib/productSurfaces";

type NavigationDestination = {
  label: string;
  href: string | null;
};

function externalSurface(surface: "trace" | "vplc"): string | null {
  const resolution = resolveDashboardProductSurface(surface);
  return resolution.ok ? resolution.href : null;
}

export function ProductNavigation() {
  const destinations: NavigationDestination[] = [
    { label: "Dashboard", href: "/" },
    { label: "Station Summary", href: "/station-summary" },
    { label: "Accepted Events", href: "/accepted-events" },
    { label: "PLC Deployment", href: "/deployment/plc" },
    { label: "Trace", href: externalSurface("trace") },
    { label: "V-PLC", href: externalSurface("vplc") },
  ];

  return (
    <nav className="product-navigation" aria-label="Primary product navigation">
      <a className="product-navigation-brand" href="/">Edge MES</a>
      <div className="product-navigation-links">
        {destinations.map((destination) =>
          destination.href ? (
            <a key={destination.label} href={destination.href}>{destination.label}</a>
          ) : (
            <span key={destination.label} className="product-navigation-unavailable" aria-disabled="true">{destination.label}</span>
          ),
        )}
      </div>
    </nav>
  );
}
