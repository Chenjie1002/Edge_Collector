export type DashboardProductSurface = "trace" | "vplc";

export type DashboardProductSurfaceEnvironment = Readonly<{
  EDGE_MES_DASHBOARD_TRACE_ORIGIN?: string;
  EDGE_MES_DASHBOARD_VPLC_ORIGIN?: string;
}>;

export type DashboardProductSurfaceResolution =
  | { readonly ok: true; readonly href: string }
  | { readonly ok: false; readonly code: "ORIGIN_INVALID" };

const surfaceConfiguration: Record<
  DashboardProductSurface,
  {
    readonly environmentKey: keyof DashboardProductSurfaceEnvironment;
    readonly defaultOrigin: string;
    readonly path: string;
  }
> = {
  trace: {
    environmentKey: "EDGE_MES_DASHBOARD_TRACE_ORIGIN",
    defaultOrigin: "http://127.0.0.1:8000",
    path: "/trace"
  },
  vplc: {
    environmentKey: "EDGE_MES_DASHBOARD_VPLC_ORIGIN",
    defaultOrigin: "http://127.0.0.1:8200",
    path: "/vplc"
  }
};

function invalidOrigin(): DashboardProductSurfaceResolution {
  return { ok: false, code: "ORIGIN_INVALID" };
}

export function resolveDashboardProductSurface(
  surface: DashboardProductSurface,
  environment?: DashboardProductSurfaceEnvironment
): DashboardProductSurfaceResolution {
  const configuration = surfaceConfiguration[surface];
  const configuredOrigin = environment?.[configuration.environmentKey];
  const rawOrigin = configuredOrigin ?? configuration.defaultOrigin;

  if (rawOrigin === "" || rawOrigin !== rawOrigin.trim()) return invalidOrigin();

  let parsedOrigin: URL;
  try {
    parsedOrigin = new URL(rawOrigin);
  } catch {
    return invalidOrigin();
  }

  if (
    !["http:", "https:"].includes(parsedOrigin.protocol) ||
    parsedOrigin.username !== "" ||
    parsedOrigin.password !== "" ||
    parsedOrigin.pathname !== "/" ||
    parsedOrigin.search !== "" ||
    parsedOrigin.hash !== "" ||
    parsedOrigin.hostname === ""
  ) {
    return invalidOrigin();
  }

  return { ok: true, href: `${parsedOrigin.origin}${configuration.path}` };
}
