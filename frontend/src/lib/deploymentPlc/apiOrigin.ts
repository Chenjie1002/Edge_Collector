export type DeploymentApiOriginEnvironment = Readonly<{
  EDGE_MES_DASHBOARD_API_ORIGIN?: string;
}>;

export type DeploymentApiOriginResolution =
  | { ok: true; origin: string }
  | { ok: false; code: "ORIGIN_INVALID" };

export function resolveDeploymentApiOrigin(
  environment?: DeploymentApiOriginEnvironment
): DeploymentApiOriginResolution {
  const source = environment ?? {
    EDGE_MES_DASHBOARD_API_ORIGIN: process.env.EDGE_MES_DASHBOARD_API_ORIGIN
  };
  const rawOrigin = source.EDGE_MES_DASHBOARD_API_ORIGIN ?? "http://127.0.0.1:8000";
  if (rawOrigin === "" || rawOrigin !== rawOrigin.trim()) return { ok: false, code: "ORIGIN_INVALID" };
  try {
    const parsed = new URL(rawOrigin);
    if (
      !["http:", "https:"].includes(parsed.protocol) ||
      parsed.username !== "" ||
      parsed.password !== "" ||
      parsed.pathname !== "/" ||
      parsed.search !== "" ||
      parsed.hash !== "" ||
      parsed.hostname === ""
    ) {
      return { ok: false, code: "ORIGIN_INVALID" };
    }
    return { ok: true, origin: parsed.origin };
  } catch {
    return { ok: false, code: "ORIGIN_INVALID" };
  }
}
